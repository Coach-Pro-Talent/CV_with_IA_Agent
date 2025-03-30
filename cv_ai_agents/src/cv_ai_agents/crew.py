from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from cv_ai_agents.tools.github_tool import GitHubAnalyzerTool
from crewai_tools import (
    FileWriterTool,
    FileReadTool

)
from typing import List

from .models import (
    ProjectAnalysis,
    SelectedProject,
    TrainingRecommendation,
    ProjectAnalysisList,
    SelectedProjectList,
    TrainingRecommendationList,
    CVContent
)
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class CvAiAgents():
    """CvAiAgents crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def github_analyst(self) -> Agent:
        """Agent d'analyse des projets GitHub."""
        return Agent(
            config=self.agents_config['github_analyst'],
            llm=LLM('o1'),
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
            llm=LLM('o1'),
            tools=[FileReadTool()],
            verbose=True
        )

    @agent
    def learning_recommender(self) -> Agent:
        """Agent de recommandation de formations."""
        return Agent(
            config=self.agents_config['learning_recommender'],
            llm=LLM('o1'),
            tools=[FileReadTool()],
            verbose=True
        )

    @agent
    def cv_generator(self) -> Agent:
        """Agent de génération de CV."""
        return Agent(
            config=self.agents_config['cv_generator'],
            llm=LLM('o1'),
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
            output_pydantic=ProjectAnalysisList,
            output_file="output/projects_analysis.json"
            
        )

    @task
    def select_best_projects(self) -> Task:
        """Sélection des meilleurs projets."""
        return Task(
            config=self.tasks_config['select_best_projects'],
            output_pydantic=SelectedProjectList,
            output_file="output/selected_projects.json",
            context=[self.analyze_projects]
        )

    @task
    def provide_recommendations(self) -> Task:
        """Recommandations de formations."""
        return Task(
            config=self.tasks_config['provide_recommendations'],
            output_pydantic=TrainingRecommendationList,
            output_file="output/recommendations.json",
            context=[self.select_best_projects]
        )

    @task
    def generate_cv(self) -> Task:
        """Génération du CV."""
        return Task(
            config=self.tasks_config['generate_cv'],
            output_pydantic=CVContent,
            output_file="output/cv.md",
            context = [self.provide_recommendations]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the CvAiAgents crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
