import streamlit as st
import pandas as pd
import duckdb
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from nl2sql.engine import nl_to_sql, explain_result
from database.db import get_sample_data
from theme import apply_theme, page_header

st.set_page_config(page_title="Ask Anything | CampusIQ", page_icon="💬", layout="wide")
apply_theme()

st.markdown("""
<style>
    .sql-box {
        background: rgba(167,139,250,0.07); border: 1px solid rgba(167,139,250,0.30);
        border-radius: 12px; padding: 1rem 1.2rem;
        font-family: 'JetBrains Mono', 'Courier New', monospace; font-size: 0.88rem;
        color: #c4b5fd; white-space: pre-wrap; line-height: 1.6;
    }
    .insight-box {
        background: rgba(96,165,250,0.08); border-left: 3px solid #60a5fa;
        border-radius: 0 12px 12px 0; padding: 1rem 1.2rem; color: #cbd5e1;
        font-size: 0.92rem; line-height: 1.6;
    }
    .section-label {
        font-size: 0.78rem; font-weight: 700; letter-spacing: 0.04em;
        color: #94a3b8; text-transform: uppercase; margin: 1.2rem 0 0.5rem;
    }
    .error-box {
        background: rgba(248,113,113,0.08); border-left: 3px solid #f87171;
        border-radius: 0 12px 12px 0; padding: 1rem 1.2rem; color: #fca5a5;
        font-size: 0.9rem; line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

page_header("💬", "Ask Anything", "Ask questions about student data in plain English — no SQL needed.", color="#a78bfa")

# ── Data source: hardcoded to the real dataset CSV (no DB toggle) ─────────────
# If you later want a live-DB option back, swap get_sample_data()["students"]
# below for run_query(sql) from database.db.

# Session state: "nl_input" is the actual text_input widget key — must set it
# directly (not a separate variable) or Streamlit ignores it on rerun.
st.session_state.setdefault("nl_input", "")
st.session_state.setdefault("trigger_run", False)
st.session_state.setdefault("clear_pending", False)

# Consume a pending "Clear" request BEFORE the text_input widget below is
# created — trying to reset it after creation raises StreamlitAPIException.
# IMPORTANT: both the example buttons AND the Clear button must go through
# this flag. Setting st.session_state["nl_input"] directly anywhere *after*
# the widget below is instantiated will crash the app.
if st.session_state["clear_pending"]:
    st.session_state["nl_input"] = ""
    st.session_state["clear_pending"] = False

# Example questions
st.markdown('<div class="section-label">Try these examples</div>', unsafe_allow_html=True)
examples = [
    "Show top 5 students by CGPA in CSE",
    "Which students have attendance below 75%?",
    "Average CGPA per branch",
    "How many students are in semester 6?",
    "Students placed at TCS"
]

cols = st.columns(len(examples))
for i, ex in enumerate(examples):
    with cols[i]:
        if st.button(ex, key=f"ex_{i}", use_container_width=True):
            # Can't set nl_input directly here either — widget is created
            # further down in this same script run. Route through the
            # clear_pending-style flag pattern via a dedicated pending value.
            st.session_state["pending_value"] = ex
            st.session_state["clear_pending"] = True
            st.session_state["trigger_run"] = True
            st.rerun()

# Apply a pending example click (must also happen before widget creation)
if st.session_state.get("pending_value") is not None and st.session_state.get("trigger_run"):
    st.session_state["nl_input"] = st.session_state.pop("pending_value")

st.markdown("<br>", unsafe_allow_html=True)

# Query Input — bound to session_state via key, no separate `value=` needed
query = st.text_input(
    "Your question",
    placeholder="e.g. Show all CSE students with CGPA above 8.5",
    key="nl_input"
)

col1, col2 = st.columns([1, 4])
with col1:
    run_btn = st.button("🔍 Run Query", type="primary", use_container_width=True)
with col2:
    clear_btn = st.button("Clear", use_container_width=True)
    if clear_btn:
        # Don't touch st.session_state["nl_input"] here — the widget above
        # is already instantiated in this run. Just set the flag and rerun;
        # the clear_pending block at the top will reset it on the next run.
        st.session_state["clear_pending"] = True
        st.session_state["trigger_run"] = False
        st.rerun()

should_run = (run_btn or st.session_state.get("trigger_run", False)) and query
if should_run:
    st.session_state["trigger_run"] = False  # consume the auto-run flag

    with st.spinner("Generating SQL..."):
        sql = nl_to_sql(query)

    st.markdown('<div class="section-label">Generated SQL</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sql-box">{sql}</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    students_df = get_sample_data()["students"]

    # ── Actually execute the generated SQL against the DataFrame ────────────
    # Previously this just dumped the raw students_df regardless of the SQL,
    # so "top 5" queries showed all 600 rows. duckdb lets us run real SQL
    # (WHERE / ORDER BY / LIMIT / GROUP BY etc.) directly against a DataFrame.
    df = pd.DataFrame()
    query_error = None
    try:
        con = duckdb.connect()
        con.register("students", students_df)
        df = con.execute(sql).df()
        con.close()
    except Exception as e:
        query_error = str(e)

    st.markdown('<div class="section-label">Results</div>', unsafe_allow_html=True)

    if query_error:
        st.markdown(
            f'<div class="error-box">⚠️ The generated SQL could not be run against the data: {query_error}</div>',
            unsafe_allow_html=True
        )
        result_summary = f"Query failed: {query_error}"
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)
        result_summary = f"{len(df)} rows returned. Columns: {list(df.columns)}"

    # AI Explanation
    if not query_error and not df.empty:
        with st.spinner("Generating insight..."):
            insight = explain_result(query, sql, result_summary)
        st.markdown('<div class="section-label">AI Insight</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="insight-box">💡 {insight}</div>', unsafe_allow_html=True)

    # Query history
    if "history" not in st.session_state:
        st.session_state["history"] = []
    st.session_state["history"].append({"question": query, "sql": sql})

# Query History
if st.session_state.get("history"):
    st.divider()
    st.markdown('<div class="section-label">Query History (this session)</div>', unsafe_allow_html=True)
    for i, h in enumerate(reversed(st.session_state["history"][-5:])):
        with st.expander(f"Q: {h['question']}"):
            st.code(h["sql"], language="sql")