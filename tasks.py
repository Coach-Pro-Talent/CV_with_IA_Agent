from crewai import Task
from crewai_tools import FileReadTool, FileWriterTool, SerperDevTool,ScrapeWebsiteTool
from tools.github_tool import GithubTool
from agents import github_analyst,job_analyst,project_selector , learning_recommender, cv_writer


recuperer_github_repo = Task(
    description="""
                Récupérer et enrichir les informations des dépôts GitHub de l'utilisateur afin de mieux évaluer leur pertinence.
                Étapes :
                1. Utiliser `GithubTool` pour récupérer la liste des dépôts de l'utilisateur.
                2. Analyser et enrichir les données avec des informations supplémentaires :
                - Pertinence du projet
                - Fonctionnalités principales
                - Complexité du projet
                - Impact potentiel du projet
                - Technologies utilisées
                - Niveau de maturité (prototype, MVP, production)
                - Contributions majeures
                - Autres insights utiles
                3. Sauvegarder les résultats dans 'output/project_repo.json' en utilisant `FileWriterTool`.
    """,
    expected_output="""
                      Un fichier JSON contenant :
                            - name_repo : Nom du dépôt
                            - content_repo : Contenu du dépôt
                            - topics_repo : Thématiques associées
                            - description_repo : Description du dépôt
                            - languages_repo : Langages utilisés
                            - fonctionnalites_principales : Fonctionnalités clés
                            - pertinence_projet : Niveau de pertinence
                            - complexite_projet : Facile / Moyen / Avancé
                            - impact_projet : Évaluation de l'impact
                            - maturite_projet : Prototype / MVP / Production
                            - contributions_majeures : Contributions importantes au projet
                            - autres_informations : Autres insights utiles

    """,
       tools=[FileReadTool(), GithubTool()],
    agent = github_analyst,
    output_file="output/project_repo.json"
)

analyser_offre = Task(
    description= """
                    Analyser une offre d'emploi afin d'en extraire les éléments clés pour optimiser la candidature de l'utilisateur.

                    Étapes :
                    1. Lire et analyser la description du poste {job_description}.
                    2. Identifier les éléments essentiels :
                      - Hard skills requis
                      - Soft skills recherchés
                      - Exigences obligatoires (Must-have)
                      - Compétences appréciées (Nice-to-have)
                      - Opportunités et recommandations pour améliorer la candidature
                      - Niveau d'expérience recherché
                      - Secteur d'activité et tendances du marché
                    3. Sauvegarder les résultats dans 'output/job_description_synthetise.txt' en utilisant `FileWriterTool`.


    """,
    expected_output="""
                    Un fichier texte formaté contenant :
                          - Hardskills
                          - Softskills
                          - Must-have
                          - Nice-to-have
                          - Opportunités pour booster la candidature
                          - Points de vigilance et conseils
                          - Niveau d'expérience recommandé
                          - Tendances du marché et secteur d'activité


    """,
       tools=[FileWriterTool()],
    async_execution=True,
    agent = job_analyst,
    output_file="output/job_description_synthetise.txt"
)

selectionner_meilleurs_projets = Task(
    description="""
                    Identifier les projets les plus pertinents recuperer sur github en fonction des attentes du poste pour maximiser les chances de succès.

                        Étapes :
                        1. Lire le fichier 'output/job_description_synthetise.txt' pour extraire les exigences du poste (`FileReadTool`).
                        2. Lire le fichier 'output/project_repo.json' contenant les informations des projets (`FileReadTool`).
                        3. Effectuer un matching et sélectionner les {nombre_projet} projets les plus adaptés au poste mentionné dans la documentation.
                        4. Justifier chaque sélection avec des éléments concrets.
                        5. Analyser les écarts entre les compétences requises et les compétences projet.
                        6. Sauvegarder les résultats dans 'output/top_project.json' en utilisant `FileWriterTool`.

    """,
    expected_output= """

                    Un fichier JSON contenant :
                  - nom_projet : Nom du projet sélectionné
                  - description : Description détaillée du projet
                  - taches_principales : Liste des tâches principales (méthode STAR)
                  - pertinence_pour_le_poste : Justification du choix
                  - technologies_utilisees : Technologies principales du projet
                  - niveau_de_complexite : Facile / Moyen / Avancé
                  - ecarts_competences : Différences entre compétences projet et poste
                  - autres_informations : Autres insights pertinents

    """,
    context= [recuperer_github_repo, analyser_offre],
                tools=[FileWriterTool(), FileReadTool()],
    agent = project_selector

)

fournir_des_recommandations = Task(

      description=""""
                  Générer des recommandations de nouveau  projets innovant en et basant sur le background de l'utilisateur , de ses anciens projets et aussi des tendances du marché qui l'aidera à maximiser ses chances.

                      Étapes :
                      1. Lire `output/job_description_synthetise.txt` pour comprendre les attentes du poste (`FileReadTool`).
                      2. Lire `output/top_project.json` pour analyser les projets sélectionnés (`FileReadTool`).
                      3. Proposer des recommandations personnalisées en fonction des compétences de l'utilisateur et des tendances du marché.
                      4. Enrichir avec des ressources d’apprentissage (liens, formations, tutoriels, networking, etc.).
                      5. Sauvegarder les recommandations dans 'output/recommendations.json' en utilisant `FileWriterTool`.
                  Recommende de nouveau projet impactant (je ne veux pas ce qui ont déjà été relever)
                  Les projets que tu recommanderas doivent être bien detaillé
                   """,
      expected_output= """

                    Un fichier JSON contenant (bien detaille et explique) avec tous les projets ou chaque projet contient les informations suivantes :
                    - nom_projet : Nom du projet recommandé
                    - taches : Liste des tâches associées
                    - technologies : Technologies impliquées
                    - ressources_utiles : Liste de liens utiles pour approfondir les compétences
                    - opportunites_de_networking : Conférences, forums et événements pertinents

      """,
      context = [selectionner_meilleurs_projets, recuperer_github_repo, analyser_offre],
                  tools=[FileWriterTool(), FileReadTool(), SerperDevTool(), ScrapeWebsiteTool()],
      agent = learning_recommender,
      output_file='output/recommendations.json'
)


create_cv = Task(
  description= """
                Générer un CV technique optimisé en utilisant mes meilleurs projets selectionnés(github) et aussi l'analyse du poste.

                    Étapes :
                    1. Lire `output/top_project.json` pour récupérer les projets les plus pertinents (`FileReadTool`).
                    2. Structurer un CV technique attractif en Markdown avec icônes et mise en forme avancée.
                    3. Personnaliser le CV en fonction des attentes du poste.
                    4. Sauvegarder le CV dans 'output/cv_optimise.md'.
                    Le cv devra contenir juste les projets de l'utilisateur notamment les projets qui ont été récupéré ne rajoute pas d'autres

                   Rajoute des icones et des couleurs sur le rendu final
  """,

  expected_output="""
                Un fichier Markdown contenant (les projets doivent etre bien detaillés et surtour en respectant la methode STAR n'ajoute aucune informations qui ne t'a pas été fourni) :
                    - Informations personnelles de l'utilisateur en te basant sur la base de connaissance de l'utilisateur
                    - Résumé des compétences
                    - Projets pertinents pour le poste (tu renommera ses projets pertinents en 'Mes projets')
                    - Un Partie pour la formations (notamment ou la personne a frequenté):  si tu ne trouve pas cette partie dans ton analyse ne la met pas
                    - Certifications
                    - Soft skills qui matcheront le plus avec le poste
                    - Expériences mises en avant en lien avec le poste (je ne veux pas d'hallucinations inspire toi des données de l'utilisateur et enrichie juste)
                    - Présentation visuelle optimisée avec icônes et mise en forme avancée

  """,
  context = [fournir_des_recommandations, selectionner_meilleurs_projets, recuperer_github_repo, analyser_offre],
              tools=[FileReadTool(), FileWriterTool()],
  agent=cv_writer,
            output_file='output/report.md',
)
