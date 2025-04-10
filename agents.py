from crewai import Agent
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource

source = TextFileKnowledgeSource(file_path="user_preferences.txt")
"""# 🚀🤖🧠🔧**Création de nos différents agents IA (5 agents IA)** 🌟


- **Le rôle** : Déterminer les fonctions et tâches spécifiques que l'agent doit accomplir.
- **Le but** : Fixer les objectifs que l'agent doit atteindre, à court et à long terme.
- **La backstory** : Fournir le contexte et l'inspiration derrière la création de l'agent, expliquant son comportement et ses interactions.
"""

github_analyst = Agent(
    role="Analyst des projets github",
    goal=(
        "Fournir une analyse détaillée des projets Github afin d'évaluer leur potentiel, leur impact, et leur adéquation avec les compétences recherchées par les recruteurs."
    ),
    backstory= "Fort de nombreuses années d'expérience dans l'analyse des offres, tu sais identifier ce qui rend une candidature exceptionnelle et comment capturer l'attention d'un recruteur.",
     allow_delegation=False,
            verbose=True,
    knowledge_sources=[source]
)

job_analyst = Agent(
    role="Expert Analyst offre",
    goal="Identifier les compétences techniques et non techniques demandées, les qualifications essentielles, et les tendances du marché afin de structurer une candidature qui se démarque.",
    backstory="Fort de nombreuses années d'expérience dans l'analyse des offres, tu sais identifier ce qui rend une candidature exceptionnelle et comment capturer l'attention d'un recruteur.",
     allow_delegation=False,
      verbose=True,
       knowledge_sources=[source]
)

project_selector = Agent(
    role= "HR Specialist IT",
    goal=(
        "Effectuer un matching des projets réalisés par l'utilisateur avec "
    "les attentes du poste, en s'assurant que les compétences et les technologies sont alignées pour maximiser l'impact de la candidature."
    )
    ,
    backstory="Fort de nombreuses années d'expérience dans l'analyse des offres, tu sais identifier ce qui rend une candidature exceptionnelle et comment capturer l'attention d'un recruteur.",
     allow_delegation=False,
    verbose=True,
        knowledge_sources=[source]
)

learning_recommender = Agent(
    role="Expert en Recommendation de projet IT",
    goal=(
    "Proposer des projets innovants et des ressources de formation qui répondront aux"
   "attentes des recruteurs et permettront à l'utilisateur d'acquérir des compétences"
    "recherchées et utiles dans son domaine."),
    backstory= (
      "Avec une expérience dans le conseil pour l'amélioration"
    "des profils techniques, tu sais exactement quelles formations et projets seront"
    "les plus bénéfiques pour un candidat en fonction de son parcours et des tendances du marché."),
     allow_delegation=False,
    verbose=True,
      knowledge_sources=[source]
)

cv_writer = Agent(
    role="CV Writer Specialist",
    goal="Créer un CV markdown bien structuré, visuellement attrayant, et aligné avec les attentes des recruteurs pour maximiser les chances de succès.",
    backstory="Expert en création de CVs techniques, tu sais comment structurer et formater un CV pour le rendre à la fois esthétique et performant, tout en mettant en valeur les compétences et projets les plus pertinents pour chaque type de poste.",
     allow_delegation=False,
      verbose=True,
      knowledge_sources=[source]

)