from typing import Dict, Any, List
from datetime import datetime
from github import Auth, Github, GithubException, Repository
from pydantic import BaseModel, Field, ConfigDict, PrivateAttr
from crewai.tools import BaseTool
from crewai import LLM
import os

class RepoInfo(BaseModel):
    """Structure des informations brutes d'un repository"""
    name: str = Field(..., description="Nom du dépôt")
    description: str = Field("", description="Description du projet")
    languages: Dict[str, int] = Field(..., description="Langages utilisés")
    stars: int = Field(0, description="Nombre d'étoiles")
    forks: int = Field(0, description="Nombre de forks")
    topics: List[str] = Field(default_factory=list, description="Topics du projet")
    updated_at: str = Field(..., description="Dernière mise à jour")
    readme: str = Field("", description="Contenu du README")

class ProjectAnalysis(BaseModel):
    """Structure de l'analyse d'un projet"""
    name: str = Field(..., description="Nom du projet")
    technical_score: float = Field(..., ge=0, le=10, description="Score technique")
    market_relevance: float = Field(..., ge=0, le=10, description="Pertinence marché")
    main_features: List[str] = Field(..., description="Fonctionnalités principales")
    technologies: List[str] = Field(..., description="Technologies principales")
    difficulty: str = Field(..., description="Niveau de difficulté")
    learning_value: float = Field(..., ge=0, le=10, description="Valeur d'apprentissage")

class GitHubAnalyzerTool(BaseTool):
    name: str = "GitHub Portfolio Analyzer"
    description: str = "Analyse des repositories GitHub pour l'optimisation CV"

    _github: Github = PrivateAttr()
    _llm: LLM = PrivateAttr()

    def __init__(self, github_token: str):
        super().__init__()
        auth = Auth.Token(github_token)
        self._github = Github(auth=auth)
        self._llm = LLM(
            model="deepseek-coder-33b-instruct",
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url=os.getenv("DEEP_SEEK_BASE")
        )

    def _run(self, username: str, max_repos: int = 10) -> Dict[str, Any]:
        """Analyse complète des repositories"""
        print(f"Recuperation des données de {username} sur github...")
        try:
            repos_data = self._fetch_repos(username, max_repos)
            int i = 0;
            analysis_results = []
            for repo in repos_data:
                print("Traitement sur le {i} repo : ")
                analysis = self._analyze_with_llm(repo)
                analysis_results.append(analysis)
                i +=1

            summary = self._generate_summary_with_llm(analysis_results)

            return {
                "username": username,
                "summary": summary,
                "projects": analysis_results,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            raise RuntimeError(f"Erreur d'analyse: {str(e)}")

    def _fetch_repos(self, username: str, max_repos: int) -> List[Dict]:
        """Récupération des données brutes des repositories"""
        user = self._github.get_user(username)
        repos = user.get_repos(sort="updated", direction="desc")
        
        repos_data = []
        for repo in list(repos)[:max_repos]:
            try:
                repo_info = RepoInfo(
                    name=repo.name,
                    description=repo.description or "",
                    languages=repo.get_languages(),
                    stars=repo.stargazers_count,
                    forks=repo.forks_count,
                    topics=repo.get_topics(),
                    updated_at=repo.updated_at.isoformat(),
                    readme=self._get_readme_content(repo)
                )
                repos_data.append(repo_info.model_dump())
            except Exception as e:
                print(f"Erreur pour {repo.name}: {str(e)}")
                continue
                
        return repos_data

    def _get_readme_content(self, repo: Repository) -> str:
        """Récupération du README"""
        try:
            readme = repo.get_readme()
            return readme.decoded_content.decode("utf-8")
        except:
            return ""

    def _analyze_with_llm(self, repo_data: Dict) -> Dict:
        print("L'IA est entrain d'analyser le repository...")
        """Analyse d'un repository par le LLM"""
        prompt = """
        Analysez ce repository GitHub et fournissez une évaluation détaillée:

        Informations du repository:
        Nom: {name}
        Description: {description}
        Langages: {languages}
        Stars: {stars}
        Forks: {forks}
        Topics: {topics}
        README: {readme}

        Fournissez une analyse structurée avec:
        1. Score technique (0-10)
        2. Pertinence marché (0-10)
        3. Fonctionnalités principales (liste)
        4. Technologies principales utilisées (liste)
        5. Niveau de difficulté (Débutant/Intermédiaire/Avancé)
        6. Valeur d'apprentissage (0-10)

        Retournez l'analyse au format JSON.
        """

        try:
            result = self._llm.invoke(prompt.format(**repo_data))
            return ProjectAnalysis.model_validate_json(result.content).model_dump()
        except Exception as e:
            return {
                "name": repo_data["name"],
                "error": str(e)
            }

    def _generate_summary_with_llm(self, analyses: List[Dict]) -> Dict:
        """Génération du résumé par le LLM"""
        prompt = """
        Générez un résumé global de ces projets GitHub:

        Projets analysés:
        {projects}

        Fournissez un résumé avec:
        1. Technologies dominantes
        2. Points forts globaux
        3. Niveau technique global
        4. Recommandations d'amélioration

        Retournez le résumé au format JSON.
        """

        try:
            result = self._llm.invoke(prompt.format(projects=analyses))
            return result.content
        except Exception as e:
            return {"error": str(e)}