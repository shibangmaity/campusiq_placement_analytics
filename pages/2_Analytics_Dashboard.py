import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db import get_sample_data, run_query
from theme import apply_theme, page_header, PLOTLY_PALETTE, plotly_layout

st.set_page_config(page_title="Analytics | CampusIQ", page_icon="📊", layout="wide")
apply_theme()

st.markdown("""
<style>
    .kpi-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(139,92,246,0.18);
        border-radius: 14px; padding: 1.3rem 1.2rem; text-align: center;
        transition: border-color 0.2s, transform 0.2s;
    }
    .kpi-card:hover { border-color: rgba(139,92,246,0.45); transform: translateY(-2px); }
    .kpi-value {
        font-size: 2rem; font-weight: 800; line-height: 1;
        background: linear-gradient(135deg, #c4b5fd, #93c5fd);
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
</style>
""", unsafe_allow_html=True)

page_header("📊", "Analytics Dashboard", "Visual insights on student performance, attendance, and placements.", color="#34d399")

# ── Load data ─────────────────────────────────────────────────────────────────
# Always uses the local sample dataset — no DB toggle needed.
# get_sample_data() normalizes column names to lower_snake_case.
students = get_sample_data()["students"]

# ── Filters ───────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
with col1:
    branch_filter = st.multiselect("Branch", sorted(students["branch"].unique()), default=list(students["branch"].unique()))
with col2:
    sem_filter = st.multiselect("Semester", sorted(students["semester"].unique()), default=list(students["semester"].unique()))
with col3:
    cgpa_min = st.slider("Min CGPA", 0.0, 10.0, 0.0, 0.1)

filtered = students[
    (students["branch"].isin(branch_filter)) &
    (students["semester"].isin(sem_filter)) &
    (students["cgpa"] >= cgpa_min)
]

st.markdown("<br>", unsafe_allow_html=True)

# ── KPI Row ───────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-value">{len(filtered)}</div>
        <div class="kpi-label">TOTAL STUDENTS</div>
    </div>""", unsafe_allow_html=True)
with k2:
    avg_cgpa = filtered['cgpa'].mean() if len(filtered) else 0
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-value">{avg_cgpa:.2f}</div>
        <div class="kpi-label">AVG CGPA</div>
    </div>""", unsafe_allow_html=True)
with k3:
    low_att = filtered[filtered["attendance_percent"] < 75]
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-value">{len(low_att)}</div>
        <div class="kpi-label">LOW ATTENDANCE (&lt;75%)</div>
    </div>""", unsafe_allow_html=True)
with k4:
    placement_rate = filtered["placed"].mean() * 100 if len(filtered) else 0
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-value">{placement_rate:.1f}%</div>
        <div class="kpi-label">PLACEMENT RATE</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Charts Row 1 ──────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-card"><div class="chart-title">CGPA Distribution</div>', unsafe_allow_html=True)
    fig1 = px.histogram(
        filtered, x="cgpa", nbins=15, color="branch",
        color_discrete_sequence=PLOTLY_PALETTE,
        barmode="overlay", opacity=0.85,
    )
    fig1 = plotly_layout(fig1)
    fig1.update_layout(height=320, bargap=0.08)
    fig1.update_traces(marker_line_width=0)
    st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-card"><div class="chart-title">Average CGPA by Branch</div>', unsafe_allow_html=True)
    branch_cgpa = filtered.groupby("branch")["cgpa"].mean().reset_index().sort_values("cgpa", ascending=False)
    fig2 = px.bar(
        branch_cgpa, x="branch", y="cgpa",
        color="branch", color_discrete_sequence=PLOTLY_PALETTE,
        text_auto=".2f",
    )
    fig2 = plotly_layout(fig2)
    fig2.update_traces(marker_line_width=0, textposition="outside",
                        textfont=dict(color="#94a3b8", size=11))
    fig2.update_layout(height=320, showlegend=False, yaxis_range=[0, 10])
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ── Charts Row 2 ──────────────────────────────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.markdown('<div class="chart-card"><div class="chart-title">Attendance % by Branch</div>', unsafe_allow_html=True)
    att_branch = filtered.groupby("branch")["attendance_percent"].mean().reset_index().sort_values("attendance_percent")
    fig3 = px.bar(
        att_branch, x="attendance_percent", y="branch", orientation="h",
        color_discrete_sequence=["#34d399"],
        text_auto=".0f",
    )
    fig3.add_vline(x=75, line_dash="dash", line_color="#fb7185", line_width=1.5,
                    annotation_text="75% threshold", annotation_font_color="#fb7185",
                    annotation_font_size=11)
    fig3 = plotly_layout(fig3)
    fig3.update_traces(marker_line_width=0, textposition="outside",
                        textfont=dict(color="#94a3b8", size=11))
    fig3.update_layout(height=320, xaxis_title="", yaxis_title="")
    st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="chart-card"><div class="chart-title">Placement Rate by Branch</div>', unsafe_allow_html=True)
    placed_branch = (filtered.groupby("branch")["placed"].mean() * 100).reset_index().sort_values("placed", ascending=False)
    fig4 = px.bar(
        placed_branch, x="branch", y="placed",
        color_discrete_sequence=["#60a5fa"],
        text_auto=".1f",
    )
    fig4 = plotly_layout(fig4)
    fig4.update_traces(marker_line_width=0, textposition="outside",
                        textfont=dict(color="#94a3b8", size=11))
    fig4.update_layout(height=320, yaxis_title="% Placed", xaxis_title="", showlegend=False)
    st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ── Charts Row 3 — backlog & certifications ────────────────────────────────────
col5, col6 = st.columns(2)

with col5:
    st.markdown('<div class="chart-card"><div class="chart-title">Backlog Status</div>', unsafe_allow_html=True)
    backlog_counts = filtered["backlog"].value_counts().reset_index()
    backlog_counts.columns = ["backlog", "count"]
    fig5 = px.bar(
        backlog_counts.sort_values("count"), x="count", y="backlog", orientation="h",
        color="backlog", color_discrete_sequence=PLOTLY_PALETTE,
        text_auto=True,
    )
    fig5 = plotly_layout(fig5)
    fig5.update_traces(marker_line_width=0, textposition="outside",
                        textfont=dict(color="#94a3b8", size=11))
    fig5.update_layout(height=320, showlegend=False, xaxis_title="", yaxis_title="")
    st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with col6:
    st.markdown('<div class="chart-card"><div class="chart-title">Top Certifications</div>', unsafe_allow_html=True)
    cert_counts = filtered[filtered["top_certification"] != "No Certification"]["top_certification"].value_counts().head(8).reset_index()
    cert_counts.columns = ["certification", "count"]
    fig6 = px.bar(
        cert_counts.sort_values("count"), x="count", y="certification", orientation="h",
        color_discrete_sequence=["#a78bfa"], text_auto=True,
    )
    fig6 = plotly_layout(fig6)
    fig6.update_traces(marker_line_width=0, textposition="outside",
                        textfont=dict(color="#94a3b8", size=11))
    fig6.update_layout(height=320, xaxis_title="", yaxis_title="")
    st.plotly_chart(fig6, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ── Data Table ────────────────────────────────────────────────────────────────
st.divider()
st.markdown('<div class="section-label">Student Data Table</div>', unsafe_allow_html=True)
name_col = "name" if "name" in filtered.columns else "student_name"
st.dataframe(
    filtered[[name_col, "branch", "semester", "cgpa", "attendance_percent", "placement_status", "placement_company"]]
        .sort_values("cgpa", ascending=False),
    use_container_width=True, hide_index=True
)