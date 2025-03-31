#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from cv_ai_agents.crew import CvAiAgents

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'nombre_projet': 2,
               'job_description': """
                                          job_requirement:
                                    title: >
                                      Ruby on Rails and React Engineer
                                    description: >
                                      We are seeking a skilled Ruby on Rails and React engineer to join our team.
                                      The ideal candidate will have experience in both backend and frontend development,
                                      with a passion for building high-quality web applications.

                                    responsibilities: >
                                      - Develop and maintain web applications using Ruby on Rails and React.
                                      - Collaborate with teams to define and implement new features.
                                      - Write clean, maintainable, and efficient code.
                                      - Ensure application performance and responsiveness.
                                      - Identify and resolve bottlenecks and bugs.

                                    requirements: >
                                      - Proven experience with Ruby on Rails and React.
                                      - Strong understanding of object-oriented programming.
                                      - Proficiency with JavaScript, HTML, CSS, and React.
                                      - Experience with SQL or NoSQL databases.
                                      - Familiarity with code versioning tools, such as Git.

                                    preferred_qualifications: >
                                      - Experience with cloud services (AWS, Google Cloud, or Azure).
                                      - Familiarity with Docker and Kubernetes.
                                      - Knowledge of GraphQL.
                                      - Bachelor's degree in Computer Science or a related field.

                                    perks_and_benefits: >
                                      - Competitive salary and bonuses.
                                      - Health, dental, and vision insurance.
                                      - Flexible working hours and remote work options.
                                      - Professional development opportunities.
                                          """,
               'github_token':''
    }
    
    try:
        CvAiAgents().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'nombre_projet': 2,
                       'job_description': """
                                                  job_requirement:
                                            title: >
                                              Ruby on Rails and React Engineer
                                            description: >
                                              We are seeking a skilled Ruby on Rails and React engineer to join our team.
                                              The ideal candidate will have experience in both backend and frontend development,
                                              with a passion for building high-quality web applications.

                                            responsibilities: >
                                              - Develop and maintain web applications using Ruby on Rails and React.
                                              - Collaborate with teams to define and implement new features.
                                              - Write clean, maintainable, and efficient code.
                                              - Ensure application performance and responsiveness.
                                              - Identify and resolve bottlenecks and bugs.

                                            requirements: >
                                              - Proven experience with Ruby on Rails and React.
                                              - Strong understanding of object-oriented programming.
                                              - Proficiency with JavaScript, HTML, CSS, and React.
                                              - Experience with SQL or NoSQL databases.
                                              - Familiarity with code versioning tools, such as Git.

                                            preferred_qualifications: >
                                              - Experience with cloud services (AWS, Google Cloud, or Azure).
                                              - Familiarity with Docker and Kubernetes.
                                              - Knowledge of GraphQL.
                                              - Bachelor's degree in Computer Science or a related field.

                                            perks_and_benefits: >
                                              - Competitive salary and bonuses.
                                              - Health, dental, and vision insurance.
                                              - Flexible working hours and remote work options.
                                              - Professional development opportunities.
                                                  """,
                       'github_token':''
    }
    try:
        CvAiAgents().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        CvAiAgents().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")