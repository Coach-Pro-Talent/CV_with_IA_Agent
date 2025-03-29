from crewai import Agent, Crew, Process, Task, LLM
import json
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from cv_agent_ai.tools.github_tool import GitHubAnalyzerTool
from dotenv import load_dotenv
import os
from typing import List, Dict, Any
from datetime import datetime
from pathlib import Path

# Charger les variables d'environnement
load_dotenv()

@CrewBase
class CvAgentAi():
    """CvAgentAi crew pour l'analyse de projets et la génération de CV"""

    def __init__(self):
        """Initialisation de la crew avec les configurations nécessaires"""
        # Chemins des fichiers de configuration
        self.agents_config = str(Path(__file__).parent / 'config/agents.yaml')
        self.tasks_config = str(Path(__file__).parent / 'config/tasks.yaml')
        
        # Initialisation du LLM
        self.llm = LLM(
            model="deepseek-coder-33b-instruct",
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url=os.getenv("DEEPSEEK_API_BASE")
        )
        
        # Création du dossier output s'il n'existe pas
        self.output_dir = Path(__file__).parent / 'output'
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialisation des préférences utilisateur (sera chargé dans before_kickoff)
        self.user_preferences = None

    @before_kickoff
    def before_kickoff(self):
        """Préparation avant le lancement de la crew"""
        try:
            print("Chargement des préférences utilisateur...")
            self.user_preferences = load_user_preferences()
            print(f"Préférences chargées pour {self.user_preferences.full_name}")

            print("Récupération des projets GitHub...")
            github_analyzer = GitHubAnalyzerTool(github_token=os.getenv("GITHUB_TOKEN"))
            result = github_analyzer._run(self.user_preferences.github)

            # Sauvegarde des résultats
            output_file = self.output_dir / "projects_info.json"
            with open(output_file, "w", encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)

            print(f"Récupération des projets GitHub effectuée avec succès : {output_file}")
            
        except Exception as e:
            print(f"Erreur lors de l'initialisation : {str(e)}")
            raise

    @agent
    def project_analyzer(self) -> Agent:
        """Agent pour l'analyse des projets"""
        return Agent(
            config=self.agents_config['project_analyzer'],
            llm=self.llm,
            context=f"Analyse des projets pour {self.user_preferences.full_name}, "
                   f"rôle souhaité: {self.user_preferences.desired_role}, "
                   f"technologies préférées: {', '.join(self.user_preferences.preferred_technologies)}"
        )

    @agent
    def learning_recommender(self) -> Agent:
        """Agent pour les recommandations d'apprentissage"""
        return Agent(
            config=self.agents_config['learning_recommender'],
            llm=self.llm,
        )

    @agent
    def cv_generator(self) -> Agent:
        """Agent pour la génération de CV"""
        return Agent(
            config=self.agents_config['cv_generator'],
            llm=self.llm,
    
        )
    
    @task
    def analyze_projects(self) -> Task:
        """Tâche d'évaluation des projets"""
        return Task(
            config=self.tasks_config['evaluate_projects']
        )

    @task
    def generate_cv(self) -> Task:
        """Tâche de génération du CV"""
        return Task(
            config=self.tasks_config['cv_generator'],
            
        )

    @task
    def recommend_learning(self) -> Task:
        """Tâche de recommandation d'apprentissage"""
        return Task(
            config=self.tasks_config['give_recommendations'],
           
        )

    @crew
    def crew(self) -> Crew:
        """Configuration de la crew"""
        return Crew(
            agents=self.agents, 
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
