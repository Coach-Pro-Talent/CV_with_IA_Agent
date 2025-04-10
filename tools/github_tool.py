from pydantic import BaseModel
from crewai.tools import BaseTool
from github import Github, Auth
import os
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource



"""# 🛠️ 🔧 **Personnalisation de notre tool**

- **Importation des modules nécessaires** : Importer crewai.tools, pydantic, typing, et github.
- **Fonction get_readme_content** : Récupérer le contenu du fichier README.md d'un repository GitHub.
- **Modèle GithubToolInput** : Définir le champ obligatoire, token, pour l'authentification GitHub.
- **Classe GithubTool** : Définir l'outil pour récupérer les informations des repositories en utilisant le token utilisateur.
- **Méthode _run** : Authentifier via GitHub, récupérer les repositories et extraire les informations essentielles (contenu du README, sujets, description, langues) pour chaque repository, puis retourner les données collectées.
"""

"""
Il est question ici pour de récupérer le contenu de chaque repository
"""
def get_readme_content(repo):
        try:
            contents = repo.get_contents("README.md")
            return contents.decoded_content.decode()
        except Exception as e:
            return None


# class GithubToolInput(BaseModel):
#     """Input schema for MyCustomTool."""
#     token: str = Field(..., description="token github de l'utilisateur pour se connecter à son compte github et avoir accès à ses repositories")

class GithubTool(BaseTool):
    name: str = "Récupérer des informations sur les repositories d'un candidat"
    description: str =(
            "Recuperer les informations sur les repositories en prenant en paramètres le token de l'utilisateur"
    )

    # args_schema: Type[BaseModel] = GithubToolInput

    def _run(self):
        token = os.environ["GITHUB_TOKEN"]
        auth = Auth.Token(token)
        g = Github(auth=auth)
        result = []
        for repo in g.get_user().get_repos():
            readme_content = get_readme_content(repo)
            topics = repo.get_topics()
            description = repo.description
            languages = repo.get_languages()

            if readme_content:
                print(f"Processing repo : {repo.name}")
                data = {
                    "name": repo.name,
                    "content": readme_content,
                    "topics": topics,
                    "description": description,
                    "languages": languages
                }

                result.append(data)
        return result