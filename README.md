# Smart AI HR Assistant (Project in Development)

This project leverages **NLP** and **Machine Learning** to optimize recruitment by automating key tasks such as CV classification, matching with job descriptions, and interview management.

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
cd C:\Users\ramib\OneDrive\Bureau\CV_RH\functions\mcp-use
.\mcp_env\Scripts\Activate.ps1
```

Once activated:

```powershell
cd C:\Users\ramib\OneDrive\Bureau\CV_RH\functions
uvicorn main:app --reload
```

#### 3. In a separate terminal, launch the frontend (Python 3.10):

```powershell
cd C:\Users\ramib\OneDrive\Bureau\CV_RH\frontend
streamlit run app.py
```

> ✅ Make sure to configure Gmail access and API keys if email fetching is used.

---

## ✅ Status

🧪 Project under active development. Contributions, ideas, and feedback are welcome.

---

## 📎 Demo

A short demo video of the platform in action is available.  
All emails shown in the video are invalid and used purely for privacy purposes.

---

## 📂 Repository Structure (Simplified)

```
CV_RH/
├── frontend/               # Streamlit UI
│   └── app.py
├── functions/              # API & Agents
│   ├── main.py             # FastAPI app
│   ├── classifier.py       # CV classification logic
│   └── recommender.py      # JD matching & scoring
├── mcp-use/                # MCP integration (external)
├── google-workspace-mcp-server/  # Google API agent
└── README.md
```

---

## 📫 Contact

For collaboration or feedback, feel free to connect via [LinkedIn](https://www.linkedin.com/in/rami-ben-amor).

---

