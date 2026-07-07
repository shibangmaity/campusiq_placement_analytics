import streamlit as st
import pandas as pd
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db import get_sample_data
from theme import apply_theme, page_header

st.set_page_config(page_title="Placement Predictor | CampusIQ", page_icon="🎯", layout="wide")
apply_theme()

st.markdown("""
<style>
    .result-card {
        background: rgba(255,255,255,0.03); border: 1px solid rgba(139,92,246,0.20);
        border-radius: 16px; padding: 1.5rem; text-align: center;
    }
    .prob-value {
        font-size: 2.6rem; font-weight: 800; line-height: 1;
        background: linear-gradient(135deg, #34d399, #60a5fa);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .prob-label { font-size: 0.78rem; color: #64748b; margin-top: 0.5rem; font-weight: 600; letter-spacing: 0.03em; }
    .risk-pill {
        display:inline-block; padding: 4px 14px; border-radius: 999px;
        font-size: 0.85rem; font-weight: 700; margin-top: 0.5rem;
    }
    .risk-high { background: rgba(244,63,94,0.16); color: #fb7185; }
    .risk-medium { background: rgba(251,191,36,0.16); color: #fbbf24; }
    .risk-low { background: rgba(52,211,153,0.16); color: #34d399; }
    .suggestion-item {
        background: rgba(96,165,250,0.06); border-left: 3px solid #60a5fa;
        border-radius: 0 10px 10px 0; padding: 0.6rem 1rem; margin-bottom: 0.5rem;
        font-size: 0.86rem; color: #cbd5e1;
    }
    .company-row {
        display: flex; justify-content: space-between; align-items: center;
        padding: 0.6rem 0.9rem; background: rgba(255,255,255,0.02);
        border-radius: 10px; margin-bottom: 0.5rem;
    }
    .company-name { font-size: 0.9rem; font-weight: 700; color: #e2e8f0; }
    .company-role { font-size: 0.76rem; color: #64748b; }
    .company-match { font-size: 0.78rem; color: #a78bfa; font-weight: 700; max-width: 45%; text-align: right; }
    .model-note {
        background: rgba(167,139,250,0.06); border: 1px solid rgba(167,139,250,0.18);
        border-radius: 10px; padding: 0.8rem 1.1rem; font-size: 0.82rem;
        color: #94a3b8; line-height: 1.6; margin-bottom: 1.2rem;
    }
    .cert-badge {
        background: rgba(167,139,250,0.06); border: 1px solid rgba(167,139,250,0.18);
        border-radius: 10px; padding: 0.8rem 1.1rem; font-size: 0.85rem;
        color: #cbd5e1; margin-top: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

page_header(
    "🎯", "Placement Predictor",
    "AI-reasoned placement outlook for a student profile — powered by GenAI, not a fixed dataset lookup.",
    color="#34d399",
)

st.markdown("""
<div class="model-note">
🤖 This page uses <b>Generative AI</b> (same engine as Career Coach) to reason about the profile
you enter — CGPA, Attendance, Backlog, Internship Status, Projects Count, Branch, and a
freely-typed certification. There is no fixed company list and no trained ML model: the AI
evaluates certification strength on the spot and estimates placement odds, risk, likely
companies, and roles from its own knowledge of hiring patterns.
</div>
""", unsafe_allow_html=True)

# ── Branch options pulled from existing dataset, purely for the dropdown ──────
@st.cache_data
def get_branches():
    try:
        df = get_sample_data()["students"]
        return sorted(df["branch"].dropna().unique().tolist())
    except Exception:
        return ["CSE", "ECE", "Mechanical", "Civil", "IT", "EEE"]

branch_options = get_branches()

# ── Input form ────────────────────────────────────────────────────────────────
st.markdown("#### Enter a student profile")

col1, col2, col3 = st.columns(3)
with col1:
    cgpa = st.slider("CGPA", 0.0, 10.0, 7.5, 0.05)
    branch = st.selectbox("Branch", branch_options)
with col2:
    backlog = st.selectbox("Backlog", ["No", "Yes (Cleared)", "Yes"])
    internship = st.selectbox("Internship Status", ["Not Yet", "Ongoing", "Completed"])
with col3:
    projects = st.number_input("Projects Count", min_value=0, max_value=10, value=2, step=1)
    has_cert_input = st.radio("Certification?", ["No", "Yes"], horizontal=True)

custom_cert_name = ""
if has_cert_input == "Yes":
    custom_cert_name = st.text_input(
        "Certification name — include the issuing company/platform if you know it",
        placeholder="e.g. AWS Certified Cloud Practitioner, Coursera – Python for Everybody, NPTEL DBMS"
    )
    st.caption("The AI judges this on the spot — whether it's a real issuer-backed certification, how strong it is, and whether it actually helps placement, even if it's not in any predefined list.")

predict_btn = st.button("🎯 Predict Placement Outcome", type="primary", use_container_width=True)

# ── Single GenAI call that does everything ────────────────────────────────────
def get_ai_prediction(profile: dict) -> dict:
    """Ask the LLM to reason over the whole profile and return a structured
    prediction: probability, risk, certification evaluation, suggestions,
    and likely companies + roles. No dataset, no ML model — pure GenAI reasoning."""
    prompt = f"""You are an expert Indian campus placement counselor. Reason about this
student profile the way a placement cell expert would, using your general knowledge of
how companies hire on Indian campuses.

Student profile:
- CGPA: {profile['cgpa']}/10
- Branch: {profile['branch']}
- Backlog: {profile['backlog']}
- Internship Status: {profile['internship']}
- Projects Count: {profile['projects']}
- Certification typed by student: "{profile['cert_name']}" (if empty, student has no certification)

Tasks:
1. Evaluate the certification (if any): is it a real issuer-backed certification (has a
   named company/platform behind it), how strong/recognized is it (tier 1-4, where 4 =
   globally recognized like AWS/Google/Microsoft/Cisco), and does it meaningfully help
   placement odds for this branch. If the student typed something vague like just a
   subject name with no issuer, say so honestly.
2. Estimate an overall Placement Probability (0-100) and Risk Level (Low/Medium/High),
   reasoning holistically about CGPA, backlog, internship, projects, branch, and
   certification strength together — not from any fixed formula.
3. Give 3-5 short, specific, actionable suggestions to improve this profile's placement
   odds, referencing the actual weak points in the profile.
4. Predict 3-4 companies likely to hire this profile on Indian campuses, each with a
   specific likely role (not just "Software Engineer" — be specific where possible,
   e.g. SDE-1, Systems Engineer, Graduate Engineer Trainee, Data Analyst) and a short
   one-line reason tied to this profile. Base this on realistic hiring patterns for this
   CGPA/branch/project/cert combination, not a fixed list. Vary companies by branch
   (e.g. core companies for Mechanical/Civil, product/service companies for CSE/IT).

Return ONLY a JSON object with exactly this shape, no markdown, no backticks, no extra text:
{{
  "placement_probability": <int 0-100>,
  "risk_level": "<Low|Medium|High>",
  "certification": {{
    "entered": <true/false>,
    "is_recognized": <true/false>,
    "tier": <int 0-4>,
    "helps_placement": <true/false>,
    "verdict": "<one short sentence, under 20 words>"
  }},
  "suggestions": ["<suggestion 1>", "<suggestion 2>", "..."],
  "likely_companies": [
    {{"company": "<name>", "role": "<specific role>", "reason": "<short reason, under 15 words>"}}
  ]
}}"""
    try:
        from groq import Groq
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=900,
        )
        raw = response.choices[0].message.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(raw)
    except Exception as e:
        st.error(f"AI prediction failed — please try again. ({e})")
        return None

if predict_btn:
    profile = {
        "cgpa": cgpa,
        "branch": branch,
        "backlog": backlog,
        "internship": internship,
        "projects": projects,
        "cert_name": custom_cert_name.strip() if has_cert_input == "Yes" else "",
    }

    with st.spinner("AI is analyzing this profile..."):
        result = get_ai_prediction(profile)

    if result:
        prob = max(0, min(100, int(result.get("placement_probability", 50))))

        # Risk level is derived from probability in code, not taken from the
        # LLM's own risk_level field — the model can drift (e.g. say "Medium"
        # even when it also says 80%), so this keeps the two always consistent.
        if prob >= 65:
            risk_level, risk_class = "Low", "risk-low"
        elif prob >= 35:
            risk_level, risk_class = "Medium", "risk-medium"
        else:
            risk_level, risk_class = "High", "risk-high"

        st.markdown("<br>", unsafe_allow_html=True)
        r1, r2 = st.columns(2)
        with r1:
            st.markdown(f"""
            <div class="result-card">
                <div class="prob-value">{prob}%</div>
                <div class="prob-label">PLACEMENT PROBABILITY</div>
            </div>
            """, unsafe_allow_html=True)
        with r2:
            st.markdown(f"""
            <div class="result-card">
                <div class="prob-label" style="margin-top:0;">RISK LEVEL</div>
                <div class="risk-pill {risk_class}">{risk_level}</div>
            </div>
            """, unsafe_allow_html=True)

        cert = result.get("certification", {})
        if cert.get("entered"):
            badge = "✅ Recognized & helps placement" if cert.get("helps_placement") else "⚠️ Limited placement impact"
            st.markdown(f"""
            <div class="cert-badge">
                <b>{badge}</b> — Tier {cert.get('tier', 0)}/4. {cert.get('verdict', '')}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### Suggestions")
        for s in result.get("suggestions", []):
            st.markdown(f'<div class="suggestion-item">💡 {s}</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### Likely Companies & Roles")
        st.caption("AI-predicted from typical Indian campus hiring patterns for this profile — not guaranteed offers.")
        for c in result.get("likely_companies", []):
            st.markdown(f"""
            <div class="company-row">
                <div>
                    <div class="company-name">{c.get('company', '')}</div>
                    <div class="company-role">Likely role: {c.get('role', '')}</div>
                </div>
                <div class="company-match">{c.get('reason', '')}</div>
            </div>
            """, unsafe_allow_html=True)

with st.expander("How does this work?"):
    st.markdown("""
    This page is fully **GenAI-powered** — the same approach used in Career Coach.

    One AI call reasons over your entire profile (CGPA, Branch, Backlog, Internship
    Status, Projects Count, and a freely-typed Certification) and returns:

    - **Placement Probability & Risk Level** — the AI's holistic judgment, not a fixed
      formula or trained model.
    - **Certification strength** — evaluated live, even if the certification isn't in
      any predefined list. The AI infers whether it's issuer-backed, how recognized it
      is, and whether it actually helps placement.
    - **Suggestions** — specific, tied to the weak points in your actual profile.
    - **Likely Companies & Roles** — predicted from general hiring-pattern knowledge for
      your branch and profile strength, not matched against a dataset.

    Nothing here is looked up from a fixed company list or trained on historical
    placement records — every field is reasoned live by the AI.
    """)