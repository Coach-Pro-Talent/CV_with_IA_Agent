from crewai import Agent, Crew, Process, Task, LLM
import json
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from cv_agent_ai.tools.github_tool import GitHubAnalyzerTool
from dotenv import load_dotenv
import os
from typing import List, Dict, Any
from datetime import datetime

# Charger les variables d'environnement
load_dotenv()

@CrewBase
class CvAgentAi():
    """CvAgentAi crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @before_kickoff
    def before_kickoff(self):
        print("Recuperation des projets github de l'utilisateur")

        url_repo = self.inputs['url_repo']
        github_analyzer = GitHubAnalyzerTool(github_token=os.getenv("GITHUB_TOKEN"))

        result = github_analyzer._run(url_repo)

        with open("output/projects_info.json", "w") as f:
            json.dump(result, f)

        print("Recuperation des projets github de l'utilisateur effectuée avec succès : le fichier output/projects_info.json a été créé")
 
    self.llm = LLM(
        model="deepseek-coder-33b-instruct",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url=os.getenv("DEEPSEEK_API_BASE")
    )

    @agent
    def project_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['project_analyzer'],
            llm=self.llm
        )

    @agent
    def learning_recommender(self) -> Agent:
        return Agent(
            config=self.agents_config['learning_recommender'],
            llm=self.llm
        )

    @agent
    def cv_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['cv_generator'],
            llm=self.llm
        )
    
    @task
    def evaluate_projects(self) -> Task:
        return Task(
            config=self.tasks_config['evaluate_projects'],
        )

    @task
    def cv_generator(self) -> Task:
        return Task(
            config=self.tasks_config['cv_generator'],
        )

    @task
    def learning_recommender(self) -> Task:
        return Task(
            config=self.tasks_config['give_recommender'],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents, 
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
