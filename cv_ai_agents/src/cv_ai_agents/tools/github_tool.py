from crewai.tools import BaseTool



class GithubTool(BaseTool):
    name: str = "Recuperer les informations sur les repositories d'un candidat"
    description: str =(
            "Recuperer les informations sur les repositories en prenant en paramètres le token de l'utilisateur"
    )

    def get_readme_content(repo):
        try:
            contents = repo.get_contents("README.md")
            return contents.decoded_content.decode()
        except Exception as e:
            return None


    def __run(self, token):
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