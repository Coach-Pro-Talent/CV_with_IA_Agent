import streamlit as st
import time
from crew import cv_launch
from dotenv import load_dotenv
from agents import github_analyst, job_analyst, project_selector, learning_recommender, cv_writer

load_dotenv()

st.markdown(
    "<h1 style='text-align: center; color: orange;font-weight:bold'>🚀 ZTF - CV Generator</h1>",
    unsafe_allow_html=True
)

st.markdown("Bienvenue dans l'assistant intelligent de sélection de projets. Configurez les paramètres ci-dessous 👇")

# --------- Inputs utilisateur ---------
num_projects = st.number_input("Nombre de projets à sélectionner", min_value=1, step=1, value=5)
job_description = st.text_area("🧠 Description du poste", placeholder="Décrivez ici le poste visé...")
user_description = st.text_area("👤 Votre profil", placeholder="Parlez un peu de vous, de vos compétences, intérêts...")

# Vérification que les champs requis sont remplis
inputs_ready = num_projects > 0 and job_description.strip() != ""

# Stocker les résultats
result = None

# Lancer le crew
if st.button("🚀 Lancer la sélection", disabled=not inputs_ready):

    launch_details = {
        "nombre_projet": num_projects,
        "job_description": job_description
    }

    # Enregistrer le profil utilisateur
    with open("knowledge/user_preferences.txt", "w", encoding="utf-8") as file:
        file.write(user_description)

    # Charger le contenu pour le passer aux agents via l’embedder
    with open("knowledge/user_preferences.txt", "r", encoding="utf-8") as f:
        user_knowledge = f.read()

    if user_knowledge.strip():
        documents = [user_knowledge]
        ids = ["user_profile_1"]

        try:
            # Upsert directement dans l'embedder utilisé par le crew
            cv_launch.embedder.upsert(ids=ids, documents=documents)
            st.success("✅ Connaissance utilisateur ajoutée avec succès aux agents.")
        except Exception as e:
            st.error(f"❌ Erreur pendant l'ajout de connaissance : {e}")
    else:
        st.warning("⚠️ Le profil utilisateur est vide. Aucune connaissance n’a été transmise.")

    with st.spinner("🧠 Réflexion des agents en cours..."):
        time.sleep(1)
        result = cv_launch.kickoff(inputs=launch_details)

    if result:
        st.success("🎉 Analyse terminée ! Voici vos résultats 👇")

        # Fichiers de sortie
        try:
            with open("output/recommendations.json", "rb") as rec_file:
                st.download_button(
                    label="📥 Télécharger les recommandations",
                    data=rec_file,
                    file_name="recommandations.json",
                    mime="application/json"
                )

            with open("output/report.md", "rb") as report_file:
                st.download_button(
                    label="📄 Télécharger le rapport CV",
                    data=report_file,
                    file_name="mon_cv_parfait.md",
                    mime="text/plain"
                )
        except FileNotFoundError:
            st.warning("Les fichiers de résultats n'ont pas pu être générés correctement.")
    else:
        st.error("❌ Une erreur est survenue pendant l'exécution.")
else:
    if not inputs_ready:
        st.info("Veuillez remplir les champs requis pour activer le bouton.")
