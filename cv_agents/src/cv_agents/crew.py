from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from cv_agents.tools.github_tool import GitHubAnalyzerTool
from crewai_tools import FileReadTool, FileWriterTool
from dotenv import load_dotenv
import json
import os

@CrewBase
class CvAgents:
    """Crew pour l'analyse de portfolio GitHub et la génération de CV."""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        load_dotenv()
        self.llm = LLM(
            model=os.getenv("MODEL_NAME", "deepseek-coder-33b-instruct"),
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url=os.getenv("DEEP_SEEK_BASE")
        )

    @before_kickoff
    def before_kickoff(self):
        """Validation des inputs et création des dossiers."""
        required_inputs = ["username", "job_description", "number_project"]
        for input_name in required_inputs:
            if not hasattr(self.inputs, input_name):
                raise ValueError(f"Input manquant: {input_name}")
        
        os.makedirs("output", exist_ok=True)

    @agent
    def github_analyst(self) -> Agent:
        """Agent d'analyse des projets GitHub."""
        return Agent(
            config=self.agents_config['github_analyst'],
            llm=self.llm,
            tools=[
                GitHubAnalyzerTool(github_token=os.getenv("GITHUB_TOKEN")),
                FileWriterTool()
            ],
            verbose=True
        )

    @agent
    def project_selector(self) -> Agent:
        """Agent de sélection des meilleurs projets."""
        return Agent(
            config=self.agents_config['project_selector'],
            llm=self.llm,
            tools=[FileReadTool()],
            verbose=True
        )

    @agent
    def learning_recommender(self) -> Agent:
        """Agent de recommandation de formations."""
        return Agent(
            config=self.agents_config['learning_recommender'],
            llm=self.llm,
            tools=[FileReadTool()],
            verbose=True
        )

    @agent
    def cv_generator(self) -> Agent:
        """Agent de génération de CV."""
        return Agent(
            config=self.agents_config['cv_generator'],
            llm=self.llm,
            tools=[
                FileWriterTool(),
                FileReadTool()
            ],
            verbose=True
        )

    @task
    def analyze_projects(self) -> Task:
        """Analyse des projets GitHub."""
        return Task(
            config=self.tasks_config['analyze_projects'],
            context={
                "username": self.inputs.username,
                "number_projects": self.inputs.number_project,
                "job_description": self.inputs.job_description,
                "output_file": "output/projects_analysis.json"
            }
        )

    @task
    def select_best_projects(self) -> Task:
        """Sélection des meilleurs projets."""
        return Task(
            config=self.tasks_config['select_best_projects'],
            context={
                "input_file": "output/projects_analysis.json",
                "job_description": self.inputs.job_description,
                "output_file": "output/selected_projects.json"
            },
            dependencies=["analyze_projects"]
        )

    @task
    def provide_recommendations(self) -> Task:
        """Recommandations de formations."""
        return Task(
            config=self.tasks_config['provide_recommendations'],
            context={
                "input_file": "output/selected_projects.json",
                "job_description": self.inputs.job_description,
                "output_file": "output/recommendations.json"
            },
            dependencies=["select_best_projects"]
        )

    @task
    def generate_cv(self) -> Task:
        """Génération du CV."""
        return Task(
            config=self.tasks_config['generate_cv'],
            context={
                "projects_file": "output/selected_projects.json",
                "recommendations_file": "output/recommendations.json",
                "job_description": self.inputs.job_description,
                "user_info": self.inputs.user_info,
                "output_file": "output/cv.md"
            },
            dependencies=["select_best_projects", "provide_recommendations"]
        )

    @crew
    def crew(self) -> Crew:
        """Configuration du crew."""
        return Crew(
            agents=[
                self.github_analyst(),
                self.project_selector(),
                self.learning_recommender(),
                self.cv_generator()
            ],
            tasks=[
                self.analyze_projects(),
                self.select_best_projects(),
                self.provide_recommendations(),
                self.generate_cv()
            ],
            process=Process.sequential,
            verbose=True
        )