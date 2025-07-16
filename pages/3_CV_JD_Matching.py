import streamlit as st
import os
import sys

# Importation de la fonction display_ALL
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.matching import display_ALL

# Configuration de la page
st.set_page_config(page_title="Matching", page_icon="🔍", layout="wide")
st.title("👔 Gestion des CVs et Job Descriptions")

# Dossiers de stockage
CV_STORAGE_FOLDER = "uploads/cv"
JD_STORAGE_FOLDER = "uploads/job_descriptions"

# Initialisation de l'état d'upload pour éviter rechargement infini
if "cv_uploaded" not in st.session_state:
    st.session_state.cv_uploaded = False

if "jd_uploaded" not in st.session_state:
    st.session_state.jd_uploaded = False

# --- Fonctions utilitaires ---
def list_pdfs(folder_path):
    if not os.path.exists(folder_path):
        return []
    return sorted([f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")])

def save_uploaded_pdf(uploaded_file, folder_path):
    os.makedirs(folder_path, exist_ok=True)
    save_path = os.path.join(folder_path, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return save_path

# --- Upload des CVs ---
st.subheader("⬆️ Ajouter de nouveaux CVs")
uploaded_cvs = st.file_uploader(
    "📄 Upload un ou plusieurs CVs (PDF uniquement)",
    type=["pdf"],
    accept_multiple_files=True,
    key="upload_cvs"
)

uploaded_cv_paths = []
if uploaded_cvs and not st.session_state.cv_uploaded:
    for file in uploaded_cvs:
        path = save_uploaded_pdf(file, CV_STORAGE_FOLDER)
        uploaded_cv_paths.append(path)
    st.session_state.cv_uploaded = True
    st.success(f"{len(uploaded_cv_paths)} CV(s) ajouté(s) avec succès ✅")

# --- Affichage des CVs existants ---
st.subheader("📂 CVs disponibles")
existing_cvs = list_pdfs(CV_STORAGE_FOLDER)

if existing_cvs:
    for cv_filename in existing_cvs:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**📄 {cv_filename}**")
        with col2:
            cv_path = os.path.join(CV_STORAGE_FOLDER, cv_filename)
            with open(cv_path, "rb") as f:
                st.download_button(
                    label="⬇️ Télécharger",
                    data=f.read(),
                    file_name=cv_filename,
                    mime="application/pdf",
                    key="download_cv_" + cv_filename
                )
else:
    st.info("Aucun CV disponible.")

st.markdown("---")

# --- Upload des JDs ---
st.subheader("⬆️ Ajouter de nouvelles Job Descriptions")
uploaded_jds = st.file_uploader(
    "📄 Upload une ou plusieurs Job Descriptions (PDF uniquement)",
    type=["pdf"],
    accept_multiple_files=True,
    key="upload_jds"
)

uploaded_jd_paths = []
if uploaded_jds and not st.session_state.jd_uploaded:
    for file in uploaded_jds:
        path = save_uploaded_pdf(file, JD_STORAGE_FOLDER)
        uploaded_jd_paths.append(path)
    st.session_state.jd_uploaded = True
    st.success(f"{len(uploaded_jd_paths)} JD(s) ajoutée(s) avec succès ✅")

# --- Affichage des JDs existants ---
st.subheader("📂 Job Descriptions disponibles")
existing_jds = list_pdfs(JD_STORAGE_FOLDER)

if existing_jds:
    for jd_filename in existing_jds:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**📄 {jd_filename}**")
        with col2:
            jd_path = os.path.join(JD_STORAGE_FOLDER, jd_filename)
            with open(jd_path, "rb") as f:
                st.download_button(
                    label="⬇️ Télécharger",
                    data=f.read(),
                    file_name=jd_filename,
                    mime="application/pdf",
                    key="download_jd_" + jd_filename
                )
else:
    st.info("Aucune Job Description disponible.")

st.markdown("---")

# --- Matching des CVs avec les JDs ---
st.subheader("📊 Résultat du Matching CV ↔ JD")

# Chemins complets
existing_cv_paths = [os.path.join(CV_STORAGE_FOLDER, f) for f in existing_cvs]
existing_jd_paths = [os.path.join(JD_STORAGE_FOLDER, f) for f in existing_jds]

# Combine anciens + nouveaux
all_cv_paths = existing_cv_paths + uploaded_cv_paths
all_jd_paths = existing_jd_paths + uploaded_jd_paths

if all_cv_paths and all_jd_paths:
    display_ALL(all_cv_paths, all_jd_paths)
else:
    st.warning("⚠️ Veuillez ajouter au moins un CV et une Job Description pour effectuer le matching.")
