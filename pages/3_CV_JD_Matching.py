import requests
import streamlit as st
import os
import sys
import time

# Importation de la fonction display_ALL
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.matching import display_ALL

# Configuration de la page
st.set_page_config(page_title="Matching", page_icon="🔍", layout="wide")
st.title("👔 Management of CVs and Job Descriptions")

# Dossiers de stockage
CV_STORAGE_FOLDER = "uploads/cv"
JD_STORAGE_FOLDER = "uploads/job_descriptions"

def list_pdfs_with_info(folder_path):
    if not os.path.exists(folder_path):
        return []
    files = []
    for f in os.listdir(folder_path):
        if f.lower().endswith(".pdf"):
            file_path = os.path.join(folder_path, f)
            mod_time = os.path.getmtime(file_path)
            files.append({
                'name': f,
                'path': file_path,
                'mod_time': mod_time
            })
    return sorted(files, key=lambda x: x['mod_time'], reverse=True)

def save_uploaded_pdf(uploaded_file, folder_path):
    os.makedirs(folder_path, exist_ok=True)
    save_path = os.path.join(folder_path, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return save_path

def get_folder_hash(folder_path):
    """Créer un hash basé sur les fichiers du dossier"""
    if not os.path.exists(folder_path):
        return "empty"
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]
    return str(hash(tuple(sorted(files))))

# Initialiser les hash dans session_state si pas déjà fait
if 'cv_folder_hash' not in st.session_state:
    st.session_state.cv_folder_hash = get_folder_hash(CV_STORAGE_FOLDER)
    
if 'jd_folder_hash' not in st.session_state:
    st.session_state.jd_folder_hash = get_folder_hash(JD_STORAGE_FOLDER)

# --- Upload des JDs ---
st.subheader("⬆️ Add new  Job Descriptions")
uploaded_jds = st.file_uploader(
    "📄Upload one or more Job Descriptions (PDF only)",
    type=["pdf"],
    accept_multiple_files=True,
    key="upload_jds"
)

if uploaded_jds:
    progress_bar = st.progress(0)
    for i, file in enumerate(uploaded_jds):
        save_uploaded_pdf(file, JD_STORAGE_FOLDER)
        progress_bar.progress((i + 1) / len(uploaded_jds))
    progress_bar.empty()
    st.success(f"✅ {len(uploaded_jds)} JD(s) added successfully!")

# --- Affichage des JDs existants ---
st.subheader("📂 Available Job descriptions")
jd_files = list_pdfs_with_info(JD_STORAGE_FOLDER)

if jd_files:
    for jd_info in jd_files:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            # Marquer les fichiers récents (moins de 5 minutes)
            is_recent = (time.time() - jd_info['mod_time']) < 300
            icon = "🆕" if is_recent else "📄"
            st.markdown(f"**{icon} {jd_info['name']}**")
        with col2:
            st.caption(f"Modified: {time.strftime('%H:%M', time.localtime(jd_info['mod_time']))}")
        with col3:
            with open(jd_info['path'], "rb") as f:
                st.download_button(
                    label="⬇️",
                    data=f.read(),
                    file_name=jd_info['name'],
                    mime="application/pdf",
                    key="download_jd_" + jd_info['name']
                )
else:
    st.info("No available Job descriptions")

st.markdown("---")

# --- Upload des CVs ---
st.subheader("⬆️ Add new CVs")
uploaded_cvs = st.file_uploader(
    "📄 Upload one or more CVs (PDF only)",
    type=["pdf"],
    accept_multiple_files=True,
    key="upload_cvs"
)

if uploaded_cvs:
    progress_bar = st.progress(0)
    for i, file in enumerate(uploaded_cvs):
        save_uploaded_pdf(file, CV_STORAGE_FOLDER)
        progress_bar.progress((i + 1) / len(uploaded_cvs))
    progress_bar.empty()
    st.success(f"✅ {len(uploaded_cvs)} CV(s) added suceesfully!")

# --- Search CVs from email ---
st.subheader("🔍 Search CVs in your Gmail")
job_description_name = st.text_input("🧑‍💼 Enter Job Title (e.g., Developer,Accountant):")
days = st.number_input("Select how many days back to search: ", min_value=1, max_value=30, value=3, step=1)
st.info("""
📢 **Important for HR:**  
Please inform candidates to send their application emails with:  
- **Subject:** Application_JobTitle (e.g., Application_Developer)  
- **Attachment:** CV named as CV_NameCandidate (e.g., CV_RamiBenAmor.pdf)  
This format is required so the system can correctly find and download the CVs from emails.
""")
if st.button("🔍 Search and Download CVs from Email", type="primary"):
    if job_description_name.strip() == "":
        st.warning("⚠️ Please enter a job title before searching.")
    else:
        # Enregistrer l'état avant téléchargement
        cv_count_before = len(list_pdfs_with_info(CV_STORAGE_FOLDER))
        
        with st.spinner("🔍 Searching emails and downloading PDFs..."):
            try:
                response = requests.post("http://localhost:8000/downoald_search", 
                                       json={"job_description_name": job_description_name, "days": days})
                if response.status_code == 200:
                    # Attendre un peu pour que les fichiers soient écrits
                    time.sleep(1)
                    cv_count_after = len(list_pdfs_with_info(CV_STORAGE_FOLDER))
                    new_cvs = cv_count_after - cv_count_before
                    
                    if new_cvs > 0:
                        st.success(f"🎉 {new_cvs} New CV(s) uploaded from your email!")
                    else:
                        st.info("✅ Research finished - no new CV found.")
                else:
                    st.error(f"❌ Downoald fails. Error code: {response.status_code}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

st.markdown("---")

# --- Affichage des CVs existants ---
st.subheader("📂 Available CVs")
cv_files = list_pdfs_with_info(CV_STORAGE_FOLDER)

if cv_files:
    for cv_info in cv_files:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            # Marquer les fichiers récents (moins de 5 minutes)
            is_recent = (time.time() - cv_info['mod_time']) < 300
            icon = "🆕" if is_recent else "📄"
            st.markdown(f"**{icon} {cv_info['name']}**")
        with col2:
            st.caption(f"Modified: {time.strftime('%H:%M', time.localtime(cv_info['mod_time']))}")
        with col3:
            with open(cv_info['path'], "rb") as f:
                st.download_button(
                    label="⬇️",
                    data=f.read(),
                    file_name=cv_info['name'],
                    mime="application/pdf",
                    key="download_cv_" + cv_info['name']
                )
else:
    st.info("No available Cv")

st.markdown("---")

# --- Matching des CVs avec les JDs ---
st.subheader("📊 Result of Matching CV ↔ JD")

# Toujours recalculer les fichiers pour le matching (fresh data)
fresh_cv_files = list_pdfs_with_info(CV_STORAGE_FOLDER)
fresh_jd_files = list_pdfs_with_info(JD_STORAGE_FOLDER)

# Obtenir tous les fichiers actuels
all_cv_paths = [cv_info['path'] for cv_info in fresh_cv_files]
all_jd_paths = [jd_info['path'] for jd_info in fresh_jd_files]

if all_cv_paths and all_jd_paths:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.info(f"📊 Analysis of {len(all_cv_paths)} CV(s) with{len(all_jd_paths)} JD(s)")
    with col2:
        if st.button("🔄 Refresh Matching"):
            st.rerun()
    # Afficher les résultats
    with st.container():
        display_ALL(all_cv_paths, all_jd_paths)
        
else:
    st.warning("⚠️ Please add at least one Cv and one Job Description to enable matching")
    
    if not all_cv_paths:
        st.error("❌ No Cv detected")
    if not all_jd_paths:
        st.error("❌No Job Description detected")
