from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from cv_agents.tools.github_tool import GitHubAnalyzerTool
from crewai_tools import (
    DirectorySearchTool,
    FileReadTool,
    FileWriteTool,
    CodeDocsRAGSearch,
    BraveSearch,
    RAGTool,
    JSONRAGSearch,
    WebsiteRAGSearch,
    ScrapeflyScrapeTool,
    MDXRAGSearch
)
from dotenv import load_dotenv
import json
import os

@CrewBase
class CvAgents:
    """
    Crew pour l'analyse de portfolio GitHub et la génération de CV.
    Utilise DeepSeek pour l'analyse et la génération de contenu.
    """

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        load_dotenv()
        self.llm = LLM(
            model="deepseek-coder-33b-instruct",
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url=os.getenv("DEEP_SEEK_BASE")
        )
        self.github_tool = GitHubAnalyzerTool(github_token=os.getenv("GITHUB_TOKEN"))

    @before_kickoff
    def before_kickoff(self):
        """
        Exécuté avant le démarrage du crew.
        Récupère et analyse les projets GitHub de l'utilisateur.
        """
        try:
            print("📊 Analyse des repositories GitHub en cours...")
            
            result = self.github_tool._run(
                username=self.inputs.username,
                max_repos=self.inputs.number_project
            )

            # Sauvegarde des résultats
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, "projects_info.json")
            
            with open(output_file, 'w', encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Analyse GitHub complétée : {output_file}")
            
        except Exception as e:
            print(f"❌ Erreur lors de l'analyse GitHub : {str(e)}")
            raise

    @agent
    def github_analyst(self) -> Agent:
        """Agent d'analyse des projets GitHub."""
        return Agent(
            config=self.agents_config['github_analyst'],
            llm=self.llm,
            tools=[
                self.github_tool,
                DirectorySearchTool(),
                FileReadTool(),
                CodeDocsRAGSearch()
            ],
            verbose=True
        )

    @agent
    def project_selector(self) -> Agent:
        """Agent de sélection des meilleurs projets."""
        return Agent(
            config=self.agents_config['project_selector'],
            llm=self.llm,
            tools=[
                self.github_tool,
                BraveSearch(),
                RAGTool(),
                JSONRAGSearch()
            ],
            verbose=True
        )

    @agent
    def learning_recommender(self) -> Agent:
        """Agent de recommandation de formations."""
        return Agent(
            config=self.agents_config['learning_recommender'],
            llm=self.llm,
            tools=[
                BraveSearch(),
                WebsiteRAGSearch(),
                ScrapeflyScrapeTool(),
                JSONRAGSearch()
            ],
            verbose=True
        )

    @agent
    def cv_generator(self) -> Agent:
        """Agent de génération de CV."""
        return Agent(
            config=self.agents_config['cv_generator'],
            llm=self.llm,
            tools=[
                FileWriteTool(),
                DirectoryRAGSearch(),
                MDXRAGSearch(),
                JSONRAGSearch()
            ],
            verbose=True
        )

    @task
    def analyze_projects(self) -> Task:
        """Tâche d'analyse des projets GitHub."""
        return Task(
            config=self.tasks_config['analyze_projects'],
            context={
                "input_file": "output/projects_info.json",
                "job_description": self.inputs.job_description
            }
        )

    @task
    def select_best_projects(self) -> Task:
        """Tâche de sélection des meilleurs projets."""
        return Task(
            config=self.tasks_config['select_best_projects'],
            context={
                "job_description": self.inputs.job_description,
                "number_projects": self.inputs.number_project
            },
            dependencies=["analyze_projects"]
        )

    @task
    def provide_recommendations(self) -> Task:
        """Tâche de recommandation de formations."""
        return Task(
            config=self.tasks_config['provide_recommendations'],
            context={
                "job_description": self.inputs.job_description
            },
            dependencies=["select_best_projects"]
        )

    @task
    def generate_cv(self) -> Task:
        """Tâche de génération du CV."""
        return Task(
            config=self.tasks_config['generate_cv'],
            context={
                "job_description": self.inputs.job_description,
                "user_info": self.inputs.user_info
            },
            dependencies=["select_best_projects", "provide_recommendations"]
        )

    @crew
    def crew(self) -> Crew:
        """Configure et retourne le crew complet."""
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
