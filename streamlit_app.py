import streamlit as st
import time
from crew import cv_launch


st.markdown(
    "<h1 style='text-align: center; color: orange;font-weight:bold'>🚀 ZTF - Sélection des Meilleurs Projets</h1>",
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
    with open("knowledge/user_preferences.txt", "w") as file:
        file.write(user_description)
        file.close()
    with st.spinner("🧠 Réflexion des agents en cours..."):
        time.sleep(1)
        result = cv_launch.kickoff(inputs=launch_details)

    if result:
        st.success("🎉 Analyse terminée ! Voici vos résultats 👇")

        if result:
            with open("ouput/recommendations.json", "rb") as rec_file:
                st.download_button(
                    label="📥 Télécharger les recommandations",
                    data=rec_file,
                    file_name="recommandations.json",
                    mime="text/plain"
                )

            with open("ouput/report.md", "rb") as report_file:
                st.download_button(
                    label="📄 Télécharger le rapport CV",
                    data=report_file,
                    file_name="mon_cv_parfait.txt",
                    mime="text/plain"
                )
        else:
            st.warning("Les fichiers de résultats n'ont pas pu être générés correctement.")
    else:
        st.error("❌ Une erreur est survenue pendant l'exécution.")
else:
    if not inputs_ready:
        st.info("Veuillez remplir les champs requis pour activer le bouton.")
