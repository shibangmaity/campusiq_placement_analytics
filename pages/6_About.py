import streamlit as st
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from theme import apply_theme, page_header

st.set_page_config(page_title="About | CampusIQ", page_icon="📖", layout="wide")
apply_theme()

INSTITUTION_NAME = os.environ.get("INSTITUTION_NAME", "Student Intelligence")
INSTITUTION_YEAR = os.environ.get("INSTITUTION_YEAR", "2026")

st.markdown("""
<style>
    .about-card {
        background: rgba(255,255,255,0.025); border: 1px solid rgba(255,255,255,0.07);
        border-radius: 16px; padding: 1.4rem 1.5rem; margin-bottom: 1.2rem;
    }
    .about-card h3 {
        font-size: 1.0rem; font-weight: 700; color: #e2e8f0; margin: 0 0 0.6rem;
    }
    .about-card p {
        font-size: 0.88rem; color: #64748b; line-height: 1.7; margin: 0;
    }
    .module-row {
        display: flex; align-items: flex-start; gap: 12px;
        padding: 0.7rem 0; border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    .module-row:last-child { border-bottom: none; }
    .module-icon { font-size: 1.2rem; margin-top: 2px; }
    .module-name { font-size: 0.9rem; font-weight: 700; color: #e2e8f0; margin-bottom: 2px; }
    .module-desc { font-size: 0.82rem; color: #64748b; line-height: 1.55; }
    .chip-row { display:flex; flex-wrap:wrap; gap:0.45rem; }
    .stack-chip {
        background: rgba(139,92,246,0.10); border: 1px solid rgba(139,92,246,0.25);
        border-radius: 999px; padding: 5px 14px; font-size: 0.78rem; color: #c4b5fd;
    }
    .credit-row {
        display: flex; justify-content: space-between; align-items: center;
        padding: 0.6rem 0; border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    .credit-row:last-child { border-bottom: none; }
    .credit-name { font-size: 0.88rem; color: #e2e8f0; font-weight: 600; }
    .credit-role { font-size: 0.78rem; color: #64748b; }
    .stat-mini {
        display: inline-block; background: rgba(96,165,250,0.10);
        border: 1px solid rgba(96,165,250,0.25); border-radius: 8px;
        padding: 4px 12px; font-size: 0.8rem; color: #93c5fd; margin: 3px 6px 3px 0;
    }
</style>
""", unsafe_allow_html=True)

page_header("📖", "About CampusIQ", "What this platform is, how it works, and who built it.", color="#93c5fd")

# ── What it is ──────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="about-card">
    <h3>🎓 What is CampusIQ?</h3>
    <p>
    CampusIQ is an AI-powered student success platform built for {INSTITUTION_NAME}'s
    placement and academic ecosystem. It brings together natural-language data
    querying, visual analytics, early risk detection, and AI-driven career guidance
    into a single dashboard — so students, faculty, and the placement cell can all
    ask the same question in plain English and get a straight answer, instead of
    digging through spreadsheets.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Modules ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="about-card">
    <h3>🧩 What's inside</h3>
    <div class="module-row">
        <div class="module-icon">💬</div>
        <div>
            <div class="module-name">Ask Anything</div>
            <div class="module-desc">Type a question in plain English — CampusIQ converts it to SQL, runs it, and explains the result back to you in a sentence.</div>
        </div>
    </div>
    <div class="module-row">
        <div class="module-icon">📊</div>
        <div>
            <div class="module-name">Analytics Dashboard</div>
            <div class="module-desc">CGPA trends, attendance by branch, placement rates, backlog status, and top certifications — filterable by branch and semester.</div>
        </div>
    </div>
    <div class="module-row">
        <div class="module-icon">⚠️</div>
        <div>
            <div class="module-name">Risk Radar</div>
            <div class="module-desc">A transparent, weighted risk score built from CGPA, attendance, backlogs, internship progress, project count, and certifications — flags students who may need support before outcomes happen, not after.</div>
        </div>
    </div>
    <div class="module-row">
        <div class="module-icon">🤖</div>
        <div>
            <div class="module-name">Career Coach</div>
            <div class="module-desc">A RAG-powered AI counsellor for placement prep, resume tips, and career-path questions, grounded in a curated knowledge base.</div>
        </div>
    </div>
    <div class="module-row">
        <div class="module-icon">🎯</div>
        <div>
            <div class="module-name">Placement Predictor</div>
            <div class="module-desc">A GenAI-reasoned placement outlook — enter CGPA, backlog, internship status, projects, branch, and a freely-typed certification to get a placement probability, risk level, tailored suggestions, and likely companies & roles.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Dataset ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="about-card">
    <h3>📁 The data behind it</h3>
    <p style="margin-bottom:0.8rem;">
    CampusIQ runs on a 600-student dataset spanning academics, admissions, attendance,
    certifications, internships, and placement outcomes.
    </p>
    <span class="stat-mini">600 students</span>
    <span class="stat-mini">21 fields</span>
    <span class="stat-mini">B.Tech · Diploma · BCA · M.Tech · MCA · B.Sc · M.Sc</span>
</div>
""", unsafe_allow_html=True)

# ── Tech stack ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="about-card">
    <h3>🛠️ Built with</h3>
    <div class="chip-row">
        <span class="stack-chip">Streamlit</span>
        <span class="stack-chip">PostgreSQL</span>
        <span class="stack-chip">Groq · Llama 3.3</span>
        <span class="stack-chip">ChromaDB (RAG)</span>
        <span class="stack-chip">Plotly</span>
        <span class="stack-chip">scikit-learn</span>
        <span class="stack-chip">pandas</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Credits ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="about-card">
    <h3>👥 Created by</h3>
    <div class="credit-row">
        <span class="credit-name">Shibang Maity</span>
        <span class="credit-role">Lead Developer</span>
    </div>
    <div class="credit-row">
        <span class="credit-name">Roshan Panda </span>
        <span class="credit-role">System Architect</span>
    </div>
    <div class="credit-row">
        <span class="credit-name">Priyanshu Sekhar Bhuyan </span>
        <span class="credit-role">ML Model Developer</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="text-align:center; color:#334155; font-size:0.75rem; padding-top:1rem;">
    CampusIQ · {INSTITUTION_NAME} · {INSTITUTION_YEAR}
</div>
""", unsafe_allow_html=True)