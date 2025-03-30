#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from crew import CvAgents



def run():
    """
    Run the crew.
    """
    username  = input("Entrer votre username : ")
    number_project = int(input("Entrer votre nombre de  project à selectionner : "))
    job_description = input("La description du poste : ")

    inputs = {
        'username': username,
        'number_project':number_project,
        'job_description':job_description
    }
    
    try:
        CvAgents().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        CvAgents().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        CvAgents().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


if __name__=="__main__":
    run()