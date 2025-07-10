import streamlit as st
import pandas as pd
import base64
from cvScore import match_cv_to_jd
cvs_texts = [
    "Senior Accountant",
    "Data Scientist",
    "Java Developer"
]

jds_texts = [
    "Accountant",
    "Senior Java Developer"
]

data = [
    {"CV_Index":0, "JD_Index":0, "MatchingScorePenalized":0.75, "TitleSimilarity":0.8, "SkillSimilarity":0.7, "ExperienceSimilarity":0.6, "MatchingScoreRaw":0.78, "CV_Years":3, "JD_Years":5, "ExperienceGap":2},
    {"CV_Index":1, "JD_Index":0, "MatchingScorePenalized":0.4, "TitleSimilarity":0.3, "SkillSimilarity":0.5, "ExperienceSimilarity":0.4, "MatchingScoreRaw":0.45, "CV_Years":5, "JD_Years":5, "ExperienceGap":0},
    {"CV_Index":2, "JD_Index":1, "MatchingScorePenalized":0.9, "TitleSimilarity":0.95, "SkillSimilarity":0.85, "ExperienceSimilarity":0.8, "MatchingScoreRaw":0.92, "CV_Years":4, "JD_Years":5, "ExperienceGap":1},
    {"CV_Index":0, "JD_Index":1, "MatchingScorePenalized":0.3, "TitleSimilarity":0.2, "SkillSimilarity":0.25, "ExperienceSimilarity":0.1, "MatchingScoreRaw":0.28, "CV_Years":3, "JD_Years":5, "ExperienceGap":2},
]

df_scores = pd.DataFrame(data)

def display_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="900" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

st.title("CV to Job Description Matching Dashboard")

threshold = 0.5  # fixed threshold

for jd_idx, jd_text in enumerate(jds_texts):
    st.header(f"Job Description #{jd_idx}: {jd_text}")
    
    jd_matches = df_scores[(df_scores['JD_Index'] == jd_idx) & (df_scores['MatchingScorePenalized'] >= threshold)]
    jd_matches = jd_matches.sort_values(by='MatchingScorePenalized', ascending=False)
    
    if jd_matches.empty:
        st.write(f"No CV matches above the threshold {threshold}")
    else:
        for _, row in jd_matches.iterrows():
            cv_idx = int(row['CV_Index'])
            cv_name = cvs_texts[cv_idx]
            score = row['MatchingScorePenalized']
            
            # Expander with CV info and PDF
            expander = st.expander(f"CV #{cv_idx}: {cv_name} — Score: {score:.3f}")
            with expander:
                st.write(f"**Raw Score:** {row['MatchingScoreRaw']:.3f}")
                st.write(f"**Penalized Score:** {row['MatchingScorePenalized']:.3f}")
                st.write(f"**Title Similarity:** {row['TitleSimilarity']:.3f}")
                st.write(f"**Skill Similarity:** {row['SkillSimilarity']:.3f}")
                st.write(f"**Experience Similarity:** {row['ExperienceSimilarity']:.3f}")
                st.write(f"**CV Years Experience:** {int(row['CV_Years'])}")
                st.write(f"**JD Years Required:** {int(row['JD_Years'])}")
                st.write(f"**Experience Gap:** {int(row['ExperienceGap'])}")
                
                # Afficher le PDF
                pdf_path = f"cvs/cv_{cv_idx}.pdf"  # chemin local vers le PDF
                try:
                    display_pdf(pdf_path)
                except FileNotFoundError:
                    st.warning("PDF file not found for this CV.")
