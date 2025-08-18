import streamlit as st
import tempfile
import os
import sys
import shutil
import pandas as pd
import plotly.express as px

# Dossier local pour stocker les CVs uploadés (persistants sur disque)
CV_STORAGE_FOLDER = "{path}\\Smart-AI-RH-Assistant\\uploads\\cv"

# Nettoyer le dossier uploads/cv à chaque lancement (optionnel)
if os.path.exists(CV_STORAGE_FOLDER):
    shutil.rmtree(CV_STORAGE_FOLDER)
os.makedirs(CV_STORAGE_FOLDER, exist_ok=True)

# Ajout du path pour importer le module classifier.py (ton code métier)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "modules")))
from classifier import classifier

st.set_page_config(page_title="CV Classification", layout="wide")
st.title("🧾 CV Classification with Interactive Pie Chart")

def save_uploaded_pdf_to_local(uploaded_file):
    # Sauvegarde le fichier uploadé dans uploads/cv/ avec son nom d'origine
    save_path = os.path.join(CV_STORAGE_FOLDER, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return save_path

uploaded_files = st.file_uploader(
    "📄 Upload one or more CVs (PDF format)",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"{len(uploaded_files)} CV(s) uploaded successfully ✅")

    grouped_cvs = {}

    for file in uploaded_files:
        filepath = save_uploaded_pdf_to_local(file)
        predicted_category = classifier(filepath)

        if predicted_category not in grouped_cvs:
            grouped_cvs[predicted_category] = []
        grouped_cvs[predicted_category].append({
            "filename": file.name,
            "filepath": filepath
        })

    # Préparation dataframe pour graphique
    data = []
    for category, cvs in grouped_cvs.items():
        data.append({"Category": category, "Count": len(cvs)})
    df = pd.DataFrame(data)
    df["Percentage"] = (df["Count"] / df["Count"].sum()) * 100

    # Pie chart interactif avec plotly
    fig = px.pie(
        df,
        values="Count",
        names="Category",
        title="CV Distribution by Category",
        hover_data=["Count", "Percentage"],
        labels={"Count": "Number of CVs", "Category": "Category"},
        hole=0.4
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')

    st.plotly_chart(fig, use_container_width=True)

    category_selected = st.selectbox("Select category to display CVs", options=df["Category"])
    st.markdown(f"### CVs in category: **{category_selected}**")

    cvs_to_show = grouped_cvs.get(category_selected, [])

    for cv in cvs_to_show:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**📄 {cv['filename']}**")
        with col2:
            with open(cv["filepath"], "rb") as f:
                st.download_button(
                    label="⬇️ Download",
                    data=f.read(),
                    file_name=cv["filename"],
                    mime="application/pdf",
                    key="download_" + cv["filename"]
                )
else:
    st.info("Please upload one or more PDF CV files to classify.")

