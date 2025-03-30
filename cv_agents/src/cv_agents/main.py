from cv_agents.crew import CvAgents
from typing import Dict
import json
import os
from dotenv import load_dotenv

def get_user_inputs() -> Dict:
    """Récupère les entrées utilisateur de manière interactive"""
    print("\n=== Configuration de l'Analyse de Portfolio GitHub ===\n")
    
    # Récupération des informations GitHub
    username = input("Entrez votre nom d'utilisateur GitHub: ").strip()
    while not username:
        print("❌ Le nom d'utilisateur est requis!")
        username = input("Entrez votre nom d'utilisateur GitHub: ").strip()

    # Récupération du nombre de projets
    while True:
        try:
            number_project = int(input("Nombre de projets à analyser (1-10) [5]: ").strip() or "5")
            if 1 <= number_project <= 10:
                break
            print("❌ Le nombre doit être entre 1 et 10!")
        except ValueError:
            print("❌ Veuillez entrer un nombre valide!")

    # Description du poste
    print("\nDécrivez le poste visé (appuyez sur Entrée deux fois pour terminer):")
    job_description_lines = []
    while True:
        line = input()
        if not line and job_description_lines:
            break
        job_description_lines.append(line)
    job_description = "\n".join(job_description_lines)

    # Informations personnelles
    print("\n=== Informations Personnelles ===")
    user_info = {
        "name": input("Nom complet: ").strip(),
        "email": input("Email: ").strip(),
        "title": input("Titre professionnel: ").strip(),
        "linkedin": input("LinkedIn (optionnel): ").strip(),
        "location": input("Localisation: ").strip()
    }

    return {
        "username": username,
        "number_project": number_project,
        "job_description": job_description,
        "user_info": user_info
    }

def run_portfolio_analysis(
    username: str,
    job_description: str,
    number_project: int = 5,
    user_info: Dict = None
) -> Dict:
    """
    Exécute l'analyse du portfolio GitHub et génère un CV.
    """
    try:
        print("\n=== Démarrage de l'Analyse ===")
        print(f"📊 Analyse du profil GitHub: {username}")
        print(f"📁 Nombre de projets: {number_project}")
        
        # Création du crew
        crew = CvAgents()
        
        # Configuration des inputs
        crew.inputs.username = username
        crew.inputs.job_description = job_description
        crew.inputs.number_project = number_project
        crew.inputs.user_info = user_info or {}

        # Exécution du crew
        print("\n🔄 Analyse en cours...")
        result = crew.crew()
        
        output_files = {
            "analysis": "output/projects_analysis.json",
            "selected_projects": "output/selected_projects.json",
            "recommendations": "output/recommendations.json",
            "cv": "output/cv.md"
        }

        # Vérification des fichiers générés
        generated_files = []
        for name, path in output_files.items():
            if os.path.exists(path):
                generated_files.append(name)

        print("\n✅ Analyse terminée avec succès!")
        print(f"📂 Fichiers générés: {', '.join(generated_files)}")

        return {
            "status": "success",
            "message": "Analyse terminée avec succès",
            "outputs": output_files
        }

    except Exception as e:
        print(f"\n❌ Erreur: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }

def display_results(result: Dict):
    """Affiche les résultats de l'analyse"""
    if result["status"] == "success":
        print("\n=== Résultats de l'Analyse ===")
        print("Les fichiers suivants ont été générés:")
        for file_type, file_path in result["outputs"].items():
            print(f"- {file_type}: {file_path}")
        print("\nVous pouvez trouver tous les fichiers dans le dossier 'output'")
    else:
        print(f"\n❌ L'analyse a échoué: {result['message']}")

def run():
    """Fonction principale"""
    try:
        # Chargement des variables d'environnement
        load_dotenv()
        
        # Vérification des variables d'environnement requises
        required_env = ["GITHUB_TOKEN", "DEEPSEEK_API_KEY", "DEEP_SEEK_BASE"]
        missing_env = [env for env in required_env if not os.getenv(env)]
        if missing_env:
            print(f"❌ Variables d'environnement manquantes: {', '.join(missing_env)}")
            return

        inputs = get_user_inputs()
        
        result = run_portfolio_analysis(**inputs)
 
        display_results(result)

    except KeyboardInterrupt:
        print("\n\n⚠️ Opération annulée par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {str(e)}")

if __name__ == "__main__":
    run()