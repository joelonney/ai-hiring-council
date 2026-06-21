import streamlit as st
from pypdf import PdfReader
import re

from agents import (
    recruiter_agent,
    technical_agent,
    culture_agent,
    council_agent
)

st.set_page_config(
    page_title="AI Hiring Council",
    page_icon="💻",
    layout="wide"
)

# =========================
# STYLING
# =========================

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.stApp {
    background:
        radial-gradient(
            circle at top right,
            rgba(99,102,241,0.08),
            transparent 40%
        ),
        radial-gradient(
            circle at bottom left,
            rgba(34,197,94,0.08),
            transparent 40%
        );
}

.agent-card {

    background: rgba(255,255,255,0.75);

    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);

    border: 1px solid rgba(255,255,255,0.3);

    border-radius: 22px;

    padding: 24px;

    box-shadow:
        0 8px 32px rgba(99,102,241,0.08);

    text-align:center;

    margin-bottom:1rem;
}

.metric {
    font-size: 1.6rem;
    font-weight: bold;
}

.step-bar {

    background: rgba(255,255,255,0.65);

    backdrop-filter: blur(12px);

    border: 1px solid rgba(255,255,255,0.3);

    color:#4F46E5;

    padding:16px;

    border-radius:18px;

    text-align:center;

    margin-bottom:24px;

    font-weight:700;

    box-shadow:
        0 4px 20px rgba(99,102,241,0.08);
}

</style>
""", unsafe_allow_html=True)

# =========================
# HELPERS
# =========================

def extract_pdf_text(uploaded_file):

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def get_verdict(agent_output):

    output = agent_output.lower()

    if "reject" in output:
        return "Reject"

    if "hold" in output:
        return "Hold"

    if "proceed" in output:
        return "Proceed"

    return "Unknown"


def extract_confidence(text):

    match = re.search(r'(\d+)%', text)

    if match:
        return match.group(1)

    return "80"


# =========================
# HEADER
# =========================

st.markdown("""
<h1 style="
margin-bottom:0;
font-size:3rem;
font-weight:800;
color:#111827;
">
AI Hiring Council
</h1>

<p style="
font-size:1.1rem;
color:#64748B;
margin-top:0;
">
AI-Powered Candidate Review & Decision Support
</p>
""", unsafe_allow_html=True)

st.caption(
    "Multi-Agent Hiring Intelligence • Recruiter • Technical • Behavioral"
)

st.markdown("""
<div class="step-bar">
① Candidate Inputs &nbsp; → &nbsp;
② AI Evaluation &nbsp; → &nbsp;
③ Council Decision
</div>
""", unsafe_allow_html=True)

# =========================
# INPUTS
# =========================

col1, col2 = st.columns(2)

with col1:

    resume = st.file_uploader(
        "📄 Upload Resume",
        type=["pdf"]
    )

with col2:

    jd = st.text_area(
        "🎯 Job Description",
        height=220
    )

notes = st.text_area(
    "📝 Interview Notes",
    height=150
)

# =========================
# RUN
# =========================

if st.button("🤖 Generate Hiring Recommendation", use_container_width=True):

    if not resume:
        st.error("Please upload a resume.")
        st.stop()

    if not jd:
        st.error("Please provide a Job Description.")
        st.stop()

    resume_text = extract_pdf_text(resume)

    with st.spinner("👩‍💼 Recruiter Agent evaluating..."):
        recruiter_result = recruiter_agent(
            jd,
            resume_text,
            notes
        )

    with st.spinner("💻 Technical Agent evaluating..."):
        technical_result = technical_agent(
            jd,
            resume_text,
            notes
        )

    with st.spinner("🤝 Behavioral Agent evaluating..."):
        culture_result = culture_agent(
            jd,
            resume_text,
            notes
        )

    with st.spinner("🏛️ Hiring Council deliberating..."):
        council_result = council_agent(
            recruiter_result,
            technical_result,
            culture_result
        )

    confidence = extract_confidence(council_result)

    recruiter_vote = get_verdict(recruiter_result)
    technical_vote = get_verdict(technical_result)
    culture_vote = get_verdict(culture_result)

    votes = [
        recruiter_vote,
        technical_vote,
        culture_vote
    ]

    proceed_count = votes.count("Proceed")
    reject_count = votes.count("Reject")

    if proceed_count >= 2:
        final_decision = "ADVANCE"

    elif reject_count >= 2:
        final_decision = "REJECT"

    else:
        final_decision = "HOLD"

    hero_class = "hero-green"

    if final_decision == "HOLD":
        hero_class = "hero-orange"

    if final_decision == "REJECT":
        hero_class = "hero-red"

    # =========================
    # HERO CARD
    # =========================

    hero_color = "#22c55e"

    if final_decision == "HOLD":
        hero_color = "#f59e0b"

    if final_decision == "REJECT":
        hero_color = "#ef4444"

    st.markdown(
        f"""
    <div style="
    padding:40px;
    border-radius:24px;
    text-align:center;
    color:white;
    background:linear-gradient(
    135deg,
    {hero_color},
    #60A5FA
    );
    box-shadow:0 10px 30px rgba(0,0,0,0.15);
    margin-bottom:25px;
    ">

    <div style="
    font-size:18px;
    font-weight:600;
    margin-bottom:10px;
    ">
    🏛️ FINAL COUNCIL DECISION
    </div>

    <div style="
    font-size:64px;
    font-weight:800;
    margin-bottom:15px;
    ">
    {final_decision}
    </div>

    <div style="
    font-size:24px;
    font-weight:600;
    margin-bottom:10px;
    ">
    Confidence: {confidence}%
    </div>

    <div style="
    font-size:18px;
    opacity:0.95;
    ">
    Consensus: {proceed_count}/3 Agents Recommend Proceed
    </div>

    </div>
    """,
        unsafe_allow_html=True
    )

    # =========================
    # VOTE SUMMARY
    # =========================

    st.subheader("📊 AI Evaluation Panel")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="agent-card">
        <h4>👩‍💼 Recruiter</h4>
        <div class="metric">{recruiter_vote}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="agent-card">
        <h4>💻 Technical</h4>
        <div class="metric">{technical_vote}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="agent-card">
        <h4>🤝 Behavioral</h4>
        <div class="metric">{culture_vote}</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    if final_decision == "ADVANCE":
        st.success("✅ Candidate Recommended for Advancement")

    elif final_decision == "HOLD":
        st.warning("⚠️ Additional Evaluation Recommended")

    else:
        st.error("❌ Candidate Not Recommended")

    # =========================
    # COUNCIL SUMMARY
    # =========================

    st.subheader("🏛️ AI Hiring Council Recommendation")

    st.markdown(council_result)

    # =========================
    # EXPANDERS
    # =========================

    with st.expander("👩‍💼 Recruiter Analysis"):
        st.markdown(recruiter_result)

    with st.expander("💻 Technical Analysis"):
        st.markdown(technical_result)

    with st.expander("🤝 Behavioral Analysis"):
        st.markdown(culture_result)