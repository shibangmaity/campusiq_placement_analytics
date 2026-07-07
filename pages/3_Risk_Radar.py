import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db import run_query
from theme import apply_theme, page_header, PLOTLY_PALETTE, plotly_layout

st.set_page_config(page_title="Risk Radar | CampusIQ", page_icon="⚠️", layout="wide")
apply_theme()

st.markdown("""
<style>
    .kpi-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(244,63,94,0.18);
        border-radius: 14px; padding: 1.3rem 1.2rem; text-align: center;
        transition: border-color 0.2s, transform 0.2s;
    }
    .kpi-card:hover { border-color: rgba(244,63,94,0.45); transform: translateY(-2px); }
    .kpi-value {
        font-size: 2rem; font-weight: 800; line-height: 1;
        background: linear-gradient(135deg, #fb7185, #fbbf24);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .kpi-label { font-size: 0.78rem; color: #64748b; margin-top: 0.5rem; font-weight: 600; letter-spacing: 0.02em; }
    .chart-card {
        background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px; padding: 1.2rem 1.2rem 0.4rem; margin-bottom: 1rem;
    }
    .chart-title { font-size: 0.92rem; font-weight: 700; color: #cbd5e1; margin-bottom: 0.6rem; }
    .section-label {
        font-size: 0.78rem; font-weight: 700; letter-spacing: 0.04em;
        color: #94a3b8; text-transform: uppercase; margin: 0.3rem 0 0.7rem;
    }
    .risk-badge {
        display:inline-block; padding: 2px 10px; border-radius: 999px;
        font-size: 0.72rem; font-weight: 700;
    }
    .risk-high { background: rgba(244,63,94,0.16); color: #fb7185; }
    .risk-medium { background: rgba(251,191,36,0.16); color: #fbbf24; }
    .risk-low { background: rgba(52,211,153,0.16); color: #34d399; }
    .note-box {
        background: rgba(96,165,250,0.07); border: 1px solid rgba(96,165,250,0.20);
        border-radius: 10px; padding: 0.9rem 1.2rem; font-size: 0.85rem;
        color: #94a3b8; line-height: 1.6; margin: 0.5rem 0 1.2rem;
    }
    /* Streamlit's default inline-code style is a near-white box — override
       it here so `Placement_Status`-style badges match the dark theme. */
    code {
        background: rgba(167,139,250,0.15) !important;
        color: #c4b5fd !important;
        padding: 2px 7px !important;
        border-radius: 5px !important;
        font-size: 0.85em !important;
    }
</style>
""", unsafe_allow_html=True)

page_header("⚠️", "Risk Radar", "Flags students likely to struggle — before outcomes happen, not after.", color="#fb7185")

st.markdown("""
<div class="note-box">
📌 <b>Design note:</b> This score is built only from <b>CGPA, Attendance %, Backlog, Internship Status,
Projects Count, and Top Certification</b> — signals known <i>before</i> placement season.
<code>Placement_Status</code> is deliberately excluded from the score itself (using it would leak the
answer into the prediction). It only appears further down, to check whether high-risk students really
did end up less likely to be placed.
</div>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
# Always queries the live database — the "Use sample data" toggle has been
# removed, so this page requires DB_HOST/DB_NAME/DB_USER/DB_PASSWORD to be
# configured (see database/db.py). run_query() normalizes column names to
# lower_snake_case for the students table.
students = run_query("SELECT * FROM students")


# ============================================================
# RISK SCORING — transparent, weighted, out of 100
# ============================================================
def compute_risk(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # CGPA — up to 30 pts. Lower CGPA = higher risk.
    df["cgpa_risk"] = ((10 - df["cgpa"]).clip(lower=0) / 10 * 30).round(1)

    # Attendance — up to 25 pts. Below-75% students carry most of the weight here.
    df["attendance_risk"] = ((100 - df["attendance_percent"]).clip(lower=0) / 100 * 25).round(1)

    # Backlog — up to 20 pts.
    backlog_map = {"No": 0.0, "Yes (Cleared)": 0.5, "Yes": 1.0}
    df["backlog_risk"] = (df["backlog"].map(backlog_map).fillna(0.5) * 20).round(1)

    # Internship progress — up to 10 pts. No movement yet = higher risk.
    internship_map = {"Completed": 0.0, "Ongoing": 0.3, "Not Yet": 1.0}
    df["internship_risk"] = (df["internship_status"].map(internship_map).fillna(0.5) * 10).round(1)

    # Projects — up to 10 pts. Fewer than 3 projects raises risk.
    df["projects_risk"] = ((3 - df["projects_count"]).clip(lower=0) / 3 * 10).round(1)

    # Certification — up to 5 pts. No certification at all is a flag.
    df["certification_risk"] = np.where(df["top_certification"] == "No Certification", 5.0, 0.0)

    df["risk_score"] = (
        df["cgpa_risk"] + df["attendance_risk"] + df["backlog_risk"]
        + df["internship_risk"] + df["projects_risk"] + df["certification_risk"]
    ).round(1)

    def bucket(score):
        if score >= 55:
            return "High"
        elif score >= 30:
            return "Medium"
        return "Low"
    df["risk_level"] = df["risk_score"].apply(bucket)

    factor_labels = {
        "cgpa_risk": "Low CGPA",
        "attendance_risk": "Low Attendance",
        "backlog_risk": "Backlog",
        "internship_risk": "No Internship Progress",
        "projects_risk": "Few Projects",
        "certification_risk": "No Certification",
    }
    df["top_risk_factor"] = df[list(factor_labels.keys())].idxmax(axis=1).map(factor_labels)

    return df

scored = compute_risk(students)

# ── Filters ───────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
with col1:
    branch_filter = st.multiselect("Branch", sorted(scored["branch"].unique()), default=list(scored["branch"].unique()))
with col2:
    sem_filter = st.multiselect("Semester", sorted(scored["semester"].unique()), default=list(scored["semester"].unique()))
with col3:
    risk_filter = st.multiselect("Risk Level", ["High", "Medium", "Low"], default=["High", "Medium", "Low"])

filtered = scored[
    (scored["branch"].isin(branch_filter)) &
    (scored["semester"].isin(sem_filter)) &
    (scored["risk_level"].isin(risk_filter))
]

st.markdown("<br>", unsafe_allow_html=True)

# ── KPI Row ───────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-value">{(filtered['risk_level'] == 'High').sum()}</div>
        <div class="kpi-label">HIGH RISK STUDENTS</div>
    </div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-value">{(filtered['risk_level'] == 'Medium').sum()}</div>
        <div class="kpi-label">MEDIUM RISK</div>
    </div>""", unsafe_allow_html=True)
with k3:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-value">{(filtered['risk_level'] == 'Low').sum()}</div>
        <div class="kpi-label">LOW RISK</div>
    </div>""", unsafe_allow_html=True)
with k4:
    avg_score = filtered["risk_score"].mean() if len(filtered) else 0
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-value">{avg_score:.1f}</div>
        <div class="kpi-label">AVG RISK SCORE / 100</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Charts Row 1 ──────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-card"><div class="chart-title">Risk Level Distribution</div>', unsafe_allow_html=True)
    level_counts = filtered["risk_level"].value_counts().reindex(["High", "Medium", "Low"]).fillna(0).reset_index()
    level_counts.columns = ["risk_level", "count"]
    fig1 = px.bar(
        level_counts, x="risk_level", y="count", color="risk_level",
        color_discrete_map={"High": "#fb7185", "Medium": "#fbbf24", "Low": "#34d399"},
        text_auto=True, category_orders={"risk_level": ["High", "Medium", "Low"]},
    )
    fig1 = plotly_layout(fig1)
    fig1.update_traces(marker_line_width=0, textposition="outside", textfont=dict(color="#94a3b8", size=11))
    fig1.update_layout(height=320, showlegend=False, xaxis_title="", yaxis_title="")
    st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-card"><div class="chart-title">CGPA vs Attendance (colored by risk)</div>', unsafe_allow_html=True)
    fig2 = px.scatter(
        filtered, x="cgpa", y="attendance_percent", color="risk_level",
        color_discrete_map={"High": "#fb7185", "Medium": "#fbbf24", "Low": "#34d399"},
        hover_data=["name", "branch", "risk_score"] if "name" in filtered.columns else ["branch", "risk_score"],
        category_orders={"risk_level": ["High", "Medium", "Low"]},
    )
    fig2 = plotly_layout(fig2)
    fig2.update_traces(marker=dict(size=8, opacity=0.75))
    fig2.update_layout(height=320, xaxis_title="CGPA", yaxis_title="Attendance %")
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ── Charts Row 2 — top driver + validation ─────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.markdown('<div class="chart-card"><div class="chart-title">Top Risk Driver (High-Risk Students)</div>', unsafe_allow_html=True)
    high_risk = filtered[filtered["risk_level"] == "High"]
    if len(high_risk):
        driver_counts = high_risk["top_risk_factor"].value_counts().reset_index()
        driver_counts.columns = ["factor", "count"]
        fig3 = px.bar(
            driver_counts.sort_values("count"), x="count", y="factor", orientation="h",
            color_discrete_sequence=["#fb7185"], text_auto=True,
        )
        fig3 = plotly_layout(fig3)
        fig3.update_traces(marker_line_width=0, textposition="outside", textfont=dict(color="#94a3b8", size=11))
        fig3.update_layout(height=300, xaxis_title="", yaxis_title="")
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
    else:
        st.caption("No high-risk students in the current filter.")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="chart-card"><div class="chart-title">Validation — Placement Rate by Risk Level</div>', unsafe_allow_html=True)
    st.caption("Placement_Status was NOT used to compute risk. Shown here only to check the score against real outcomes.")
    val = filtered.groupby("risk_level")["placed"].mean().reindex(["High", "Medium", "Low"]) * 100
    val = val.reset_index()
    val.columns = ["risk_level", "placement_rate"]
    fig4 = px.bar(
        val, x="risk_level", y="placement_rate", color="risk_level",
        color_discrete_map={"High": "#fb7185", "Medium": "#fbbf24", "Low": "#34d399"},
        text_auto=".1f", category_orders={"risk_level": ["High", "Medium", "Low"]},
    )
    fig4 = plotly_layout(fig4)
    fig4.update_traces(marker_line_width=0, textposition="outside", textfont=dict(color="#94a3b8", size=11))
    fig4.update_layout(height=300, showlegend=False, xaxis_title="", yaxis_title="% Placed")
    st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ── High-Risk Student Table ──────────────────────────────────────────────────
st.divider()
st.markdown('<div class="section-label">Flagged Students (sorted by risk score)</div>', unsafe_allow_html=True)
name_col = "name" if "name" in filtered.columns else "student_name"
display_cols = [name_col, "branch", "semester", "cgpa", "attendance_percent", "backlog",
                 "internship_status", "projects_count", "top_certification",
                 "risk_score", "risk_level", "top_risk_factor"]
st.dataframe(
    filtered[display_cols].sort_values("risk_score", ascending=False),
    use_container_width=True, hide_index=True
)

with st.expander("How is the risk score calculated?"):
    st.markdown("""
    Each student gets points added from six factors (max 100):

    | Factor | Max Points | Logic |
    |---|---|---|
    | CGPA | 30 | Lower CGPA → more points |
    | Attendance % | 25 | Lower attendance → more points |
    | Backlog | 20 | `Yes` = full points, `Yes (Cleared)` = half, `No` = 0 |
    | Internship Status | 10 | `Not Yet` = full points, `Ongoing` = partial, `Completed` = 0 |
    | Projects Count | 10 | Fewer than 3 projects → points scale up |
    | Top Certification | 5 | `No Certification` = full points, else 0 |

    **Score ≥ 55 → High risk · 30–54 → Medium risk · < 30 → Low risk**

    `Placement_Status` is intentionally excluded from this table — it's an outcome, not a
    predictor, and including it would leak the answer into the score.
    """)