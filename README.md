# 🎓 CampusIQ — AI Student Success Platform

> An AI-powered platform for KIIT University combining Natural Language Analytics, ML-based placement/risk prediction, and a RAG-powered career counselor — built on a real 600-student dataset.

🔗 **Live App:** [campusiqplacementanalytics.streamlit.app](https://campusiqplacementanalytics.streamlit.app/)

---

## 👥 Team

| Name | Role |
|---|---|
| Shibang Maity | Lead Developer |
| Roshan Panda | System Architect |
| Priyanshu Sekhar Bhuyan | ML Model Developer |

**Institution:** KIIT University

---

## 🧩 Modules

| Page | What it does |
|---|---|
| **Ask Anything** | Natural language → SQL, run live against the dataset, plain-English explanation of results |
| **Analytics Dashboard** | CGPA trends, attendance by branch, placement rate, backlog status, top certifications — filterable |
| **Risk Radar** | Transparent, weighted risk score (CGPA, Attendance, Backlog, Internship Status, Projects, Certification) — flags at-risk students *before* outcomes happen, validated against real placement rates |
| **Career Coach** | RAG-powered chatbot for placement prep, resume tips, and career-path questions |
| **Placement Predictor** | GenAI-reasoned placement outlook for any student profile — placement probability, risk level, live-judged certification strength, and likely companies & roles |
| **About** | Project overview, tech stack, credits |

---

## 📊 Dataset

`CampusIQ_Final_Dataset_Presentation.csv` — 600 real student records, 21 fields spanning academics (10th/12th marks, CGPA), attendance, backlog status, certifications, internships, projects, and placement outcomes across B.Tech, Diploma, BCA, M.Tech, MCA, B.Sc, and M.Sc streams.

**Design principle:** `Placement_Status` is only ever used as a training/validation *label* — never as an input feature — in both Risk Radar and Placement Predictor, to avoid leaking the outcome into the prediction.

---

## 🚀 Local Setup

### 1. Clone the repo
```bash
git clone https://github.com/shibangmaity/campusiq_placement_analytics.git
cd campusiq_placement_analytics
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set environment variables
Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
DB_HOST=your_postgres_host
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_PORT=5432
```
Postgres is hosted on [Neon](https://neon.tech) (free tier) for this project — grab your connection details from your Neon project dashboard.

### 4. Load the dataset into Postgres
```bash
python database/seed_data.py
```

### 5. Run the app
```bash
streamlit run App.py
```

---

## 📁 Project Structure
```
campusiq_placement_analytics/
├── App.py                          # Main entry point
├── theme.py                        # Dark theme + shared UI helpers
├── seed_data.py                    # Loads the real CSV into Postgres
├── .streamlit/
│   └── config.toml                 # Native Streamlit theme config
├── pages/
│   ├── 1_Ask_Anything.py           # NL → SQL interface
│   ├── 2_Analytics_Dashboard.py    # Charts & KPIs
│   ├── 3_Risk_Radar.py             # Weighted risk scoring
│   ├── 4_Career_Coach.py           # RAG chatbot
│   ├── 5_Placement_Predictor.py    # GenAI placement reasoning
│   └── 6_About.py                  # Project info & credits
├── nl2sql/
│   └── engine.py                   # Groq NL→SQL engine
├── database/
│   ├── db.py                       # DB connection + normalized sample data
│   ├── schema.sql                  # Table schema
│   └── CampusIQ_Final_Dataset_Presentation.csv
├── notebook/                       # ML training notebook (model development)
├── requirements.txt
└── .env                             # Not committed — see .gitignore
```

---

## 🔑 Getting a Groq API Key
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up / log in
3. Create an API key → paste into `.env`

---

## 🌐 Deploying on Streamlit Cloud
1. Push code to GitHub (`.env` stays out via `.gitignore`)
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Select the repo, set **Main file path** to `App.py`
4. Under **Advanced settings → Secrets**, paste your env vars in TOML format:
   ```toml
   GROQ_API_KEY = "..."
   DB_HOST = "..."
   DB_NAME = "..."
   DB_USER = "..."
   DB_PASSWORD = "..."
   DB_PORT = "5432"
   ```
5. Deploy

---

## 🛠️ Tech Stack
- **Frontend:** Streamlit
- **LLM:** LLaMA 3.3 70B via Groq
- **Vector DB:** ChromaDB (RAG)
- **Database:** PostgreSQL (Neon)
- **ML:** scikit-learn (Logistic Regression, Random Forest, Decision Tree, KNN, SVM)
- **Charts:** Plotly
- **Deployment:** Streamlit Community Cloud
