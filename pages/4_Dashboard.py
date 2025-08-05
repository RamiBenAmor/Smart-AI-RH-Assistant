import streamlit as st
import pandas as pd
from datetime import datetime
import os

CSV_PATH = "C:\\Users\\ramib\\OneDrive\\Bureau\\CV_RH\\sent_emails.csv"
# Créer le fichier avec entêtes si vide ou inexistant
if not os.path.exists(CSV_PATH) or os.path.getsize(CSV_PATH) == 0:
    pd.DataFrame(columns=["Candidate Name", "Email", "Interview Date", "CV Path", "Sent Date","job_title"]).to_csv(CSV_PATH, index=False)

st.set_page_config(page_title="Candidate Interview Dashboard", layout="wide")

st.markdown("""
    <h1 style='text-align: center; color: #2e86c1;'>🧑‍💼 Candidate Interview Dashboard</h1>
    <hr style='border: 1px solid #bbb;' />
""", unsafe_allow_html=True)


# Lecture du fichier
df = pd.read_csv(CSV_PATH)

# Affichage des métriques
col1, col2 = st.columns(2)
col1.metric("📬 Emails Sent", len(df))
col2.metric("📄 CVs Collected", df['CV Path'].nunique())

# Affichage du tableau
st.markdown("### 📋 Candidates List")
st.dataframe(df, use_container_width=True)

# Section pour ajouter une entrée manuelle
st.markdown("---")
st.markdown("### ➕ Add a New Entry Manually")

with st.form("add_entry_form"):
    col1, col2 = st.columns(2)
    name = col1.text_input("Candidate Name")
    email = col2.text_input("Email")
    date = col1.date_input("Interview Date")
    cv_path = col2.text_input("CV Path (e.g., cv_files/your_cv.pdf)")
    job_title=col2.text_input("Job Title")
    submitted = st.form_submit_button("Add Entry")

    if submitted:
        new_row = pd.DataFrame([{
            "Candidate Name": name,
            "Email": email,
            "Interview Date": str(date),
            "CV Path": cv_path,
            "Sent Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "job_title":job_title
        }])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(CSV_PATH, index=False)
        st.success("✅ Candidate added successfully.")
        #st.rerun()
