import streamlit as st

st.set_page_config(page_title="Smart AI HR Assistant", page_icon="📂", layout="wide")

st.title("Smart AI HR Assistant")

st.markdown(
    """
### 🎯 Project Objective  
This application is a smart recruitment platform designed to assist HR teams by automating two essential tasks:

- **Automatic classification** of CVs into professional domains (e.g., IT, Finance, HR)  
- **Intelligent matching** between CVs and Job Descriptions (JDs), including:  
  - Personalized scores based on skills, job titles, and experience  
  - Clear visualization of the best-matching CVs for each JD  
  - Pie charts displaying the distribution of CVs by job title

Additionally, the platform streamlines the recruitment process by:  
- Generating **personalized interview questions**  
- Offering a **dashboard to track scheduled interviews**  
- Automating communication by sending **custom interview invitations** and **rejection emails**

---

### 🧭 Navigation  
Use the sidebar menu to access the main modules:  

- 📄 **CV_Classifier**: Upload CVs and automatically classify them into relevant domains.  

- 🧠 **CV_JD_Matching**:  
  - Upload Job Descriptions (JDs)  
  - Upload CVs manually *or* fetch them directly from your inbox (filtered by job title)  
  - The system filters and returns only CVs with a high personalized matching score, based on skills, job titles, experience similarity, and more  
  - Analyze the distribution of CVs across job descriptions  
  - View detailed scoring explanations for each match  
  - Generate tailored interview questions based on the candidate’s CV and the job description  
  - Schedule interviews and send email invitations  
  - Automatically send rejection emails to unselected candidates for a specific job description  

- 📅 **Dashboard**: Monitor scheduled interviews, including candidate names, emails, interview dates, CV paths, send dates, and job titles.

---

### 📝 Recommendations  
- Ensure your **CVs and JDs are in PDF format** and clearly structured.

---

> *"Making the HR process smarter, faster, and more transparent."*
"""
)
