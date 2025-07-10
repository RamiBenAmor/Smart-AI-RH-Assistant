import streamlit as st

st.set_page_config(page_title="Smart CV Matcher", page_icon="📂", layout="wide")

st.title("📂 Smart CV Matcher – ATS Intelligent")
st.markdown("---")

st.markdown(
    """
### 🎯 Objectif du projet
Cette application vise à assister les recruteurs dans le traitement de CVs en automatisant deux tâches essentielles :

- **Classification** des CVs selon leur domaine (Informatique, Finance, RH, etc.)
- **Matching intelligent** entre CVs et offres d'emploi grâce à :
  - Similarité sémantique (SBERT)
  - Comparaison des compétences, du titre, et de l'expérience
  - Visualisation claire des scores

---
### 🧭 Navigation
Utilisez le menu à gauche pour accéder aux différents modules de l'application :
- 📄 **Upload & Classification** : Chargez des CVs et obtenez leur domaine automatiquement.
- 🧠 **Matching** : Chargez des Job Descriptions (JDs) et trouvez les CVs les plus pertinents.
- 📊 **Résultats & Visualisation** : Analysez les scores, filtrez les résultats, et téléchargez les CVs.

---
### 👨‍💻 Technologies utilisées
- **SBERT** pour la similarité sémantique (sentence-transformers)
- **BERT fine-tuné** pour la classification automatique des CVs
- **Streamlit** pour l'interface interactive
- **Scikit-learn**, **NLTK**, **regex** pour les traitements NLP
- **Joblib / Torch** pour le chargement des modèles

---
### 📝 Conseils
- Préparez vos fichiers **CVs en PDF** et **Job Descriptions en PDF**.
- Pour de meilleurs résultats, veillez à ce que les documents soient bien structurés.
- L'application supporte le filtrage par score, le téléchargement des résultats, et des visualisations interactives.

---
### 📫 Auteur
Développé par un étudiant en IA, passionné de NLP et d'outils RH intelligents.

> *"Helping recruiters make better decisions, one vector at a time."*
"""
)
