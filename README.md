# 🚀 GitHub Project Analyzer & AI CV Generator 🧠📄
**Valorise tes projets. Impressionne les recruteurs. Simplifie ta vie avec l'IA.**

---

## 🌟 Pourquoi ce projet ?

Les étudiants ingénieurs ont souvent du mal à identifier et mettre en valeur leurs projets les plus pertinents. Grâce à ce système d'agents IA, ce projet automatise :
- L'extraction et l'analyse de projets GitHub
- La compréhension des exigences de poste
- La génération d’un CV en Markdown optimisé pour les recruteurs

✨ *Une façon intelligente de transformer ton code en opportunité professionnelle !*

---

## 🔧 Fonctionnalités Clés

| 🧩 Fonctionnalité | 💬 Description |
|------------------|----------------|
| 🔍 Analyse GitHub | Exploration de tous tes repos pour extraire, évaluer et enrichir leur contenu |
| 🧾 Lecture d'offres | Analyse d'une offre d'emploi pour en extraire les compétences et attentes clés |
| 🎯 Matching | Sélection automatique des projets qui matchent le mieux avec l’offre |
| 💡 Recommandations | Suggestion de projets innovants et formations basées sur les tendances du marché |
| 📄 Génération de CV | Création d’un CV structuré, esthétique et prêt à être envoyé aux recruteurs |

---

## 🧠 Les Agents IA

> Chaque agent a un rôle bien précis. Ensemble, ils collaborent pour générer un livrable puissant.

- 👨‍💻 **`github_analyst`** : Analyse les projets GitHub
- 🧾 **`job_analyst`** : Comprend les attentes d’une offre
- 👩‍🏫 **`project_selector`** : Fait correspondre projets et poste
- 🧑‍💼 **`learning_recommender`** : Propose des projets complémentaires et ressources d’apprentissage
- ✍️ **`cv_writer`** : Génére un CV en Markdown clair et pro

---

## 📦 Stack Technique

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![CrewAI](https://img.shields.io/badge/CrewAI-Agent--Based-orange)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT4-lightgrey?logo=openai)
![Azure](https://img.shields.io/badge/Microsoft-Azure-blue?logo=microsoft)
![GitHub API](https://img.shields.io/badge/GitHub-API-black?logo=github)

---

## 🚀 Installation

```bash
# Installe Python 3.11
sudo apt-get install -y python3.11

# Crée un environnement virtuel (optionnel mais recommandé)
python3.11 -m venv env
source env/bin/activate

# Installe les dépendances
pip install crewai crewai[tools] openai PyGithub pydantic
