#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from cv_agent_ai.crew import CvAgentAi

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew.
    """
    
    number_project = input("Combien de projets voulez vous pour votre porte folio : ")
    url_repo = input("Entrez l'url du repo github : ")
    description_poste = input("Entrez la description du poste : ")

    inputs = {
        'nombre_projet': nombre_projet,
        'url_repo': url_repo,
        'description_poste': description_poste
    }
    
    try:
        CvAgentAi().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'nombre_projet': nombre_projet,
        'url_repo': url_repo,
        'description_poste': description_poste
    }
    try:
        CvAgentAi().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        CvAgentAi().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'nombre_projet': nombre_projet,
        'url_repo': url_repo,
        'description_poste': description_poste
    }
    try:
        CvAgentAi().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    sys.exit(run())
