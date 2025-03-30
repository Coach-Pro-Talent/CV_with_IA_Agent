#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from cv_agents.crew import CvAgents
import json
import os

def get_user_inputs():
    """Collecte les informations de l'utilisateur."""
    print("\n=== Configuration de l'Analyse de Portfolio ===")
    
    # Collecte des informations
    username = input("Entrer votre username GitHub : ")
    number_project = int(input("Nombre de projets à analyser [5] : ") or "5")
    job_description = input("Description du poste visé : ")
    
    return {
        'username': username,
        'number_project': number_project,
        'job_description': job_description,
        'timestamp': datetime.now().isoformat()
    }

def save_results(results, filename):
    """Sauvegarde les résultats dans un fichier JSON."""
    os.makedirs("output", exist_ok=True)
    output_file = f"output/{filename}"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"📁 Résultats sauvegardés dans: {output_file}")

def run():
    """Exécute l'analyse du portfolio."""
    try:
        print("\n🚀 Démarrage de l'Analyse de Portfolio")
        
        # Collecte des informations
        inputs = get_user_inputs()
        
        # Exécution de l'analyse
        print("\n🔍 Analyse en cours...")
        crew = CvAgents()
        results = crew.crew().kickoff(inputs=inputs)
        
        # Sauvegarde des résultats
        filename = f"analysis_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        save_results(results, filename)
        
        print("\n✅ Analyse terminée avec succès!")
        
    except KeyboardInterrupt:
        print("\n⚠️ Analyse interrompue par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur: {str(e)}")
        raise


if __name__ == "__main__":
   run()