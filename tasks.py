from crewai import Task

def create_tasks(github_agent, analysis_agent, selection_agent, recommendation_agent, cv_agent):
    # Tâche de récupération GitHub
    github_task = Task(
        description="""Analyser les dépôts GitHub de l'étudiant :
        1. Récupérer tous les projets publics
        2. Analyser les README et fichiers clés
        3. Extraire les technologies utilisées
        4. Identifier les contributions significatives
        5. Créer un catalogue structuré des projets""",
        agent=github_agent
    )

    # Tâche d'analyse et notation
    analysis_task = Task(
        description="""Évaluer chaque projet selon les critères suivants :
        1. Complexité technique
        2. Pertinence par rapport au poste visé
        3. Innovation et créativité
        4. Impact et résultats
        5. Qualité du code et documentation
        Attribuer une note sur 10 pour chaque critère""",
        agent=analysis_agent
    )

    # Tâche de sélection
    selection_task = Task(
        description="""Sélectionner les meilleurs projets :
        1. Filtrer selon les notes obtenues
        2. Adapter aux préférences de l'utilisateur
        3. Assurer une diversité des compétences
        4. Prioriser les projets les plus pertinents
        5. Créer des descriptions détaillées""",
        agent=selection_agent
    )

    # Tâche de recommandation
    recommendation_task = Task(
        description="""Recommander des formations et certifications :
        1. Analyser les compétences actuelles
        2. Identifier les lacunes
        3. Proposer des formations pertinentes
        4. Suggérer des certifications valorisées
        5. Créer un plan de développement""",
        agent=recommendation_agent
    )

    # Tâche de génération de CV
    cv_task = Task(
        description="""Générer un CV en Markdown :
        1. Structurer les informations
        2. Mettre en valeur les projets sélectionnés
        3. Intégrer les recommandations
        4. Optimiser pour les ATS
        5. Créer une version professionnelle""",
        agent=cv_agent
    )

    return [github_task, analysis_task, selection_task, recommendation_task, cv_task] 