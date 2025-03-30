#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from cv_ai_agents.crew import CvAiAgents

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")






def run():
    """
    Run the crew.
    """
    
    inputs = {
         "username": "azeghaanicet",
        "number_project": 3,
        "job_description": "data analyst at Microsoft",
        "user_info": {
        "name": "anicet",
        "email": "anicet",
        "title": "data engineer",
        "linkedin": "anicetazegha",
        "location": "France"
        }
    }
    
    try:
        CvAiAgents().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")



if __name__=="__main__":
    run()