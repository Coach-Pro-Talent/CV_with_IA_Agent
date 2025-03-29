from typing import Dict, Any, List
from github import Github, GithubException
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from crewai_tools import DirectorySearchTool
from pydantic import BaseModel, Field, field_validator, ConfigDict
import os
import shutil
import tempfile
from pathlib import Path

class ProjectInfo(BaseModel):
    """Classe simple pour stocker les informations d'un projet"""
    model_config = ConfigDict(extra='forbid')
    
    description: str = Field(description="Description courte du projet")
    main_features: List[str] = Field(description="Liste des fonctionnalités principales")
    technologies: List[str] = Field(description="Technologies utilisées")
    difficulty: str = Field(description="Niveau de difficulté (Débutant, Intermédiaire, Avancé)")

    @field_validator('difficulty')
    @classmethod
    def validate_difficulty(cls, v: str) -> str:
        """Valide le niveau de difficulté"""
        valid_levels = ["Débutant", "Intermédiaire", "Avancé"]
        if v not in valid_levels:
            raise ValueError(f"Le niveau de difficulté doit être l'un des suivants: {', '.join(valid_levels)}")
        return v

    @field_validator('main_features', 'technologies')
    @classmethod
    def validate_list_items(cls, v: List[str]) -> List[str]:
        """Valide les listes de fonctionnalités et technologies"""
        if not v:
            raise ValueError("La liste ne peut pas être vide")
        return [item.strip() for item in v if item.strip()]

class GitHubAnalyzer:
    """Classe pour analyser les dépôts GitHub"""
    
    def __init__(self, github_token: str):
        """Initialise l'analyseur avec un token GitHub"""
        if not github_token:
            raise ValueError("Le token GitHub est requis")
        self.github = Github(github_token)
        self.llm = ChatOpenAI(temperature=0)

    def analyze_repository(self, repo_url: str) -> Dict[str, Any]:
        """Analyse un dépôt GitHub et retourne les informations importantes"""
        if not repo_url:
            raise ValueError("L'URL du dépôt est requise")
            
        try:
            if not self._is_valid_github_url(repo_url):
                raise ValueError("URL GitHub invalide. Format attendu: https://github.com/username/repo")
            
            # Récupérer les informations de base
            repo_info = self._get_repo_info(repo_url)
            if not repo_info:
                raise ValueError("Impossible de récupérer les informations du dépôt")
            
            # Analyser le code
            code_analysis = self._analyze_code(repo_url)
            
            # Combiner les résultats
            result = {
                "basic_info": repo_info,
                "code_analysis": code_analysis,
                "analyzed_at": datetime.now().isoformat()
            }
            
            return result
            
        except GithubException as e:
            print(f"Erreur GitHub: {str(e)}")
            raise
        except Exception as e:
            print(f"Erreur lors de l'analyse du dépôt: {str(e)}")
            raise

    def _is_valid_github_url(self, url: str) -> bool:
        """Vérifie si l'URL est une URL GitHub valide"""
        if not url:
            return False
        parts = url.split("/")
        return (url.startswith("https://github.com/") and 
                len(parts) >= 5 and 
                parts[3] and parts[4])

    def _get_repo_info(self, repo_url: str) -> Dict[str, Any]:
        """Récupère les informations de base du dépôt"""
        try:
            # Extraire le nom d'utilisateur et le nom du repo de manière sécurisée
            parts = repo_url.split("github.com/")[1].split("/")
            if len(parts) < 2:
                raise ValueError("Format d'URL invalide")
                
            username, repo_name = parts[0], parts[1]
            repo = self.github.get_repo(f"{username}/{repo_name}")
            
            return {
                "name": repo.name,
                "description": repo.description or "Pas de description",
                "stars": repo.stargazers_count,
                "languages": list(repo.get_languages().keys()),
                "readme": self._get_readme_content(repo)
            }
        except GithubException as e:
            print(f"Erreur GitHub API: {str(e)}")
            return {}
        except Exception as e:
            print(f"Erreur lors de la récupération des informations: {str(e)}")
            return {}

    def _analyze_code(self, repo_url: str) -> Dict[str, Any]:
        """Analyse le code source du projet"""
        temp_dir = None
        try:
            temp_dir = tempfile.mkdtemp(prefix="github_analysis_")
            self._clone_repo(repo_url, temp_dir)
            
            search_tool = DirectorySearchTool(
                directory=temp_dir,
                name="Analyse du code source",
                description="Analyse le contenu du code source pour extraire les informations pertinentes",
                summarize=True,  # Activer la résumé automatique
                result_as_answer=True  # Retourner le résultat comme une réponse structurée
            )
            
            # Créer le prompt pour l'analyse
            prompt = PromptTemplate(
                template="""Analysez ce code et donnez une description simple du projet.
                Incluez:
                - Une description courte
                - Les fonctionnalités principales
                - Les technologies utilisées
                - Le niveau de difficulté
                
                Code:
                {context}
                """,
                input_variables=["context"]
            )
            
            # Analyser le code en utilisant la méthode run
            result = search_tool.run(
                input="Analysez le code source pour comprendre la structure et les fonctionnalités du projet"
            )
            
            if not result:
                return {"error": "Aucun code trouvé à analyser"}
                
            analysis = self.llm.invoke(prompt.format(context=result))
            return {"analysis": analysis.content}
            
        except Exception as e:
            print(f"Erreur lors de l'analyse du code: {str(e)}")
            return {"error": str(e)}
        finally:
            if temp_dir and os.path.exists(temp_dir):
                self._cleanup_repo(temp_dir)

    def _clone_repo(self, repo_url: str, target_dir: str) -> None:
        """Clone le dépôt dans un dossier temporaire de manière sécurisée"""
        try:
            os.system(f'git clone --depth 1 {repo_url} "{target_dir}"')
            if not os.path.exists(target_dir):
                raise ValueError("Le clonage a échoué")
        except Exception as e:
            print(f"Erreur lors du clonage du dépôt: {str(e)}")
            raise

    def _cleanup_repo(self, path: str) -> None:
        """Supprime le dépôt temporaire de manière sécurisée"""
        try:
            if os.path.exists(path):
                shutil.rmtree(path)
        except Exception as e:
            print(f"Erreur lors du nettoyage du dossier temporaire: {str(e)}")

    def _get_readme_content(self, repo) -> str:
        """Récupère le contenu du README de manière sécurisée"""
        try:
            readme = None
            for file in repo.get_contents(""):
                if file.name.lower().startswith("readme"):
                    readme = file
                    break
            
            if readme:
                content = readme.decoded_content.decode('utf-8')
                return content[:5000]  # Limiter la taille pour éviter les problèmes de mémoire
            else:
                return "Pas de README trouvé dans ce dépôt"
                
        except GithubException as e:
            print(f"Erreur GitHub API lors de la lecture du README: {str(e)}")
            return "Impossible de lire le README"
        except Exception as e:
            print(f"Erreur lors de la lecture du README: {str(e)}")
            return "Impossible de lire le README"