from pydantic import BaseModel, Field, confloat
from typing import List, Dict


class ProjectAnalysis(BaseModel):
    """Modèle pour l'analyse technique d'un projet"""
    name: str = Field(..., description="Nom du projet")
    technical_score: confloat(ge=0, le=10) = Field(..., description="Score technique sur 10")
    market_relevance: confloat(ge=0, le=10) = Field(..., description="Pertinence marché sur 10")
    main_features: List[str] = Field(..., description="Fonctionnalités clés")
    technologies: List[str] = Field(..., description="Technologies utilisées")
    difficulty: str = Field(..., description="Niveau de difficulté", pattern="^(Débutant|Intermédiaire|Avancé)$")
    learning_value: confloat(ge=0, le=10) = Field(..., description="Valeur éducative sur 10")

class SelectedProject(BaseModel):
    """Modèle pour les projets sélectionnés"""
    project_name: str = Field(..., description="Nom du projet")
    relevance_score: confloat(ge=0, le=10) = Field(..., description="Score de pertinence")
    selection_reasons: List[str] = Field(..., description="Raisons de sélection")
    improvement_recommendations: List[str] = Field(..., description="Recommandations d'amélioration")

class TrainingRecommendation(BaseModel):
    """Modèle pour les recommandations de formation"""
    skill_area: str = Field(..., description="Domaine de compétence")
    priority_level: str = Field(..., description="Niveau de priorité", pattern="^(Haute|Moyenne|Basse)$")
    recommended_resources: List[str] = Field(..., description="Ressources recommandées")
    learning_objectives: List[str] = Field(..., description="Objectifs d'apprentissage")

class CVContent(BaseModel):
    """Modèle pour la structure du CV généré"""
    personal_info: Dict[str, str] = Field(..., description="Informations personnelles")
    technical_skills: List[str] = Field(..., description="Compétences techniques")
    project_highlights: List[Dict[str, str]] = Field(..., description="Projets clés")
    learning_roadmap: List[Dict[str, str]] = Field(..., description="Plan de formation")
    professional_summary: str = Field(..., description="Résumé professionnel")


class RepoInfo(BaseModel):
    """Structure des informations brutes d'un repository"""
    name: str = Field(..., description="Nom du dépôt")
    description: str = Field("", description="Description du projet")
    languages: Dict[str, int] = Field(..., description="Langages utilisés")
    stars: int = Field(0, description="Nombre d'étoiles")
    forks: int = Field(0, description="Nombre de forks")
    topics: List[str] = Field(default_factory=list, description="Topics du projet")
    updated_at: str = Field(..., description="Dernière mise à jour")
    readme: str = Field("", description="Contenu du README")

# Ajoutez ces modèles dans models.py
class ProjectAnalysisList(BaseModel):
    """Conteneur pour une liste d'analyses de projets"""
    projects: List[ProjectAnalysis]

class SelectedProjectList(BaseModel):
    projects: List[SelectedProject]

class TrainingRecommendationList(BaseModel):
    recommendations: List[TrainingRecommendation]