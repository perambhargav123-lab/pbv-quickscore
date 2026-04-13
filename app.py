"""
PBV Finance | AI Governance Quick Score
Standalone single-page Streamlit lead-gen tool.

Run locally:  streamlit run quick_score.py
Deploy:       Streamlit Cloud → https://pbv-quickscore.streamlit.app

No API key required. Pure-Python scoring. Self-contained — does NOT import
from the full governance suite, so it can be deployed on its own.
"""

import streamlit as st
import plotly.graph_objects as go


# ============================================================
# BRAND
# ============================================================
COLORS = {
    "primary": "#1E3A5F",
    "secondary": "#2E75B6",
    "accent": "#E8941A",
    "success": "#28A745",
    "warning": "#FFC107",
    "danger": "#DC3545",
}

CONTACT_EMAIL = "bhargavperam98@gmail.com"
CALENDLY_URL = "https://calendly.com/bhargavperam98/15min"  # update if your Calendly slug differs

GCC_BENCHMARK = 2.3

MATURITY_LEVELS = {
    1: {"name": "Ad Hoc", "color": "#FF4444", "desc": "No formal governance; reactive only"},
    2: {"name": "Developing", "color": "#FF8C00", "desc": "Basic awareness; inconsistent practices"},
    3: {"name": "Defined", "color": "#FFD700", "desc": "Formal processes documented; partial adoption"},
    4: {"name": "Managed", "color": "#90EE90", "desc": "Embedded in operations; measured and monitored"},
    5: {"name": "Optimized", "color": "#00AA00", "desc": "Continuous improvement; competitive differentiator"},
}


# ============================================================
# QUESTIONS — one per dimension
# ============================================================
QUESTIONS = [
    {
        "key": "strategy",
        "label": "Strategy",
        "text": "Does your finance function have a formal AI strategy with executive sponsorship?",
        "weak_warning": "Without a formal AI strategy, adoption is ad hoc — random ChatGPT prompts, zero coordination, zero ROI.",
    },
    {
        "key": "risk_controls",
        "label": "Risk & Controls",
        "text": "Do you validate AI outputs before they affect financial reporting?",
        "weak_warning": "Unvalidated AI outputs flowing into financial statements is a material misstatement waiting to happen.",
    },
    {
        "key": "data_technology",
        "label": "Data & Technology",
        "text": "Do you know where ALL your financial data is processed — including by AI tools like Copilot and ChatGPT?",
        "weak_warning": "Shadow AI is the #1 governance risk in 2026. UAE PDPL fines reach AED 5,000,000 for unmapped cross-border data.",
    },
    {
        "key": "governance_process",
        "label": "Governance & Process",
        "text": "Is there an audit trail capturing every AI input, output, and human review decision?",
        "weak_warning": "No audit trail = no defense when auditors ask why AI made a posting decision 3 years ago.",
    },
    {
        "key": "people_culture",
        "label": "People & Culture",
        "text": "Can your finance team identify and escalate AI errors?",
        "weak_warning": "Untrained staff either blindly trust AI (dangerous) or refuse to use it (wasted investment). Both fail.",
    },
]


# ============================================================
# 3 GOVERNANCE GATES
# Gate 1 → Data Sovereignty (Q3 = data_technology)
# Gate 2 → Human Approval Protocol (Q2 = risk_controls)
# Gate 3 → Output Labelling Standard (Q4 = governance_process)
# ============================================================
GATES = [
    {
        "key": "data_technology",
        "icon": "🔒",
        "name": "Data Sovereignty",
        "criteria": "Data stays in confirmed jurisdiction. AI does not train on your data. Encryption + audit log.",
        "fail": "Financial data may be processed in unknown jurisdictions, potentially training third-party models. UAE PDPL: up to AED 5,000,000.",
    },
    {
        "key": "risk_controls",
        "icon": "👤",
        "name": "Human Approval Protocol",
        "criteria": "Every AI output has a defined approval level. No AI output acts above materiality without human sign-off.",
        "fail": "AI could post journal entries or approve payments without human review. SOX / audit finding guaranteed.",
    },
    {
        "key": "governance_process",
        "icon": "🏷️",
        "name": "Output Labelling Standard",
        "criteria": "Every AI output labelled CALCULATED FACT / AI-ASSISTED / AI HYPOTHESIS, with source citation.",
        "fail": "Auditors cannot distinguish verified data from AI-generated analysis. Internal control deficiency.",
    },
]


def gate_status(score: int) -> tuple[str, str]:
    """Return (badge, color) for a 1-5 score."""
    if score >= 4:
        return "✅ PASS", COLORS["success"]
    if score >= 3:
        return "⚠️ PARTIAL", COLORS["warning"]
    return "❌ FAIL", COLORS["danger"]


def maturity_for(avg: float) -> dict:
    level = max(1, min(5, round(avg)))
    return {"level": level, **MATURITY_LEVELS[level]}


# ============================================================
# PAGE
# ============================================================
st.set_page_config(
    page_title="PBV Finance | AI Governance Quick Score",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    f"""
<style>
    .stApp {{ background-color: #FAFBFC; }}
    h1, h2, h3 {{ color: {COLORS['primary']}; }}
    .stButton>button, .stLinkButton>a {{
        background-color: {COLORS['secondary']};
        color: white;
        border: none;
        font-weight: 600;
    }}
    .stButton>button:hover {{ background-color: {COLORS['primary']}; }}
    .hero {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        color: white;
        padding: 24px;
        border-radius: 12px;
        text-align: center;
    }}
    .hero h1 {{ color: white; margin: 0; }}
    .hero p {{ color: white; margin: 6px 0 0; opacity: 0.95; }}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class='hero'>
  <h1>PBV Finance | AI Governance Quick Score</h1>
  <p>5 questions. 2 minutes. See where you stand.</p>
</div>
""",
    unsafe_allow_html=True,
)
st.markdown("")

st.error(
    "**86% of finance teams have encountered hallucinated AI data.** "
    "One unvalidated output in a board report doesn't just create a restatement — "
    "it destroys years of trust."
)

st.markdown("---")

# ============================================================
# QUESTIONS
# ============================================================
st.subheader("📋 Five Questions")
st.caption("Score each from 1 (Not at all) to 5 (Fully embedded).")

scores: dict[str, int] = {}
for i, q in enumerate(QUESTIONS, 1):
    scores[q["key"]] = st.slider(
        f"**Q{i}.** {q['text']}",
        min_value=1,
        max_value=5,
        value=3,
        key=f"q_{q['key']}",
        help="1 = Not at all · 2 = Ad hoc · 3 = Partially defined · 4 = Mostly implemented · 5 = Fully embedded",
    )

st.markdown("---")

# ============================================================
# RESULTS
# ============================================================
st.subheader("📊 Your Results")

avg_score = round(sum(scores.values()) / len(scores), 2)
level = maturity_for(avg_score)

# Hero metric
st.markdown(
    f"""
<div style='text-align:center; padding:20px; border-radius:12px;
            background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
            color:white; margin-bottom:16px;'>
  <p style='margin:0; opacity:0.85;'>OVERALL MATURITY</p>
  <h1 style='color:white; font-size:56px; margin:6px 0;'>{avg_score}/5</h1>
  <p style='color:white; font-size:18px; margin:0;'>Level {level['level']} — {level['name']}</p>
  <p style='color:white; opacity:0.85; font-size:13px; margin-top:4px;'>{level['desc']}</p>
</div>
""",
    unsafe_allow_html=True,
)

# Benchmark line
delta_vs_avg = round(avg_score - GCC_BENCHMARK, 2)
delta_color = COLORS["success"] if delta_vs_avg >= 0 else COLORS["danger"]
delta_sign = "+" if delta_vs_avg >= 0 else ""
st.markdown(
    f"**Your score:** {avg_score}/5 · "
    f"**GCC mid-market average:** {GCC_BENCHMARK}/5 · "
    f"<span style='color:{delta_color}; font-weight:600;'>{delta_sign}{delta_vs_avg} vs average</span>",
    unsafe_allow_html=True,
)
st.markdown("")

# Radar chart
labels = [q["label"] for q in QUESTIONS]
values = [scores[q["key"]] for q in QUESTIONS]
fig = go.Figure()
fig.add_trace(
    go.Scatterpolar(
        r=values + [values[0]],
        theta=labels + [labels[0]],
        fill="toself",
        line=dict(color=COLORS["secondary"], width=3),
        fillcolor="rgba(46,117,182,0.3)",
        name="You",
    )
)
fig.add_trace(
    go.Scatterpolar(
        r=[GCC_BENCHMARK] * (len(labels) + 1),
        theta=labels + [labels[0]],
        line=dict(color="#999999", width=2, dash="dash"),
        name="GCC Average",
    )
)
fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
    showlegend=True,
    height=400,
    margin=dict(t=20, b=20, l=20, r=20),
)
st.plotly_chart(fig, use_container_width=True)

# Per-dimension warnings (anything ≤ 2)
weak = [q for q in QUESTIONS if scores[q["key"]] <= 2]
if weak:
    st.markdown("### ⚠️ Risk Warnings")
    for q in weak:
        st.warning(f"**{q['label']} ({scores[q['key']]}/5):** {q['weak_warning']}")

st.markdown("---")

# ============================================================
# 3 GOVERNANCE GATES
# ============================================================
st.subheader("🔐 3 Governance Gates")
st.caption("Every AI output must pass all 3 gates before going live. (Based on PBV's CFO×AI Framework.)")

for gate in GATES:
    score = scores[gate["key"]]
    badge, badge_color = gate_status(score)
    with st.container(border=True):
        st.markdown(
            f"<div style='display:flex; justify-content:space-between; align-items:center;'>"
            f"<div><span style='font-size:20px;'>{gate['icon']}</span> "
            f"<b>Gate: {gate['name']}</b></div>"
            f"<div style='color:{badge_color}; font-weight:700;'>{badge}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )
        st.caption(f"**Pass criteria:** {gate['criteria']}")
        if score < 4:
            st.error(f"**Risk if not addressed:** {gate['fail']}")

st.markdown("---")

# ============================================================
# CTA
# ============================================================
st.subheader("🚀 Want the Full Picture?")
st.markdown(
    "The complete **60-question assessment** generates a board-ready report with "
    "regulatory gap analysis, risk register, 90-day roadmap, and 6 policy templates — "
    "the same depth Big 4 firms charge AED 50,000–150,000 for."
)

mailto = (
    f"mailto:{CONTACT_EMAIL}"
    "?subject=Full%20AI%20Governance%20Assessment%20Request"
    "&body=Hi%20Bhargav%2C%0A%0AI%20completed%20the%20Quick%20Score%20and%20"
    "would%20like%20the%20full%2060-question%20assessment%20for%20%5Bcompany%20name%5D.%0A%0AThanks%2C"
)

cta1, cta2 = st.columns(2)
with cta1:
    st.link_button("📧 Get Full Assessment", mailto, use_container_width=True)
with cta2:
    st.link_button("📅 Book 15-Minute Demo", CALENDLY_URL, use_container_width=True)

st.info(
    "**Or send 4 numbers — Revenue, Receivables, Inventory, Payables — "
    "for a free working capital check. 24 hours.**  \n"
    f"Email: **{CONTACT_EMAIL}**"
)

st.markdown("---")
st.caption(
    "PBV Finance | AI Governance & Automation | Privacy-First | India · UAE · KSA · UK"
)
