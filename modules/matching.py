import streamlit as st
import pandas as pd
import base64
from .cvScore import *
from .preprocessing import preprocess_pdf
import os
import plotly.express as px
from datetime import datetime


def categorize_score(score):
    if score >= 0.8:
        return "Excellent Match"
    elif score >= 0.6:
        return "Good Match"
    elif score >= 0.5:
        return "Acceptable Match"
    else:
        return "Below Threshold"

# Fonction principale
def match_cv_to_jd(cv_name, jd_name, cv_text: str, jd_text: str) -> dict:
    weights = {
        "full_text": 0.3,
        "skills": 0.15,
        "experience": 0.15,
        "title": 0.4
    }

    cv_skills = extract_section(cv_text, "Skills")
    jd_skills = extract_section(jd_text, "Skills")
    skill_sim = sbert_similarity(cv_skills, jd_skills)

    cv_exp = extract_section(cv_text, "Experience")
    jd_exp = extract_section(jd_text, "Experience")
    cv_exp_sent = extract_experience_sentences(cv_exp)
    jd_exp_sent = extract_experience_sentences(jd_exp)
    exp_sim = sbert_similarity(cv_exp_sent, jd_exp_sent)

    cv_years = extract_years(cv_exp)
    jd_years = extract_years(jd_exp)
    exp_gap = max(jd_years - cv_years, 0)

    title_sim = title_similarity(cv_text, jd_text)
    full_text_sim = compute_sbert_similarity(cv_text, jd_text)

    raw_score = (
        weights["full_text"] * full_text_sim +
        weights["skills"] * skill_sim +
        weights["experience"] * exp_sim +
        weights["title"] * title_sim
    )

    final_score = penalize_exp_gap(raw_score, exp_gap)
    category = categorize_score(final_score)

    return {
        "CV_Name": cv_name,
        "JobDescription_Name": jd_name,
        "MatchingScoreRaw": round(raw_score, 3),
        "MatchingScorePenalized": round(final_score, 3),
        "FullTextSimilarity": round(full_text_sim, 3),
        "SkillSimilarity": round(skill_sim, 3),
        "ExperienceSimilarity": round(exp_sim, 3),
        "TitleSimilarity": round(title_sim, 3),
        "CV_Years": cv_years,
        "JD_Years": jd_years,
        "ExperienceGap": exp_gap,
        "Category": category
    }

def display_pdf(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="900" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    else:
        st.warning("Fichier PDF non trouvé : " + file_path)

def display_Matching(cvfilepath, jdfilepath):
    cv = preprocess_pdf(cvfilepath)
    jd = preprocess_pdf(jdfilepath)
    result = match_cv_to_jd(cvfilepath, jdfilepath, cv, jd)

    if result["MatchingScorePenalized"] < 0.5:
        return

    score = result["MatchingScorePenalized"]
    expander = st.expander(f"CV: {result['CV_Name']} × JD: {result['JobDescription_Name']} — Score: {score:.3f}")
    with expander:
        st.write(f"**Raw Score:** {result['MatchingScoreRaw']:.3f}")
        st.write(f"**Penalized Score:** {result['MatchingScorePenalized']:.3f}")
        st.write(f"**Title Similarity:** {result['TitleSimilarity']:.3f}")
        st.write(f"**Skill Similarity:** {result['SkillSimilarity']:.3f}")
        st.write(f"**Experience Similarity:** {result['ExperienceSimilarity']:.3f}")
        st.write(f"**CV Years Experience:** {int(result['CV_Years'])}")
        st.write(f"**JD Years Required:** {int(result['JD_Years'])}")
        st.write(f"**Experience Gap:** {int(result['ExperienceGap'])}")
        
        display_pdf(cvfilepath)
def display_ALL(cvs, jds):
    st.title("📊 Excellent Matching CV ↔ Job Description")

    data = []

    for cv_path in cvs:
        for jd_path in jds:
            cv_name = os.path.basename(cv_path)
            jd_name = os.path.basename(jd_path)

            try:
                cv_text = preprocess_pdf(cv_path)
                jd_text = preprocess_pdf(jd_path)

                result = match_cv_to_jd(cv_name, jd_name, cv_text, jd_text)
                if result["MatchingScorePenalized"] >= 0.5:
                    data.append(result)

            except Exception as e:
                st.error(f"Erreur : {cv_name} × {jd_name} → {str(e)}")

    if not data:
        st.warning("Aucune correspondance (Score ≥ 0.5) trouvée.")
        return

    df = pd.DataFrame(data)

    grouped = df.groupby("JobDescription_Name")["CV_Name"].apply(list).reset_index()
    grouped["Count"] = grouped["CV_Name"].apply(len)
    grouped["CVs_List"] = grouped["CV_Name"].apply(lambda cvs: ", ".join(cvs))

    st.subheader("📈 Répartition des CVs par Job Description")
    fig = px.pie(
        grouped,
        values="Count",
        names="JobDescription_Name",
        title="Cliquez sur un Job Description pour voir les CVs associés",
        hover_data=["CVs_List"],
        hole=0.4
    )
    fig.update_traces(textposition='inside', textinfo='label+percent')

    selected_job = st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    for index, row in grouped.iterrows():
        job_name = row["JobDescription_Name"]
        with st.expander(f"📌 {job_name} — {row['Count']} CV(s) correspondant(s)", expanded=False):
            matching_cvs = df[df["JobDescription_Name"] == job_name]
            for _, cv_row in matching_cvs.iterrows():
                cv_name = cv_row["CV_Name"]
                st.markdown(f"**👤 {cv_name}** — Matching Score: `{cv_row['MatchingScorePenalized']:.2f}`")
                col1, col2, col3 = st.columns(3)

                with col1:
                    if st.button(f"🧠 Explain Matching — {cv_name}", key=f"explain_{cv_name}_{job_name}"):
                        st.info("🔍 Explication: Ce bouton affichera une analyse détaillée des points de correspondance entre le CV et le poste.")

                with col2:
                    if st.button(f"❓ Generate Questions — {cv_name}", key=f"questions_{cv_name}_{job_name}"):
                        st.success("📋 Questions générées :\n1. Pourquoi avez-vous utilisé [Tech] ?\n2. Quelles difficultés avez-vous rencontrées dans ce projet ?")

                with col3:
                    with st.form(key=f"schedule_form_{cv_name}_{job_name}"):
                        st.markdown("📅 **Planifier un entretien**")
                        date = st.date_input("Date", key=f"date_{cv_name}_{job_name}")
                        time = st.time_input("Heure", key=f"time_{cv_name}_{job_name}")
                        submit = st.form_submit_button("Envoyer Mail")
                        if submit:
                            st.success(f"✅ Mail d'entretien programmé le {date} à {time} pour {cv_name}")

                st.markdown("---")
