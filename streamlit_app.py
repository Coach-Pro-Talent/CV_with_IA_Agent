import streamlit as st
import time
from crew import cv_launch
# --------- Mise en page ---------
st.markdown(
    "<h1 style='text-align: center; color: #4B8BBE;'>🚀 ZTF - Sélection des Meilleurs Projets</h1>",
    unsafe_allow_html=True
)

st.markdown("Bienvenue dans l'assistant intelligent de sélection de projets. Configurez les paramètres ci-dessous 👇")

# --------- Inputs utilisateur ---------
num_projects = st.number_input("Nombre de projets à sélectionner", min_value=1, step=1, value=5)
job_description = st.text_area("🧠 Description du poste", placeholder="Décrivez ici le poste visé...")
user_description = st.text_area("👤 Votre profil", placeholder="Parlez un peu de vous, de vos compétences, intérêts...")

if st.button("Lancer App"):
# --------- Affichage de la réflexion des agents ---------
    launch = cv_launch.kickoff(inputs=launch_details)

    st.download_button(
        label="📁 Télécharger les résultats",
        file_name="projets_selectionnes.txt",
        mime="text/plain"
    )st.download_button(
        label="📁 Télécharger les résultats",
        file_name="projets_selectionnes.txt",
        mime="text/plain"
    )
