# 🎓 CampusIQ — AI Student Success Platform

> An AI-powered platform for KIIT University that combines Natural Language Analytics, ML-based risk prediction, and a RAG career counselor.

---

## 👥 Team Split

| Module | Owner | Tech |
|--------|-------|------|
| NL→SQL + Analytics Dashboard | Shibang | Groq, LLaMA, Streamlit, Plotly |
| Student Risk Prediction | P2 | Scikit-learn, Pandas, Streamlit |
| Career Counselor Chatbot | Shibang | ChromaDB, Groq, LLaMA, Streamlit |
| DB Setup + Data Pipeline | P3 | PostgreSQL, psycopg2, CSV |

---

## 🚀 Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/campusiq.git
cd campusiq
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set environment variables
Create a `.env` file:
```
GROQ_API_KEY=your_groq_api_key_here
DB_HOST=localhost
DB_NAME=campusiq
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432
```

### 4. Run the app
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
campusiq/
├── app.py                        # Main entry point
├── pages/
│   ├── 1_Ask_Anything.py         # NL→SQL interface (Shibang)
│   ├── 2_Analytics_Dashboard.py  # Charts & KPIs (Shibang)
│   ├── 3_Student_Risk.py         # ML risk model (P2)
│   └── 4_Career_Coach.py         # RAG chatbot (Shibang)
├── nl2sql/
│   └── engine.py                 # Groq NL→SQL engine
├── rag/
│   └── (ChromaDB handled in page)
├── database/
│   └── db.py                     # DB connection + sample data
├── data/                         # CSV datasets (P3 adds here)
└── requirements.txt
```

---

## 🔑 Getting Groq API Key
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up / Login
3. Create API key → copy to `.env`

---

## 🌐 Deploying on Streamlit Cloud
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repo → set secrets (GROQ_API_KEY etc.)
4. Deploy!

---

## 📊 Tech Stack
- **Frontend**: Streamlit
- **LLM**: LLaMA 3.3 70B via Groq
- **Vector DB**: ChromaDB
- **Database**: PostgreSQL
- **ML**: Scikit-learn
- **Charts**: Plotly
- **Deployment**: Streamlit Cloud
