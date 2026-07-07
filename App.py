from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
from theme import apply_theme

st.set_page_config(
    page_title="CampusIQ",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_theme()

# ── Institution branding (configurable per deployment) ────────────────────────
# Set these in your .env file to rebrand CampusIQ for any college:
#   INSTITUTION_NAME=KIIT University
#   INSTITUTION_YEAR=2025
INSTITUTION_NAME = os.environ.get("INSTITUTION_NAME", "Student Intelligence")
INSTITUTION_YEAR = os.environ.get("INSTITUTION_YEAR", "2026")

# ── Sidebar branding ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:1rem 0.6rem 1.5rem;">
        <div style="font-size:1.25rem; font-weight:800; letter-spacing:-0.01em;
                    background:linear-gradient(135deg,#c4b5fd 0%,#93c5fd 60%,#6ee7b7 100%);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text; margin-bottom:2px;">
            🎓 CampusIQ
        </div>
        <div style="font-size:0.65rem; color:#334155 !important; letter-spacing:0.10em;
                    text-transform:uppercase; font-weight:700;">
            """ + INSTITUTION_NAME + " · " + INSTITUTION_YEAR + """
        </div>
        <div style="margin-top:1.2rem; height:1px;
                    background:linear-gradient(90deg,rgba(139,92,246,0.30),transparent);"></div>
    </div>
    """, unsafe_allow_html=True)

# ── Extra CSS for the hero/stat strip/cards ───────────────────────────────────
st.markdown("""
<style>
.hero-wrap {
    position: relative; text-align: center; padding: 2.5rem 1rem 1.5rem;
    overflow: visible;
}
.hero-glow {
    position: absolute; top: -100px; left: 50%; transform: translateX(-50%);
    width: 800px; height: 420px;
    background: radial-gradient(ellipse at 40% 50%, rgba(139,92,246,0.20) 0%, rgba(59,130,246,0.12) 42%, transparent 68%);
    pointer-events: none; z-index: 0;
}
.badge {
    display:inline-flex; align-items:center; gap:7px;
    background:rgba(139,92,246,0.13); border:1px solid rgba(139,92,246,0.35);
    border-radius:999px; padding:5px 18px;
    font-size:0.67rem; font-weight:700; letter-spacing:0.11em;
    text-transform:uppercase; color:#a78bfa; margin-bottom:1.2rem;
    position: relative; z-index: 1;
}
.dot {
    width:6px; height:6px; border-radius:50%; background:#a78bfa;
    box-shadow:0 0 7px rgba(167,139,250,0.9);
    display:inline-block;
}
.hero-title {
    font-size:3.4rem; font-weight:800; line-height:1.03; letter-spacing:-0.03em;
    background:linear-gradient(135deg,#f8fafc 0%,#c4b5fd 32%,#93c5fd 62%,#6ee7b7 100%);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
    margin-bottom:0.7rem; position: relative; z-index: 1;
}
.hero-sub {
    font-size:0.96rem; color:#475569; max-width:430px;
    margin:0 auto 1.6rem; line-height:1.7; position: relative; z-index: 1;
}

.stat-box {
    background: rgba(255,255,255,0.025); border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px; text-align: center; padding: 1.1rem 0.5rem;
}
.stat-num { font-size: 1.5rem; font-weight: 700; color: #e2e8f0; line-height: 1; }
.stat-lbl { font-size: 0.62rem; color: #334155; font-weight: 700; letter-spacing: 0.09em; text-transform: uppercase; margin-top: 5px; }

/* Clickable module cards via st.page_link, restyled to look like cards */
div[data-testid="stPageLink"] {
    background: transparent !important;
    border: none !important;
    padding: 0 0.8rem !important;
    margin-bottom: 0 !important;
}
div[data-testid="stPageLink"] p {
    font-size: 1.0rem !important;
    font-weight: 700 !important;
    color: #f1f5f9 !important;
}
div[data-testid="stPageLink"]:hover p { color: #ffffff !important; }

.card-outer {
    border-radius: 16px !important;
    border: 1px solid rgba(255,255,255,0.07);
    background: rgba(255,255,255,0.025);
    transition: border-color 0.2s, background 0.2s, transform 0.2s, box-shadow 0.2s;
    overflow: hidden;
    margin-bottom: 1rem;
}
.card-outer:hover { transform: translateY(-3px); }
.card-purple:hover { border-color: rgba(139,92,246,0.65); background: rgba(139,92,246,0.07); box-shadow: 0 12px 36px rgba(139,92,246,0.14); }
.card-blue:hover   { border-color: rgba(59,130,246,0.65);  background: rgba(59,130,246,0.07);  box-shadow: 0 12px 36px rgba(59,130,246,0.14); }
.card-rose:hover   { border-color: rgba(244,63,94,0.65);   background: rgba(244,63,94,0.07);   box-shadow: 0 12px 36px rgba(244,63,94,0.13); }
.card-emerald:hover{ border-color: rgba(16,185,129,0.65);  background: rgba(16,185,129,0.07);  box-shadow: 0 12px 36px rgba(16,185,129,0.13); }
.card-amber:hover  { border-color: rgba(251,191,36,0.65);  background: rgba(251,191,36,0.07);  box-shadow: 0 12px 36px rgba(251,191,36,0.13); }

.card-icon-row { display:flex; align-items:center; gap:10px; padding: 1rem 0.8rem 0.5rem; }
.card-icon { font-size: 1.3rem; }
.card-tag {
    font-size: 0.60rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase;
    padding: 3px 10px; border-radius: 999px;
}
.tag-purple { background: rgba(139,92,246,0.18); color: #a78bfa; }
.tag-blue { background: rgba(59,130,246,0.18); color: #60a5fa; }
.tag-rose { background: rgba(244,63,94,0.18); color: #fb7185; }
.tag-emerald { background: rgba(16,185,129,0.18); color: #34d399; }
.tag-amber { background: rgba(251,191,36,0.18); color: #fbbf24; }
.card-desc { font-size: 0.81rem; color: #475569; line-height: 1.6; padding: 0.2rem 0.8rem 1.1rem; }

.section-lbl { font-size:0.65rem; font-weight:700; letter-spacing:0.11em; text-transform:uppercase; color:#1e3a5f; margin: 1.6rem 0 0.7rem; }
.chip-row { display:flex; flex-wrap:wrap; gap:0.45rem; margin-bottom: 1.6rem; }
.chip {
    background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08);
    border-radius:999px; padding:7px 16px; font-size:0.79rem; color:#475569;
}
.hint {
    display:flex; align-items:center; gap:10px;
    background:rgba(59,130,246,0.07); border:1px solid rgba(59,130,246,0.18);
    border-radius:10px; padding:0.8rem 1.2rem;
    font-size:0.84rem; color:#60a5fa; margin: 1rem 0 1.5rem;
}
.foot { text-align:center; color:#1e293b; font-size:0.72rem; padding-top:1.5rem; border-top:1px solid rgba(255,255,255,0.04); }
</style>
""", unsafe_allow_html=True)

# ── HERO ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-wrap">
    <div class="hero-glow"></div>
    <div class="badge"><span class="dot"></span> {INSTITUTION_NAME} · {INSTITUTION_YEAR}</div>
    <div class="hero-title">CampusIQ</div>
    <div class="hero-sub">AI-powered student success platform — from attendance to placements, all in one place.</div>
</div>
""", unsafe_allow_html=True)

# ── STATS STRIP ────────────────────────────────────────────────────────────────
# Reflects the real dataset (600 students, 21 fields), not the old fake seed.
s1, s2, s3, s4 = st.columns(4)
stats = [("600", "Students"), ("21", "Data Fields"), ("5", "AI Modules"), ("NL→SQL", "Query Engine")]
for col, (num, lbl) in zip([s1, s2, s3, s4], stats):
    with col:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-num">{num}</div>
            <div class="stat-lbl">{lbl}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── MODULE CARDS — real, clickable st.page_link ────────────────────────────────
# NOTE: adjust these paths/filenames to exactly match your pages/ folder
c1, c2 = st.columns(2)

with c1:
    st.markdown('<div class="card-outer card-purple">', unsafe_allow_html=True)
    st.markdown('<div class="card-icon-row"><span class="card-icon">💬</span><span class="card-tag tag-purple">NL → SQL</span></div>', unsafe_allow_html=True)
    st.page_link("pages/1_Ask_Anything.py", label="Ask Anything")
    st.markdown('<div class="card-desc">Type a question in plain English. Get instant SQL-powered answers from your student database.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="card-outer card-blue">', unsafe_allow_html=True)
    st.markdown('<div class="card-icon-row"><span class="card-icon">📊</span><span class="card-tag tag-blue">ANALYTICS</span></div>', unsafe_allow_html=True)
    st.page_link("pages/2_Analytics_Dashboard.py", label="Dashboard")
    st.markdown('<div class="card-desc">CGPA trends, branch breakdowns, attendance heatmaps, and placement KPIs — all visualised.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

c3, c4 = st.columns(2)

with c3:
    st.markdown('<div class="card-outer card-rose">', unsafe_allow_html=True)
    st.markdown('<div class="card-icon-row"><span class="card-icon">⚠️</span><span class="card-tag tag-rose">ML · RISK</span></div>', unsafe_allow_html=True)
    st.page_link("pages/3_Risk_Radar.py", label="Risk Radar")
    st.markdown('<div class="card-desc">Flags at-risk students early using CGPA, attendance, backlogs, internships, projects, and certifications.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c4:
    st.markdown('<div class="card-outer card-emerald">', unsafe_allow_html=True)
    st.markdown('<div class="card-icon-row"><span class="card-icon">🤖</span><span class="card-tag tag-emerald">RAG · AI</span></div>', unsafe_allow_html=True)
    st.page_link("pages/4_Career_Coach.py", label="Career Coach")
    st.markdown('<div class="card-desc">AI counsellor powered by RAG — gives personalised placement advice and career roadmaps.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

c5, c6 = st.columns(2)

with c5:
    st.markdown('<div class="card-outer card-amber">', unsafe_allow_html=True)
    st.markdown('<div class="card-icon-row"><span class="card-icon">🎯</span><span class="card-tag tag-amber">GENAI</span></div>', unsafe_allow_html=True)
    st.page_link("pages/5_Placement_Predictor.py", label="Placement Predictor")
    st.markdown('<div class="card-desc">AI-reasoned placement odds, risk level, and likely companies & roles for any student profile.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c6:
    st.empty()

# ── QUICK CHIPS ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-lbl">✦ Try asking →</div>', unsafe_allow_html=True)
st.markdown("""
<div class="chip-row">
    <div class="chip">Top 10 CSE students by CGPA</div>
    <div class="chip">Average attendance by branch</div>
    <div class="chip">Students with active backlogs</div>
    <div class="chip">Students placed at TCS</div>
    <div class="chip">Students with no certifications</div>
    <div class="chip">Placement rate by stream</div>
</div>
""", unsafe_allow_html=True)

# ── NAV HINT + FOOTER ───────────────────────────────────────────────────────────
st.markdown('<div class="hint">👈 Use the sidebar to navigate between modules</div>', unsafe_allow_html=True)
st.markdown(f'<div class="foot">Built with ♥ by Team CampusIQ &nbsp;·&nbsp; {INSTITUTION_NAME} {INSTITUTION_YEAR}</div>', unsafe_allow_html=True)