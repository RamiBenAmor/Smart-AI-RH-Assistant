import streamlit as st
import glob
import pandas as pd
import base64
from .cvScore import *
from .preprocessing import load_text, preprocess_pdf
import os
import plotly.express as px
from datetime import datetime, timedelta
from .explain_score import Explanationpdf, explain_cv_score
from .interviewQuestions import generate_interview_questionstxt
import requests
import pytz 
from .addLineDashboard import add_to_dashboard
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
        st.warning("PDF File not found : " + file_path)

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
    count = 0
    data = []
    ## Check how many job descriptions exists [new] 
    jd_count = len(jds)
    debug_mode = st.checkbox("🔍 Show Matching Details", False)
    for cv_path in cvs:
        for jd_path in jds:
            cv_name = os.path.basename(cv_path)
            jd_name = os.path.basename(jd_path)  # FIX: Cette ligne était manquante !

            try:
                cv_text = preprocess_pdf(cv_path)
                jd_text = preprocess_pdf(jd_path)
                result = match_cv_to_jd(cv_name, jd_name, cv_text, jd_text)
                if debug_mode:
                # Debug: Afficher les tailles de texte
                    st.write(f"🔍 Debug: {cv_name} - CV text length: {len(cv_text)}, JD text length: {len(jd_text)}")
                # Debug: Afficher le score
                    st.write(f"📊 Score for {cv_name} × {jd_name}: {result['MatchingScorePenalized']:.3f}")
                
                if result["MatchingScorePenalized"] >= 0.5:
                    data.append(result)

            except Exception as e:
                st.error(f"Error : {cv_name} × {jd_name} → {str(e)}")

    if not data:
        st.warning("No match (Score ≥ 0.5) found.")
        # Debug: Afficher tous les scores même < 0.5
        #debug_mode1 = st.checkbox("🔍 Enable Debug Mode (Show Matching Details)", False)
        #st.info("🔍 Tous les scores calculés ont été affichés ci-dessus.")
        return

    df = pd.DataFrame(data)

    grouped = df.groupby("JobDescription_Name")["CV_Name"].apply(list).reset_index()
    grouped["Count"] = grouped["CV_Name"].apply(len)
    grouped["CVs_List"] = grouped["CV_Name"].apply(lambda cvs: ", ".join(cvs))

    st.subheader("📈 Breakdown of CVs by Job Description")
    fig = px.pie(
        grouped,
        values="Count",
        names="JobDescription_Name",
        title="Click on a Job Description to view the associated CVs",
        hover_data=["CVs_List"],
        hole=0.4
    )
    fig.update_traces(textposition='inside', textinfo='label+percent')

    selected_job = st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    for index, row in grouped.iterrows():
        job_name = row["JobDescription_Name"]
        with st.expander(f"📌 {job_name} — {row['Count']} Matching CV(s)", expanded=False):
            matching_cvs = df[df["JobDescription_Name"] == job_name]
            cv_directory = "uploads/cv"
            all_uploaded_cvs = set([
            os.path.basename(path)
            for path in glob.glob(os.path.join(cv_directory, "*.pdf"))
        ])
            matched_cv_names = set(matching_cvs["CV_Name"].unique())
            rejected_cvs = all_uploaded_cvs - matched_cv_names
            df_rejected = pd.DataFrame({"Rejected_CV": list(rejected_cvs)})
            for _, cv_row in matching_cvs.iterrows():
                cv_name = cv_row["CV_Name"]
                st.markdown(f"**👤 {cv_name}** — Matching Score: `{cv_row['MatchingScorePenalized']:.2f}`")
                col1, col2, col3 = st.columns(3)

                with col1:
                    if st.button(f"explain_{count}_{cv_name}_{job_name[:-3]}"):
                        # FIX: Utiliser les chemins dynamiques au lieu de chemins hardcodés
                        cv_path = None
                        jd_path = None
                        # Trouver les chemins complets
                        for cv in cvs:
                            if os.path.basename(cv) == cv_name:
                                cv_path = cv
                                break
                        
                        for jd in jds:
                            if os.path.basename(jd) == job_name:
                                jd_path = jd
                                break
                        
                        if cv_path and jd_path:
                            cv_text = preprocess_pdf(cv_path)
                            jd_text = preprocess_pdf(jd_path) 
                            result = match_cv_to_jd(cv_name, job_name, cv_text, jd_text)
                            Explanationpdf(result["FullTextSimilarity"],result["SkillSimilarity"],result["TitleSimilarity"],result["ExperienceSimilarity"],extract_section(cv_text, "Skills"),extract_section(jd_text, "Skills"))
                        
                with col2:
                    if st.button(f"❓ Generate Questions_{count}_{cv_name}_{job_name}"):
                        # FIX: Utiliser les chemins dynamiques
                        cv_path = None
                        jd_path = None
                        
                        for cv in cvs:
                            if os.path.basename(cv) == cv_name:
                                cv_path = cv
                                break
                        
                        for jd in jds:
                            if os.path.basename(jd) == job_name:
                                jd_path = jd
                                break
                                
                        if cv_path and jd_path:
                            cv_text = preprocess_pdf(cv_path)
                            jd_text = preprocess_pdf(jd_path) 
                            generate_interview_questionstxt(cv_text,jd_text)    
                      
                with col3:
                    with st.form(key=f"schedule_form_{count}_{cv_name}_{job_name}"):
                        url = "http://localhost:8000/email_meet"
                        st.markdown("📅 **Plan interview**")
                        
                        # FIX: Utiliser les chemins dynamiques
                        cv_path = None
                        for cv in cvs:
                            if os.path.basename(cv) == cv_name:
                                cv_path = cv
                                break
                        
                        if cv_path:
                            cv_textFULL = load_text(cv_path)
                            email = extract_email_from_cv(cv_textFULL)
                            st.write(f"Email extracted from CV : {email}")
                            
                            # Choisir date et heure
                            date = st.date_input("Date", key=f"date_{cv_name}_{job_name}")
                            time = st.time_input("Heure", key=f"time_{cv_name}_{job_name}")
                            submit = st.form_submit_button("Send Mail")
                            
                            if submit:
                                interview_datetime = datetime.combine(date, time)
                                sent_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                #cv_name="CV_nameCandidat"
                                add_to_dashboard(
                                      "C:\\Users\\ramib\\OneDrive\\Bureau\\CV_RH\\sent_emails.csv",
                                      cv_name[3:-4],
                                      email,
                                      interview_datetime.strftime("%Y-%m-%d %H:%M"),
                                      cv_path,
                                      sent_datetime,
                                      job_name
                                     )
                                # Combinaison date + time en datetime
                                #dt_start_naive = datetime.combine(date, time)
                                # Ajout du fuseau horaire (exemple : Europe/Tunis = UTC+1)
                                tz = pytz.timezone("Africa/Tunis")
                                dt_start = tz.localize(interview_datetime)

                                # Durée de l'entretien (1 heure ici)
                                dt_end = dt_start + timedelta(hours=2)

                                # Conversion en ISO 8601 (avec timezone +01:00)
                                start_iso = dt_start.isoformat()
                                end_iso = dt_end.isoformat()

                                payload = {
                                    "start_iso": start_iso,
                                    "end_iso": end_iso,
                                    "attendees_emails": [email],
                                    "accepted": True,
                                    "job_title":job_name
                                }

                                try:
                                    response = requests.post(url, json=payload)
                                    response.raise_for_status()  # pour attraper les erreurs
                                    st.success(f"✅ Interview Programmed Successfully!")
                                except requests.exceptions.RequestException as e:
                                    st.error(f"❌ Error when sending : {e}")
                
                count += 1
                st.markdown("---")
    if len(jds) == 1:
      st.subheader("📤 Send Rejection Emails")
      if st.button("🚫 Send rejection emails to unmatched candidates"):
        st.warning("❌ List of rejected CVs:")
        st.dataframe(df_rejected)
        url = "http://localhost:8000/email_meet"
        cv_directory = "uploads/cv"
        for _, row in df_rejected.iterrows():
            cv_name = row["Rejected_CV"]
            cv_path = os.path.join(cv_directory, cv_name)
            if os.path.exists(cv_path):
                cv_textFULL = load_text(cv_path)
                email = extract_email_from_cv(cv_textFULL)
                st.write(f"Email extracted from CV : {email}")
                # Dates par défaut (tu peux adapter)
                start_iso = datetime.now().isoformat()
                end_iso = (datetime.now() + timedelta(hours=1)).isoformat()
                payload = {
                    "start_iso": start_iso,
                    "end_iso": end_iso,
                    "attendees_emails": [email],
                    "accepted": False,
                    "job_title": job_name
                }
                try:
                    response = requests.post(url, json=payload)
                    response.raise_for_status()
                    st.success(f"❌ Rejection email sent to {cv_name[3:]}")
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Error when sending to {cv_name[3:]}: {e}")
    else:
     st.info("ℹ️ Rejection emails can only be sent automatically when exactly one Job Description is selected.")
