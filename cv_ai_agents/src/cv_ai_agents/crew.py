from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
from crewai_tools import (
    TXTSearchTool,
    FileReadTool,
    FileWriterTool,
    ScrapeWebsiteTool,
    SerperDevTool
)
from cv_ai_agents.tools.github_tool import GithubTool

@CrewBase
class CvAiAgents():
    """CvAiAgents crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    text_source = TextFileKnowledgeSource(
        file_paths=["user_preference.txt"]
    )

    @agent
    def github_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['github_analyst'],
            allow_delegation=False,
            verbose=True,
            tools=[FileReadTool(), GithubTool()]
        )

    @agent
    def job_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['job_analyst'],
            allow_delegation=False,
            verbose=True,
            tools=[FileWriterTool()]
        )

    @agent
    def project_selector(self) -> Agent:
        return Agent(
            config=self.agents_config['project_selector'],
            allow_delegation=False,
            verbose=True,
            tools=[FileWriterTool(), FileReadTool(), self.text_source]
        )

    @agent
    def learning_recommender(self) -> Agent:
        return Agent(
            config=self.agents_config["learning_recommender"],
            allow_delegation=False,
            verbose=True,
            tools=[FileWriterTool(), FileReadTool(), SerperDevTool(), ScrapeWebsiteTool(), self.text_source]
        )

    @agent
    def cv_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["cv_writer"],
            allow_delegation=False,
            verbose=True,
            tools=[FileReadTool(), FileWriterTool(), self.text_source]
        )

    # DEFINITION DES TASKS

    @task
    def recuperer_github_repo(self) -> Task:
        return Task(
            config=self.tasks_config['recuperer_github_repo'],
            agent=self.github_analyst
        )

    @task
    def analyser_offre(self) -> Task:
        return Task(
            config=self.tasks_config['analyser_offre'],
            agent=self.job_analyst
        )

    @task
    def selectionner_meilleurs_projets(self) -> Task:
        return Task(
            config=self.tasks_config['selectionner_meilleurs_projets'],
            agent=self.project_selector,
            context=[self.analyser_offre(), self.recuperer_github_repo()]
        )

    @task
    def fournir_des_recommandations(self) -> Task:
        return Task(
            config=self.tasks_config['fournir_des_recommandations'],
            agent=self.learning_recommender,
            context=[self.analyser_offre(), self.selectionner_meilleurs_projets()]
        )

    @task
    def create_cv(self) -> Task:
        return Task(
            config=self.tasks_config['create_cv'],
            agent=self.cv_writer,
            output_file='report.md',
            context=[self.fournir_des_recommandations(), self.selectionner_meilleurs_projets()]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the CvAiAgents crew"""
        return Crew(
            agents=[self.github_analyst(), self.job_analyst(), self.project_selector(), self.learning_recommender(), self.cv_writer()],  # Automatically created by the @agent decorator
            tasks=[self.recuperer_github_repo(), self.analyser_offre(), self.selectionner_meilleurs_projets(), self.fournir_des_recommandations(), self.create_cv()],  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )