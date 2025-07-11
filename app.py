import streamlit as st

st.set_page_config(
    page_title="CV RH App",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar menu
st.sidebar.title("🧭 Navigation")
st.sidebar.page_link("pages/1_Home.py", label="🏠 Home")
st.sidebar.page_link("pages/2_CV_Classifier.py", label="🧾 CV Classification")
st.sidebar.page_link("pages/3_CV_JD_Matching.py", label="🤝 CV ↔ Job Description Matching")

# Main landing content
st.title("👋 Welcome to the AI-Powered HR Application")
st.markdown("""
Use the navigation menu on the left to explore the available features:

- **CV Classification**: Automatically categorize resumes based on their content.
- **CV ↔ Job Description Matching**: Check how well a candidate's resume matches a specific job description.
""")
