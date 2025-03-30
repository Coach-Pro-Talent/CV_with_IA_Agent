from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from tools.github_tool import GitHubAnalyzerTool
from dotenv import load_dotenv

import os





@CrewBase
class CvAgents():
    """CvAgents crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    llm = LLM(
        model="deepseek-coder-33b-instruct",
        api_key = os.getenv("DEEPSEEK_API_KEY"),
        base_url = os.getenv("DEEP_SEEK_BASE")
    )

    @before_kickoff
    def before_kickoff(self):
        try:
            print("Recuperation des repos de l'utilisateur")
          
            github_analyzer = GitHubAnalyzerTool(github_token=os.getenv("GITHUB_TOKEN"))
            result =  github_analyzer._run(username=self.inputs.username, number_project=self.inputs.number_project)

            output_file = "projects_info.json"
            with open(output_file, encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"Récupération des projets Github effectuée avec succès : {output_file}")
        except Exception as e:
            print(f"Erreur lors de l'initialisation : {str(e)}")

    @agent
    def project_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['project_analyzer'],
            verbose=True
        )

    @agent
    def cv_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['cv_generator'],
            verbose=True
        )

    @agent
    def learning_recommender(self) -> Agent:
        return Agent(
            config=self.agents_config['learning_recommender'],
            verbose=True
        )


    @task
    def analyze_projects(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_projects'],
        )


    @task
    def give_recommandations(self) -> Task:
        return Task(
            config=self.tasks_config['give_recommandations'],
            output_file='report.md'
        )

    @task
    def generate_cv(self) -> Task:
        return Task(
            config=self.tasks_config['generate_cv'],
            output_file='report.md'
        )
    @crew
    def crew(self) -> Crew:
        """Creates the CvAgents crew"""
      

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
