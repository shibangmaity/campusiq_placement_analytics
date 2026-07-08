"""
theme.py — paste `apply_theme()` at the top of every page file.
Just call:  from theme import apply_theme; apply_theme()
"""

import streamlit as st

def apply_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ── Global reset ── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    /* ── Main background: deep cosmic purple → midnight blue ── */
    .stApp {
        background: linear-gradient(135deg, #0d0221 0%, #0a0a1a 35%, #060d1f 65%, #0a0a12 100%) !important;
        color: #e2e8f0 !important;
    }

    /* ── Sidebar: dark purple, always ── */
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(180deg, #0f0728 0%, #0a0a1c 100%) !important;
        border-right: 1px solid rgba(139,92,246,0.25) !important;
    }
    /* Sidebar text */
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] a,
    [data-testid="stSidebar"] li,
    [data-testid="stSidebar"] div {
        color: #94a3b8 !important;
    }
    /* Active sidebar item */
    [data-testid="stSidebar"] [aria-selected="true"],
    [data-testid="stSidebar"] .st-emotion-cache-1rtdyuf {
        color: #c4b5fd !important;
        background: rgba(139,92,246,0.12) !important;
        border-radius: 8px;
    }
    /* Nav link hover */
    [data-testid="stSidebarNavLink"]:hover {
        background: rgba(139,92,246,0.10) !important;
        color: #c4b5fd !important;
    }
    [data-testid="stSidebarNavLink"][aria-current="page"] {
        background: rgba(139,92,246,0.18) !important;
        border-left: 3px solid #a78bfa !important;
        color: #c4b5fd !important;
    }

    /* ── Header ── */
    header[data-testid="stHeader"] {
        background: rgba(13,2,33,0.85) !important;
        border-bottom: 1px solid rgba(139,92,246,0.12);
        backdrop-filter: blur(12px);
    }

    /* ── Block container ── */
    .block-container {
        padding: 2rem 2.5rem 3rem !important;
        max-width: 1100px;
    }

    /* ── Global fallback for ALL text inputs — bypasses any dependency on
       Streamlit's wrapper div structure (.stTextInput > div > div), which
       can silently stop matching between Streamlit versions.
       Background stayed white no matter what, so text is forced BLACK
       instead — readable is more important than matching the dark theme. ── */
    input[type="text"],
    input[type="search"],
    input[type="number"],
    input[type="password"],
    input[type="email"],
    textarea {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        caret-color: #000000 !important;
    }
    input[type="text"]::placeholder,
    input[type="search"]::placeholder,
    input[type="number"]::placeholder,
    textarea::placeholder {
        color: #4b5563 !important;
        -webkit-text-fill-color: #4b5563 !important;
        opacity: 1 !important;
    }

    /* ── Inputs & text areas ── */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(139,92,246,0.25) !important;
        color: #e2e8f0 !important;
        border-radius: 10px !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: rgba(139,92,246,0.65) !important;
        box-shadow: 0 0 0 3px rgba(139,92,246,0.12) !important;
    }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 0.55rem 1.4rem !important;
        transition: opacity 0.2s, transform 0.15s !important;
    }
    .stButton > button:hover {
        opacity: 0.88 !important;
        transform: translateY(-1px) !important;
    }

    /* ── Metric cards ── */
    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(139,92,246,0.18) !important;
        border-radius: 14px !important;
        padding: 1.1rem 1.3rem !important;
    }
    [data-testid="stMetricLabel"] { color: #64748b !important; }
    [data-testid="stMetricValue"] { color: #c4b5fd !important; }

    /* ── Dataframe / table ── */
    .stDataFrame, iframe[title="streamlit_aggrid.agGrid"] {
        border-radius: 12px !important;
        overflow: hidden;
        border: 1px solid rgba(139,92,246,0.18) !important;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255,255,255,0.03) !important;
        border-radius: 10px;
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #64748b !important;
        border-radius: 8px !important;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(139,92,246,0.18) !important;
        color: #c4b5fd !important;
    }

    /* ── Selectbox / multiselect — the control box itself ──
       (previously only the little pill tags were styled, so the
       outer control and dropdown menu fell back to browser-default
       white — this is the "big white box" bug) */
    div[data-baseweb="select"] > div,
    div[data-baseweb="select"] [class*="control"] {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(139,92,246,0.25) !important;
        border-radius: 10px !important;
    }
    div[data-baseweb="select"] input {
        color: #e2e8f0 !important;
    }
    div[data-baseweb="select"] svg {
        fill: #94a3b8 !important;
    }

    /* ── Dropdown popover menu — BaseWeb renders this in a portal
       outside .stApp, so it needs its own explicit dark styling ── */
    div[data-baseweb="popover"] {
        background: transparent !important;
    }
    div[data-baseweb="popover"] ul,
    div[data-baseweb="menu"],
    div[data-baseweb="popover"] [role="listbox"] {
        background: #12121f !important;
        border: 1px solid rgba(139,92,246,0.25) !important;
        border-radius: 10px !important;
    }
    div[data-baseweb="popover"] li,
    div[data-baseweb="menu"] li,
    div[data-baseweb="popover"] [role="option"] {
        background: #12121f !important;
        color: #e2e8f0 !important;
    }
    div[data-baseweb="popover"] li:hover,
    div[data-baseweb="menu"] li:hover,
    div[data-baseweb="popover"] [role="option"]:hover {
        background: rgba(139,92,246,0.20) !important;
    }

    /* ── Selectbox / multiselect tags ── */
    [data-baseweb="tag"] {
        background: rgba(139,92,246,0.22) !important;
        color: #c4b5fd !important;
        border-radius: 999px !important;
    }

    /* ── Slider ── */
    [data-testid="stSlider"] [data-baseweb="slider"] > div {
        background: rgba(255,255,255,0.08) !important;
    }
    [data-testid="stSlider"] [role="slider"] {
        background: #a78bfa !important;
        border-color: #a78bfa !important;
    }
    [data-testid="stTickBar"] {
        background: transparent !important;
    }

    /* ── Checkbox ── */
    .stCheckbox label { color: #94a3b8 !important; }

    /* ── Autofill fix — background stays white regardless (Chrome override
       we couldn't beat), so force black text here too instead of the light
       text color that would be invisible against it ── */
    input:-webkit-autofill,
    input:-webkit-autofill:hover,
    input:-webkit-autofill:focus,
    input:-webkit-autofill:active {
        -webkit-text-fill-color: #000000 !important;
        box-shadow: 0 0 0px 1000px #ffffff inset !important;
        transition: background-color 5000s ease-in-out 0s;
    }

    /* ── Chat input (bottom bar) — st.chat_input renders in its own fixed
       footer container, outside the normal page flow, so it needs its own
       explicit dark styling or it falls back to Streamlit's default white ── */
    [data-testid="stChatInput"],
    [data-testid="stBottomBlockContainer"],
    [data-testid="stBottom"] > div,
    .stChatFloatingInputContainer {
        background: #0a0a12 !important;
        border-top: 1px solid rgba(139,92,246,0.20) !important;
    }
    /* Global fallback — catches the chat input textarea regardless of
       whatever internal wrapper name this Streamlit version uses */
    textarea {
        background: rgba(20,20,35,0.9) !important;
        color: #e2e8f0 !important;
        -webkit-text-fill-color: #e2e8f0 !important;
        caret-color: #e2e8f0 !important;
    }
    textarea::placeholder {
        color: #64748b !important;
        -webkit-text-fill-color: #64748b !important;
        opacity: 1 !important;
    }

    [data-testid="stChatInput"] textarea,
    [data-testid="stChatInputTextArea"],
    [data-testid="stBottom"] textarea,
    [data-testid="stBottomBlockContainer"] textarea,
    .stChatFloatingInputContainer textarea {
        background: rgba(255,255,255,0.05) !important;
        color: #000000 !important;
        border-radius: 10px !important;
        -webkit-text-fill-color: #000000 !important;
        opacity: 1 !important;
        font-weight: 500 !important;
    }
    [data-testid="stChatInput"] textarea::placeholder,
    [data-testid="stChatInputTextArea"]::placeholder {
        color: #4b5563 !important;
        -webkit-text-fill-color: #4b5563 !important;
    }
    [data-testid="stChatInput"] button {
        background: rgba(139,92,246,0.25) !important;
    }
    [data-testid="stChatInput"] button svg {
        fill: #c4b5fd !important;
    }

    /* ── Inline code — Streamlit's default is a near-white box;
       this is what made things like `Placement_Status` badges
       barely visible on the dark theme ── */
    code {
        background: rgba(167,139,250,0.15) !important;
        color: #c4b5fd !important;
        padding: 2px 7px !important;
        border-radius: 5px !important;
        font-size: 0.85em !important;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb {
        background: rgba(139,92,246,0.30);
        border-radius: 999px;
    }
    ::-webkit-scrollbar-thumb:hover { background: rgba(139,92,246,0.55); }

    /* ── Plotly chart background ── */
    .js-plotly-plot .plotly,
    .js-plotly-plot .plotly .svg-container {
        background: transparent !important;
    }
    /* ── FINAL FORM-ELEMENT THEME — white background + black text, always ──
       We tried forcing these dark to match the page theme, but native
       widgets (select, number input, chat input) fought back inconsistently
       — sometimes background stayed white with light text (invisible),
       sometimes .streamlit/config.toml made it dark with black text from
       our earlier fix (also invisible). Instead of continuing to chase
       that, this locks in ONE consistent, always-readable combination for
       every interactive form element: white background, black text. The
       rest of the page (cards, sidebar, backgrounds) stays dark as before —
       only the actual input/dropdown surfaces are light. */

    div[data-baseweb="select"] > div,
    div[data-baseweb="select"] [class*="control"] {
        background: #ffffff !important;
        border: 1px solid rgba(139,92,246,0.35) !important;
        border-radius: 10px !important;
    }
    div[data-baseweb="select"] input,
    div[data-baseweb="select"] [class*="ValueContainer"] div {
        color: #000000 !important;
    }
    div[data-baseweb="select"] svg {
        fill: #374151 !important;
    }

    div[data-baseweb="popover"] ul,
    div[data-baseweb="menu"],
    div[data-baseweb="popover"] [role="listbox"] {
        background: #ffffff !important;
        border: 1px solid rgba(139,92,246,0.35) !important;
        border-radius: 10px !important;
    }
    div[data-baseweb="popover"] li,
    div[data-baseweb="menu"] li,
    div[data-baseweb="popover"] [role="option"] {
        background: #ffffff !important;
        color: #000000 !important;
    }
    div[data-baseweb="popover"] li:hover,
    div[data-baseweb="menu"] li:hover,
    div[data-baseweb="popover"] [role="option"]:hover {
        background: rgba(139,92,246,0.12) !important;
    }

    input[type="text"],
    input[type="search"],
    input[type="number"],
    input[type="password"],
    input[type="email"],
    textarea,
    [data-testid="stChatInput"] textarea,
    [data-testid="stChatInputTextArea"] {
        background: #ffffff !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        caret-color: #000000 !important;
        border-radius: 10px !important;
    }
    input[type="text"]::placeholder,
    input[type="search"]::placeholder,
    input[type="number"]::placeholder,
    textarea::placeholder,
    [data-testid="stChatInput"] textarea::placeholder {
        color: #6b7280 !important;
        -webkit-text-fill-color: #6b7280 !important;
        opacity: 1 !important;
    }

    input:-webkit-autofill,
    input:-webkit-autofill:hover,
    input:-webkit-autofill:focus,
    input:-webkit-autofill:active {
        -webkit-text-fill-color: #000000 !important;
        box-shadow: 0 0 0px 1000px #ffffff inset !important;
        transition: background-color 5000s ease-in-out 0s;
    }
    </style>
    """, unsafe_allow_html=True)


# ── Page header helper ────────────────────────────────────────────────────────
def page_header(icon: str, title: str, subtitle: str, color: str = "#a78bfa"):
    st.markdown(f"""
    <div style="margin-bottom:2rem;">
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:0.4rem;">
            <span style="font-size:1.6rem;">{icon}</span>
            <h1 style="font-size:1.9rem; font-weight:800; margin:0;
                background: linear-gradient(135deg, #f8fafc, {color});
                -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                background-clip:text; letter-spacing:-0.02em;">
                {title}
            </h1>
        </div>
        <p style="color:#475569; font-size:0.92rem; margin:0 0 0 56px;">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


# ── Plotly theme config ───────────────────────────────────────────────────────
PLOTLY_PALETTE = ["#a78bfa", "#60a5fa", "#34d399", "#fb7185", "#fbbf24", "#38bdf8"]

def plotly_layout(fig, title: str = ""):
    """Apply consistent dark theme to any plotly figure."""
    fig.update_layout(
        title=dict(text=title, font=dict(color="#e2e8f0", size=14, family="Inter")),
        paper_bgcolor="rgba(255,255,255,0.02)",
        plot_bgcolor="rgba(255,255,255,0.02)",
        font=dict(color="#94a3b8", family="Inter", size=12),
        margin=dict(l=16, r=16, t=40 if title else 16, b=16),
        legend=dict(
            bgcolor="rgba(255,255,255,0.04)",
            bordercolor="rgba(255,255,255,0.08)",
            borderwidth=1,
            font=dict(color="#94a3b8"),
        ),
        xaxis=dict(
            gridcolor="rgba(255,255,255,0.05)",
            zerolinecolor="rgba(255,255,255,0.08)",
            tickfont=dict(color="#64748b"),
        ),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.05)",
            zerolinecolor="rgba(255,255,255,0.08)",
            tickfont=dict(color="#64748b"),
        ),
    )
    # Apply palette to all traces that support marker.color
    # (pie traces have marker.colors, not marker.color — hasattr guards against that)
    for i, trace in enumerate(fig.data):
        if hasattr(trace, "marker") and hasattr(trace.marker, "color") and trace.marker.color is None:
            trace.marker.color = PLOTLY_PALETTE[i % len(PLOTLY_PALETTE)]
    return fig
