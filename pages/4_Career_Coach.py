import streamlit as st
import chromadb
from groq import Groq
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from theme import apply_theme, page_header

st.set_page_config(page_title="Career Coach | CampusIQ", page_icon="🤖", layout="wide")
apply_theme()

st.markdown("""
<style>
    .chat-user {
        background: rgba(167,139,250,0.14); border-radius: 14px 14px 4px 14px;
        padding: 0.8rem 1.1rem; margin: 0.5rem 0 0.5rem auto; max-width: 80%;
        text-align: right; color: #e2e8f0; border: 1px solid rgba(167,139,250,0.28);
    }
    .chat-bot {
        background: rgba(96,165,250,0.09); border-radius: 14px 14px 14px 4px;
        padding: 0.8rem 1.1rem; margin: 0.5rem auto 0.5rem 0; max-width: 80%;
        color: #e2e8f0; border: 1px solid rgba(96,165,250,0.26);
    }
    .source-tag {
        display: inline-block; background: rgba(52,211,153,0.10);
        border: 1px solid rgba(52,211,153,0.30); border-radius: 999px;
        padding: 0.15rem 0.6rem; font-size: 0.72rem; color: #34d399;
        margin-top: 0.4rem; font-weight: 600;
    }
    .section-label {
        font-size: 0.78rem; font-weight: 700; letter-spacing: 0.04em;
        color: #94a3b8; text-transform: uppercase; margin: 1.2rem 0 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

page_header("🤖", "Career Coach", "Ask anything about placements, career paths, resume tips, and more.", color="#fbbf24")

# Initialize clients
@st.cache_resource
def init_chromadb():
    client = chromadb.Client()
    collection = client.get_or_create_collection("career_kb")

    if collection.count() == 0:
        documents = [
            "KIIT University placement season typically starts in August-September for final year students. Top recruiters include TCS, Infosys, Wipro, Capgemini, and Accenture.",
            "For data analyst roles, students should know SQL, Python (pandas, numpy), and at least one BI tool like Power BI or Tableau. Kaggle projects strengthen your profile.",
            "For AI/ML engineering roles, focus on scikit-learn, PyTorch or TensorFlow, NLP basics, and deploy at least one end-to-end ML project. HuggingFace models are highly valued.",
            "A strong resume for CSE freshers should have: 2-3 projects with GitHub links, relevant certifications, technical skills listed clearly, and CGPA above 7.0 for most companies.",
            "For SAP-related roles, having SAP Business Data Cloud or SAP Data Analytics certification significantly improves shortlisting chances at companies like Deloitte and Accenture.",
            "Common interview rounds at top product companies: Online Assessment (DSA) → Technical Interview (CS fundamentals + projects) → HR round.",
            "For off-campus placements, LinkedIn optimization, GitHub activity, and applying through company career portals directly are the best strategies.",
            "CGPA cutoffs: TCS = 6.0, Infosys = 6.5, Wipro = 6.0, Capgemini = 6.0, Amazon = 7.5, Microsoft = 8.0 (approx, may change).",
            "Core Java is essential for full stack roles. Focus on OOP, Collections, Streams, JDBC, and Spring Boot basics.",
            "For data engineering roles, learn Apache Spark, Kafka basics, PostgreSQL, and cloud platforms like AWS or GCP. Pipeline projects on GitHub are very impressive.",
        ]
        ids = [f"doc_{i}" for i in range(len(documents))]
        collection.add(documents=documents, ids=ids)

    return collection

@st.cache_resource
def init_groq():
    return Groq(api_key=os.environ.get("GROQ_API_KEY"))

collection = init_chromadb()
groq_client = init_groq()

# Chat history
if "career_messages" not in st.session_state:
    st.session_state["career_messages"] = []


def generate_response(user_input: str):
    """Runs the RAG lookup + Groq call and appends the assistant reply to history."""
    with st.spinner("Thinking..."):
        results = collection.query(query_texts=[user_input], n_results=3)
        context_docs = results["documents"][0] if results["documents"] else []
        context = "\n".join(context_docs)

        system_prompt = f"""You are CampusIQ Career Coach, an AI counselor for students.
You help students with placement preparation, career advice, resume tips, and job market insights.

Use the following knowledge base context to answer:
{context}

Be specific, practical, and encouraging. Keep answers concise (3-5 sentences max).
If the question is outside your knowledge base, give general advice and recommend consulting the placement cell."""

        messages = [{"role": "system", "content": system_prompt}]
        for msg in st.session_state["career_messages"][-6:]:
            messages.append({"role": msg["role"], "content": msg["content"]})

        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=400
        )
        answer = response.choices[0].message.content.strip()

    st.session_state["career_messages"].append({
        "role": "assistant",
        "content": answer,
        "sources": context_docs
    })

# Domain filter
domain = st.selectbox(
    "Filter by domain",
    ["All", "Placements", "Data Analytics", "AI/ML", "Full Stack", "SAP", "Resume Tips"]
)

st.markdown("<br>", unsafe_allow_html=True)

# Display chat history
chat_container = st.container()
with chat_container:
    for msg in st.session_state["career_messages"]:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-user">👤 {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bot">🤖 {msg["content"]}</div>', unsafe_allow_html=True)
            if msg.get("sources"):
                st.markdown(f'<span class="source-tag">📚 Based on Campus Insights </span>', unsafe_allow_html=True)

# Quick questions
if not st.session_state["career_messages"]:
    st.markdown('<div class="section-label">Quick Questions</div>', unsafe_allow_html=True)
    quick = [
        "What is the CGPA cutoff for TCS?",
        "How to prepare for data analyst interviews?",
        "Best certifications for AI/ML roles?",
        "How to improve my resume?"
    ]
    cols = st.columns(2)
    for i, q in enumerate(quick):
        with cols[i % 2]:
            if st.button(q, key=f"quick_{i}", use_container_width=True):
                st.session_state["career_messages"].append({"role": "user", "content": q})
                generate_response(q)
                st.rerun()

# Input
user_input = st.chat_input("Ask about placements, resume, career paths...")

if user_input:
    st.session_state["career_messages"].append({"role": "user", "content": user_input})
    generate_response(user_input)
    st.rerun()