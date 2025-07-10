import streamlit as st
import os
import pandas as pd
from sentence_transformers import SentenceTransformer
from modules.preprocessing import preprocess_pdf
# Charger le modèle SBERT une seule fois
sbert_model = SentenceTransformer("all-MiniLM-L6-v2")

# Répertoire des fichiers
CV_FOLDER = "cv_pdfs"
JD_FOLDER = "jd_pdfs"

# Configuration de l'app
st.set_page_config(page_title="CV Classifier and job description Matcher", layout="wide")
st.title("🔍 Smart CV Matcher")

# Uploader les fichiers
with st.sidebar:
    st.header("📁 Upload your files")

    uploaded_cvs = st.file_uploader("Upload CV PDFs", type="pdf", accept_multiple_files=True)
    uploaded_jds = st.file_uploader("Upload Job Description PDFs", type="pdf", accept_multiple_files=True)

# Sauvegarder les fichiers localement
os.makedirs(CV_FOLDER, exist_ok=True)
os.makedirs(JD_FOLDER, exist_ok=True)

def save_uploaded_files(uploaded_files, folder):
    filepaths = []
    for file in uploaded_files:
        path = os.path.join(folder, file.name)
        with open(path, "wb") as f:
            f.write(file.getbuffer())
        filepaths.append(path)
    return filepaths

cv_paths = save_uploaded_files(uploaded_cvs, CV_FOLDER) if uploaded_cvs else []
jd_paths = save_uploaded_files(uploaded_jds, JD_FOLDER) if uploaded_jds else []

# Processus principal
if cv_paths and jd_paths:
    st.success("✅ Fichiers bien chargés !")

    results = []
    for cv_path in cv_paths:
        cv_text = preprocess_pdf(cv_path)
        best_match = None
        best_score = 0
        best_details = {}

        for jd_path in jd_paths:
            jd_text = load_jd_text(jd_path)
            result = compute_final_score(cv_text, jd_text, sbert_model)
            score = result["FinalScore"]

            if score > best_score:
                best_score = score
                best_match = jd_path
                best_details = result

        result_row = {
            "CV": os.path.basename(cv_path),
            "BestJob": os.path.basename(best_match),
            "FinalScore": round(best_score, 3),
            "MatchingScore": round(best_details["MatchingScore"], 3),
            "SkillSimilarity": round(best_details["SkillSimilarity"], 3),
            "ExperienceSimilarity": round(best_details["ExperienceSimilarity"], 3),
            "TitleSimilarity": round(best_details["TitleSimilarity"], 3),
            "Penalty": round(best_details["Penalty"], 3),
            "CVPath": cv_path
        }
        results.append(result_row)

    df = pd.DataFrame(results)

    # Séparer en deux groupes
    passed = df[df["FinalScore"] >= threshold]
    rejected = df[df["FinalScore"] < threshold]

    st.subheader("✅ CVs that match the job descriptions")
    for i, row in passed.iterrows():
        with st.expander(f"📄 {row['CV']} ➡️ {row['BestJob']} | Score: {row['FinalScore']}"):
            display_score_breakdown(row)
            with open(row["CVPath"], "rb") as f:
                st.download_button("⬇️ Download CV", f, file_name=row["CV"])

    st.subheader("❌ CVs with low matching scores")
    for i, row in rejected.iterrows():
        with st.expander(f"📄 {row['CV']} ➡️ {row['BestJob']} | Score: {row['FinalScore']} ❌"):
            display_score_breakdown(row)
            with open(row["CVPath"], "rb") as f:
                st.download_button("⬇️ Download CV", f, file_name=row["CV"])
else:
    st.info("⬅️ Upload CVs and job descriptions in the sidebar to begin.")
