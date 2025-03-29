from typing import Dict, Any, List
from github import Github, GithubException, Repository
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from crewai_tools import DirectorySearchTool
from pydantic import BaseModel, Field, field_validator, ConfigDict, ValidationError
from crewai.tools import BaseTool
import tempfile
import shutil
from pathlib import Path
import re

class ProjectInfo(BaseModel):
    model_config = ConfigDict(extra='forbid')
    
    name: str = Field(..., description="Nom du dépôt")
    description: str = Field("", description="Description du projet")
    main_features: List[str] = Field(..., description="Fonctionnalités principales", min_items=3)
    technologies: List[str] = Field(..., description="Technologies utilisées", min_items=3)
    difficulty: str = Field(..., description="Niveau de difficulté (Débutant, Intermédiaire, Avancé)")
    stars: int = Field(..., description="Nombre d'étoiles")
    updated_at: datetime = Field(..., description="Dernière mise à jour")
    analysis_score: float = Field(..., ge=0, le=10, description="Score d'analyse technique")

    @field_validator('difficulty')
    @classmethod
    def validate_difficulty(cls, v: str) -> str:
        valid_levels = ["Débutant", "Intermédiaire", "Avancé"]
        if v not in valid_levels:
            raise ValueError(f"Niveau invalide: {v}. Options: {', '.join(valid_levels)}")
        return v

class GitHubAnalyzerTool(BaseTool):
    name: str = "GitHub Portfolio Analyzer"
    description: str = (
        "Analyse complète de tous les dépôts GitHub d'un utilisateur pour l'optimisation CV. "
        "Fournit une analyse technique détaillée et des métriques de qualité."
    )

    def __init__(self, github_token: str):
        super().__init__()
        self.github = Github(github_token)
        self.llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.1)
        self.parser = PydanticOutputParser(pydantic_object=ProjectInfo)

    def _run(self, username: str, max_repos: int = 10) -> Dict[str, Any]:
        try:
            user = self.github.get_user(username)
            repos = self._get_filtered_repos(user, max_repos)
            
            results = []
            for repo in repos:
                try:
                    result = self._full_analysis(repo)
                    results.append(result)
                except Exception as e:
                    continue

            return self._generate_summary(results)

        except GithubException as e:
            raise RuntimeError(f"Erreur GitHub: {str(e)}")

    def _get_filtered_repos(self, user, max_repos: int) -> List[Repository.Repository]:
        return sorted(
            user.get_repos(sort="updated", direction="desc"),
            key=lambda r: (-r.stargazers_count, -r.forks_count),
        )[:max_repos]

    def _full_analysis(self, repo: Repository.Repository) -> Dict[str, Any]:
        with tempfile.TemporaryDirectory() as temp_dir:
            self._clone_repo(repo.clone_url, temp_dir)
            
            code_analysis = self._analyze_codebase(temp_dir)
            readme_analysis = self._analyze_readme(repo)
            
            return {
                "basic_info": self._get_basic_info(repo),
                "technical_analysis": code_analysis,
                "readme_quality": readme_analysis,
                "market_score": self._calculate_market_score(repo),
            }

    def _analyze_codebase(self, repo_path: str) -> Dict[str, Any]:
        try:
            search_tool = DirectorySearchTool(
                directory=repo_path,
                glob="**/*.py",
                recursive=True,
                chunk_size=2000,
                similarity_threshold=0.85,
            )

            prompt_template = PromptTemplate(
                template="""Analyse technique du code suivant :
                {context}
                
                {format_instructions}
                """,
                input_variables=["context"],
                partial_variables={"format_instructions": self.parser.get_format_instructions()}
            )

            context = search_tool.run("Analyse de l'architecture et des patterns techniques")
            result = self.llm.invoke(prompt_template.format(context=context))
            
            return self.parser.parse(result.content).dict()

        except ValidationError as e:
            return {"error": str(e)}

    def _analyze_readme(self, repo: Repository.Repository) -> Dict[str, Any]:
        readme = self._get_readme_content(repo)
        return {
            "quality_score": len(readme) // 1000,
            "sections": self._detect_readme_sections(readme),
            "update_frequency": self._calculate_update_frequency(repo),
        }

    def _get_basic_info(self, repo: Repository.Repository) -> Dict[str, Any]:
        return {
            "name": repo.name,
            "description": repo.description,
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "languages": repo.get_languages(),
            "created_at": repo.created_at.isoformat(),
            "updated_at": repo.updated_at.isoformat(),
            "topics": repo.get_topics(),
            "size": repo.size,
            "license": repo.license.spdx_id if repo.license else None,
        }

    def _clone_repo(self, clone_url: str, target_dir: str):
        Repo.clone_from(clone_url, target_dir, depth=1, filter="blob:none")

    def _get_readme_content(self, repo: Repository.Repository) -> str:
        try:
            readme = repo.get_readme()
            return readme.decoded_content.decode("utf-8")[:10000]
        except:
            return ""

    # Méthodes utilitaires supplémentaires
    def _calculate_market_score(self, repo: Repository.Repository) -> float:
        return (repo.stargazers_count * 0.4 + 
                repo.forks_count * 0.3 + 
                len(repo.get_commits()) * 0.2 + 
                len(repo.get_contributors()) * 0.1)

    def _detect_readme_sections(self, content: str) -> List[str]:
        sections = []
        if re.search(r"##\s+Installation", content, re.IGNORECASE):
            sections.append("installation")
        if re.search(r"##\s+Features", content, re.IGNORECASE):
            sections.append("features")
        return sections

    def _generate_summary(self, results: List[Dict]) -> Dict[str, Any]:
        return {
            "user_summary": {
                "total_repos": len(results),
                "top_languages": self._get_top_technologies(results),
                "activity_score": sum(r["basic_info"]["stars"] for r in results),
            },
            "project_analyses": results,
        }

    def _get_top_technologies(self, results: List[Dict]) -> List[str]:
        tech_counter = Counter()
        for project in results:
            tech_counter.update(project["technical_analysis"].get("technologies", []))
        return [tech for tech, _ in tech_counter.most_common(5)]