from typing import Dict, Any, List
from github import Github
import requests
from ..utils.logger import Logger
from ..utils.exceptions import GitHubError, APIError
from ..utils.validators import DataValidator
from langchain.tools import tool
from crewai.tools import DirectoryRAGSearch
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
import re
import os
from datetime import datetime

class ProjectInfo(BaseModel):
    """Structure simple pour stocker les informations du projet"""
    description: str = Field(description="Description simple du projet")
    main_features: List[str] = Field(description="Liste des fonctionnalités principales")
    technologies: List[str] = Field(description="Technologies utilisées")
    difficulty: str = Field(description="Niveau de difficulté (Débutant, Intermédiaire, Avancé)")

class GitHubTools:
    def __init__(self, github_token: str, logger: Logger):
        self.github = Github(github_token)
        self.logger = logger
        self.validator = DataValidator()
        self.parser = PydanticOutputParser(pydantic_object=ProjectInfo)

    @tool("Analyse un dépôt GitHub et extrait les informations pertinentes")
    def analyze_repository(self, repo_url: str) -> Dict[str, Any]:
        """Analyse un dépôt GitHub et extrait les informations pertinentes."""
        try:
            self.logger.info("L'url de votre repos doit être au format : https://github.com/username/repo-name")
            self.logger.debug(f"Analyse du dépôt: {repo_url}")
            
            parts = repo_url.rstrip('/').split('/')
            if len(parts) < 5:
                raise GitHubError("URL de dépôt GitHub invalide reverifier s'il vous plait inspirez vous de l'exemple donnée precedemment")
            
            username = parts[-2]
            repo_name = parts[-1]
            
            repo = self.github.get_repo(f"{username}/{repo_name}")
            
            basic_info = {
                'name': repo.name,
                'description': repo.description,
                'stars': repo.stargazers_count,
                'forks': repo.forks_count,
                'languages': list(repo.get_languages().keys()),
                'topics': repo.get_topics(),
                'readme': self._get_readme_content(repo),
                'issues': self._get_issues_stats(repo),
                'pull_requests': self._get_pull_requests_stats(repo)
            }
            
            code_analysis = self._analyze_code(repo_url)
            
            # Combiner les résultats
            data = {
                "basic_info": basic_info,
                "code_analysis": code_analysis,
                "analyzed_at": datetime.now().isoformat()
            }
            
            errors = self.validator.validate_project_data(data)
            if errors:
                self.logger.warning(f"Problèmes de validation pour {repo_url}: {errors}")
            return data
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'analyse du dépôt {repo_url}", exc_info=e)
            raise GitHubError(f"Erreur lors de l'analyse du dépôt: {str(e)}")

    def _analyze_code(self, repo_url: str) -> Dict[str, Any]:
        """Analyse le code source du projet."""
        try:
        
            temp_path = self._clone_repo(repo_url)
            
            # Utiliser DirectoryRAGSearch pour analyser le code
            rag_search = DirectoryRAGSearch(
                directory=temp_path,
                glob="**/*.py",
                chunk_size=1000,
                chunk_overlap=200
            )
            
            prompt = PromptTemplate(
                template="""Analysez ce code et donnez une description simple du projet.
                Incluez:
                - Une description courte
                - Les fonctionnalités principales
                - Les technologies utilisées
                - Le niveau de difficulté
                
                Code:
                {context}
                
                {format_instructions}
                """,
                input_variables=["context"],
                partial_variables={"format_instructions": self.parser.get_format_instructions()}
            )
            
            # Analyser le code
            llm = ChatOpenAI(temperature=0)
            docs = rag_search.search("", k=5)
            result = llm.invoke(prompt.format(context=docs))

            self._cleanup_repo(temp_path)
    
            return self.parser.parse(result)
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'analyse du code: {str(e)}")
            raise GitHubError(f"Erreur lors de l'analyse du code: {str(e)}")

    def _clone_repo(self, repo_url: str) -> str:
        """Clone le dépôt dans un dossier temporaire Pour analyser notre repo"""
        temp_path = f"temp_repo_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.system(f"git clone {repo_url} {temp_path}")
        return temp_path

    def _cleanup_repo(self, path: str):
        """Supprime le dépôt temporaire"""
        if os.path.exists(path):
            os.system(f"rm -rf {path}")

    def _get_readme_content(self, repo) -> str:
        """Récupère le contenu du README."""
        try:
            readme = repo.get_readme()
            return readme.decoded_content.decode('utf-8')
        except:
            return "Oups vous avez oublié de mettre un README.md dans votre repo ce n'est pas une bonne pratique"

   
