import streamlit as st
import base64
import os

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="About JobShield AI",
    page_icon="🛡️",
    layout="wide"
)

# =========================================
# LOAD BACKGROUND IMAGE
# =========================================

def get_base64(file_path):

    if not os.path.exists(file_path):
        return ""

    with open(file_path, "rb") as f:

        data = f.read()

    return base64.b64encode(data).decode()


bg = get_base64("assets/background.png")

# =========================================
# BACKGROUND STYLE
# =========================================

if bg:

    background_style = f"""
    background-image:
    linear-gradient(
        rgba(5,8,22,0.90),
        rgba(5,8,22,0.95)
    ),
    url("data:image/png;base64,{bg}");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    """

else:

    background_style = """
    background:
    linear-gradient(
        135deg,
        #050816,
        #0f172a,
        #111827
    );
    """

# =========================================
# CSS
# =========================================

st.markdown(f"""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {{

    font-family: 'Poppins', sans-serif;

    color: white;

    -webkit-font-smoothing: antialiased;

    text-rendering: optimizeLegibility;
}}

.stApp {{

    {background_style}

    color: white;
}}

/* HIDE STREAMLIT */

#MainMenu {{
    visibility: hidden;
}}

footer {{
    visibility: hidden;
}}

header {{
    visibility: hidden;
}}

/* MAIN CONTAINER */

.main-container {{

    padding: 2rem 4rem;
}}

/* HERO */

.hero {{

    text-align: center;

    padding-top: 35px;

    padding-bottom: 20px;
}}

.hero-title {{

    font-size: 64px;

    font-weight: 700;

    color: white;

    margin-bottom: 12px;

    letter-spacing: 1px;
}}

.hero-subtitle {{

    font-size: 20px;

    color: #CBD5E1;
}}

/* GLASS CARD */

.glass-card {{

    background:
    rgba(15,23,42,0.72);

    backdrop-filter: blur(16px);

    border-radius: 28px;

    padding: 45px;

    margin-top: 30px;

    border:
    1px solid rgba(255,255,255,0.08);

    box-shadow:
    0 0 35px rgba(168,85,247,0.15);
}}

/* SECTION TITLE */

.section-title {{

    font-size: 30px;

    font-weight: 700;

    color: #C084FC;

    margin-top: 10px;

    margin-bottom: 18px;
}}

/* DESCRIPTION */

.description {{

    color: #CBD5E1;

    font-size: 17px;

    line-height: 1.9;
}}

/* FEATURE GRID */

.feature-grid {{

    display: grid;

    grid-template-columns: repeat(4, 1fr);

    gap: 20px;

    margin-top: 25px;
}}

/* FEATURE CARD */

.feature-card {{

    background:
    rgba(30,41,59,0.82);

    border:
    1px solid rgba(255,255,255,0.08);

    border-radius: 22px;

    padding: 25px;

    transition: 0.3s ease;

    min-height: 220px;
}}

.feature-card:hover {{

    transform: translateY(-5px);

    box-shadow:
    0 0 20px rgba(168,85,247,0.25);
}}

.feature-card h3 {{

    color: white;

    font-size: 20px;

    margin-bottom: 12px;
}}

.feature-card p {{

    color: #CBD5E1;

    line-height: 1.7;

    font-size: 15px;
}}

/* FOOTER */

.footer {{

    text-align: center;

    margin-top: 60px;

    color: #94A3B8;

    font-size: 14px;

    padding-bottom: 25px;
}}

/* MOBILE */

@media screen and (max-width: 1000px) {{

    .feature-grid {{

        grid-template-columns: repeat(2, 1fr);
    }}
}}

@media screen and (max-width: 700px) {{

    .feature-grid {{

        grid-template-columns: 1fr;
    }}

    .hero-title {{

        font-size: 42px;
    }}

    .main-container {{

        padding: 1rem;
    }}

    .glass-card {{

        padding: 25px;
    }}
}}

</style>
""", unsafe_allow_html=True)

# =========================================
# MAIN CONTAINER
# =========================================

st.markdown(
    '<div class="main-container">',
    unsafe_allow_html=True
)

# =========================================
# HERO SECTION
# =========================================

st.markdown("""
<div class="hero">

<div class="hero-title">
🛡️ JobShield AI
</div>

<div class="hero-subtitle">
AI-Powered Fake Job Detection Platform
</div>

</div>
""", unsafe_allow_html=True)

# =========================================
# GLASS CARD
# =========================================

st.markdown(
    '<div class="glass-card">',
    unsafe_allow_html=True
)

# =========================================
# ABOUT SECTION
# =========================================

st.markdown("""
<div class="section-title">
🌍 About The Platform
</div>

<div class="description">

JobShield AI is an intelligent fake job detection platform designed to protect job seekers from online recruitment scams using Artificial Intelligence and Natural Language Processing.

The system analyzes suspicious hiring patterns, unrealistic offers, fake recruiter behavior, and fraudulent wording to identify dangerous job postings in real time.

Built with modern AI technologies and a futuristic cybersecurity-inspired interface, JobShield AI helps users make safer career decisions online.

</div>
""", unsafe_allow_html=True)

# =========================================
# FEATURES SECTION
# =========================================

# =========================================
# FEATURES SECTION
# =========================================

st.markdown("""
<div class="section-title">
🚀 Core Features
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>🤖 AI Detection</h3>
        <p>
        Machine learning models intelligently identify suspicious and fraudulent job postings.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>📊 Fraud Score</h3>
        <p>
        Generates smart scam probability analysis with AI confidence scores.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3>⚡ Real-Time Scan</h3>
        <p>
        Instantly analyzes job descriptions and delivers predictions within seconds.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-card">
        <h3>🌌 Modern Interface</h3>
        <p>
        Premium glassmorphism UI with futuristic dashboard design.
        </p>
    </div>
    """, unsafe_allow_html=True)

# =========================================
# CLOSE GLASS CARD
# =========================================

st.markdown(
    "</div>",
    unsafe_allow_html=True
)

# =========================================
# FOOTER
# =========================================

st.markdown("""
<div class="footer">

Built using AI • NLP • Machine Learning • Cybersecurity

</div>
""", unsafe_allow_html=True)

# =========================================
# CLOSE MAIN CONTAINER
# =========================================

st.markdown(
    "</div>",
    unsafe_allow_html=True
)