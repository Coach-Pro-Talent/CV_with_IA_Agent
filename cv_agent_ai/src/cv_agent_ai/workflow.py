from typing import Dict, Any, List
import yaml
from pathlib import Path
from .tools.github_tool import GitHubAnalyzer
from .tools.project_evaluation_tool import ProjectEvaluationTool
from .tools.cv_analysis_tool import CVAnalysisTool

class WorkflowManager:
    """Gestionnaire de workflow pour coordonner les agents"""
    
    def __init__(self, config_path: str, github_token: str):
        """Initialise le gestionnaire de workflow"""
        self.config = self._load_config(config_path)
        self.github_token = github_token
        self.tools = self._initialize_tools()
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Charge la configuration des agents"""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
            
    def _initialize_tools(self) -> Dict[str, Any]:
        """Initialise les outils nécessaires"""
        return {
            'github_analyzer': GitHubAnalyzer(self.github_token),
            'project_evaluator': ProjectEvaluationTool(self.github_token),
            'cv_analyzer': CVAnalysisTool(self.github_token)
        }
        
    def process_repositories(self, repo_urls: List[str], cv_content: str = None) -> Dict[str, Any]:
        """Traite les dépôts GitHub en suivant le workflow défini"""
        try:
            # 1. Analyse GitHub
            github_results = []
            for repo_url in repo_urls:
                result = self.tools['github_analyzer'].analyze_repository(repo_url)
                github_results.append(result)
                
            # 2. Évaluation des projets
            project_evaluations = self.tools['project_evaluator'].evaluate_multiple_projects(repo_urls)
            
            # 3. Analyse du CV si fourni
            cv_analysis = None
            if cv_content:
                cv_analysis = self.tools['cv_analyzer'].analyze_cv(repo_urls, cv_content)
                
            # 4. Combiner les résultats
            final_results = {
                'github_analysis': github_results,
                'project_evaluations': project_evaluations,
                'cv_analysis': cv_analysis,
                'workflow_status': 'completed'
            }
            
            return final_results
            
        except Exception as e:
            print(f"Erreur lors du traitement des dépôts: {str(e)}")
            return {
                'error': str(e),
                'workflow_status': 'failed'
            }
            
    def get_agent_config(self, agent_name: str) -> Dict[str, Any]:
        """Récupère la configuration d'un agent spécifique"""
        return self.config['agents'].get(agent_name, {})
        
    def get_next_agent(self, current_agent: str) -> str:
        """Détermine le prochain agent dans le workflow"""
        agent_config = self.get_agent_config(current_agent)
        return agent_config.get('next_agent') 