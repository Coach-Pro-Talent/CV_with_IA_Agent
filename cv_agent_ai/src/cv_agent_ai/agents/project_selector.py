from typing import Dict, Any, List
from crewai import Agent
from cv_agent_ai.tools.project_selection_tool import ProjectSelectionTool

class ProjectSelectorAgent:
    """Agent responsable de la sélection des meilleurs projets en fonction d'une description de poste"""
    
    def __init__(self):
        """Initialise l'agent de sélection de projets"""
        self.tool = ProjectSelectionTool()
        self.agent = Agent(
            role="Project Selector",
            goal="Sélectionner les projets les plus pertinents pour un poste donné",
            backstory="Expert en analyse de projets et en évaluation de leur pertinence pour différents postes",
            tools=[self.tool],
            verbose=True
        )

    def select_projects(self, 
                       projects_data: List[Dict[str, Any]], 
                       job_description: str, 
                       num_projects: int = 3) -> Dict[str, Any]:
        """Sélectionne les meilleurs projets en fonction de la description du poste"""
        try:
            # Utiliser l'outil de sélection pour obtenir les résultats
            result = self.tool.select_best_projects(
                projects_data=projects_data,
                job_description=job_description,
                num_projects=num_projects
            )
            
            return result
        except Exception as e:
            print(f"Erreur lors de la sélection des projets: {str(e)}")
            return {"error": str(e)} 