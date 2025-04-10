from crewai import Crew
from agents import github_analyst, job_analyst, project_selector, learning_recommender, cv_writer
from tasks import recuperer_github_repo, analyser_offre, selectionner_meilleurs_projets, fournir_des_recommandations, create_cv



cv_launch = Crew(
    agents = [github_analyst, job_analyst, project_selector, learning_recommender, cv_writer],
    tasks = [recuperer_github_repo, analyser_offre, selectionner_meilleurs_projets, fournir_des_recommandations,create_cv ],
    verbose=True
)