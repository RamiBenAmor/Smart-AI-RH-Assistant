# Smart AI HR Assistant 

This project leverages **AI** to optimize recruitment by automating key tasks such as CV classification, matching with job descriptions, and interview management.

---

## ✨ Key Features

### 1. Automatic CV Classification
- Upload CVs and have them automatically classified by professional domains (IT, Finance, HR, etc.).  
- Visualize the distribution of CVs across job categories.

### 2. Job Description (JD)-Based CV Filtering & Matching
- Upload job descriptions (JDs).  
- Upload CVs manually or fetch them automatically from Gmail inbox with filters by job title and date range.  
- Match CVs to JDs with a personalized compatibility score based on skills, experience, and job titles.  
- Analyze CV distribution per job role.  
- View detailed scoring breakdowns per candidate.  
- Generate tailored interview questions using Large Language Models (LLMs).  
- Schedule interviews and send invitations automatically.  
- Send rejection emails automatically to unselected candidates.

### 3. Interview Management
- Monitor scheduled interviews via a dedicated dashboard showing candidate info, interview dates, CVs, and job titles.

---

## 🛠️ Tech Stack

Python • Streamlit • FastAPI • AI Agents • Model Context Protocol (MCP) • Large Language Models (LLMs) • Transformers • NLTK

---

## 📦 Installation & Setup

### Requirements
- The main project runs with **Python 3.10+** globally.  
- The server components (e.g., MCP modules) require **Python 3.13** in a **virtual environment**.

---

### 🔧 Setup Instructions

#### 1. Clone this repository and required external modules:

- [mcp-use](https://github.com/mcp-use/mcp-use)  
- [google-workspace-mcp-server](https://github.com/epaproditus/google-workspace-mcp-server)

#### 2. Create and activate a virtual environment for MCP (Python 3.13):

```powershell
cd Smart-AI-RH-Assistant\functions\mcp-use
.\mcp_env\Scripts\Activate.ps1
```

Once activated:

```powershell
cd  Smart-AI-RH-Assistant\functions
uvicorn main:app --reload
```

#### 3. In a separate terminal, launch the frontend (Python 3.10):

```powershell
cd Smart-AI-RH-Assistant
streamlit run app.py
```

> ✅ Make sure to configure Gmail access and API keys if email fetching is used.

---


## 📎 Demo

A  demo video of the platform in action is available.  
All emails shown in the video are invalid and used purely for privacy purposes.

---

## 📂 Repository Structure (Simplified)

```
Smart-AI-RH-Assistant/
│
├── .vscode/                # VSCode workspace settings (e.g., debug configs)
│
├── functions/              # Core backend logic
│   ├── __init__.py         # Python package marker
│   ├── config.json         # Configuration file (API keys, paths)
│   ├── download_attachment.py  # Fetches CVs from Gmail
│   ├── download_search.py  # Searches emails by criteria
│   ├── email_meet.py       # Handles interview scheduling/emails
│   ├── main.py             # Likely the FastAPI entry point
│   └── mcp_env/           # MCP agent dependencies
│
├── models/                 # ML models and training artifacts
│   ├── bert/               # Fine-tuned BERT model directory
│   ├── classification_report1.txt  # Model performance metrics
│   └── label_encoder.pkl   # Encodes job domains (IT/Finance/etc.)
│
├── modules/                # Reusable utility modules
│   ├── classifier.py       # CV domain classification
│   ├── cvScore.py          # JD-CV matching/scoring logic
│   ├── explain_score.py    # Explains match scores to users
│   ├── interviewQuestions.py  # Generates LLM-powered questions
│   ├── preprocessing.py    # Cleans CV/JD text
│   └── saveToTxt.py        # Save in text file
│
├── pages/                  # Streamlit UI pages
│   ├── 1_Home.py          # Landing page
│   ├── 2_CV_Classifier.py  # CV classification UI
│   ├── 3_CV_JD_Matching.py # JD matching UI
│   └── 4_Dashboard.py      # Interview tracking dashboard
│
├── results/                # Generated outputs
│   ├── explanation.txt     # Score breakdowns (for candidates)
│   └── questions.txt       # Generated interview questions
│
├── uploads/                # User-uploaded files
│   ├── cv/                 # Uploaded CVs (PDF)
│   └── job_descriptions/   # Uploaded JDs (PDF)
│
├── app.py                  # Main Streamlit entry point
├── clean_resume_data.csv   # Processed CV dataset
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
└── sent_emails.csv         # Logs of automated emails sent
```

---

## 📫 Contact

For collaboration or feedback, feel free to connect via [LinkedIn](https://www.linkedin.com/in/rami-ben-amor).

---

