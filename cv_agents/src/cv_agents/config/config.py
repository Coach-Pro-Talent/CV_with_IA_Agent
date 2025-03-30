from pathlib import Path
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()

class Config:
    # GitHub
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    
    # DeepSeek
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    DEEP_SEEK_BASE = os.getenv("DEEP_SEEK_BASE")
    
    # Configurations générales
    OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "output/"))
    MAX_REPOS = int(os.getenv("MAX_REPOS", "10"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.1"))
    MODEL_NAME = os.getenv("MODEL_NAME", "deepseek-coder-33b-instruct")

    @classmethod
    def validate(cls):
        """Valide les variables d'environnement requises"""
        required_vars = {
            "GITHUB_TOKEN": cls.GITHUB_TOKEN,
            "DEEPSEEK_API_KEY": cls.DEEPSEEK_API_KEY,
            "DEEP_SEEK_BASE": cls.DEEP_SEEK_BASE
        }
        
        missing = [var for var, value in required_vars.items() if not value]
        
        if missing:
            raise ValueError(
                f"Variables d'environnement manquantes: {', '.join(missing)}\n"
                "Veuillez les définir dans le fichier .env"
            )

    @classmethod
    def create_output_dir(cls):
        """Crée le répertoire de sortie s'il n'existe pas"""
        cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True) 