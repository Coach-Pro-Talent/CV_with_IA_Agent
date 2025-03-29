#!/usr/bin/env python
import os
import sys
import warnings
from crew import CvAgentAi
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew.
    """
    
    number_project = input("Combien de projets voulez vous pour votre porte folio : ")
    username = input("Entrez your username github : ")
    description_poste = input("Entrez la description du poste : ")

    inputs = {
        'nombre_projet': number_project,
        'username': username,
        'description_poste': description_poste
    }
    
    try:
        CvAgentAi().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


if __name__ == "__main__":
   run()
