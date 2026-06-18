import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from database import fetch_all

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

# =========================================
# CUSTOM CSS
# =========================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {

    font-family: 'Poppins', sans-serif;
}

/* MAIN BACKGROUND */

.stApp {

    background:
    linear-gradient(
        135deg,
        #050816,
        #0f172a,
        #111827
    );

    color: white;
}

/* HIDE STREAMLIT */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* TITLE */

.main-title {

    font-size: 48px;

    font-weight: 700;

    background:
    linear-gradient(
        90deg,
        #ffffff,
        #c084fc
    );

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;

    margin-bottom: 5px;
}

/* SUBTITLE */

.subtitle {

    color: #CBD5E1;

    font-size: 18px;

    margin-bottom: 30px;
}

/* METRIC CARDS */

[data-testid="metric-container"] {

    background:
    rgba(15,23,42,0.75);

    border:
    1px solid rgba(255,255,255,0.08);

    padding: 20px;

    border-radius: 22px;

    box-shadow:
    0 0 25px rgba(168,85,247,0.12);

    transition: 0.3s ease;
}

[data-testid="metric-container"]:hover {

    transform: translateY(-4px);

    box-shadow:
    0 0 30px rgba(168,85,247,0.20);
}

/* DATAFRAME */

[data-testid="stDataFrame"] {

    border-radius: 18px;

    overflow: hidden;

    border:
    1px solid rgba(255,255,255,0.08);
}

/* ALERTS */

.stAlert {

    border-radius: 15px;
}

/* SECTION HEADINGS */

h2, h3 {

    color: white;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# PAGE HEADER
# =========================================

st.markdown("""
<div class="main-title">
📊 JobShield AI Dashboard
</div>

<div class="subtitle">
Monitor fake job detection statistics and recent activity.
</div>
""", unsafe_allow_html=True)

# =========================================
# FETCH DATABASE RECORDS
# =========================================

rows = fetch_all()

total = len(rows)

fake_count = sum(
    1 for row in rows
    if "FAKE" in row[2].upper()
)

real_count = sum(
    1 for row in rows
    if "REAL" in row[2].upper()
)

# =========================================
# METRICS
# =========================================

st.subheader("📌 Overview")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Total Jobs Checked",
        total
    )

with col2:

    st.metric(
        "Fake Jobs Detected",
        fake_count
    )

with col3:

    st.metric(
        "Legitimate Jobs",
        real_count
    )

st.markdown("<br>", unsafe_allow_html=True)

# =========================================
# PIE CHART
# =========================================

st.subheader("📈 Detection Distribution")

if total > 0:

    labels = [
        "Fake Jobs",
        "Legitimate Jobs"
    ]

    sizes = [
        fake_count,
        real_count
    ]

    fig, ax = plt.subplots(
        figsize=(5, 5)
    )

    ax.pie(
        sizes,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90
    )

    ax.axis("equal")

    fig.patch.set_facecolor('#0f172a')

    st.pyplot(fig)

else:

    st.info(
        "No prediction data available yet."
    )

st.markdown("<br>", unsafe_allow_html=True)

# =========================================
# RECENT PREDICTIONS
# =========================================

st.subheader("📝 Recent Predictions")

if total > 0:

    df = pd.DataFrame(
        rows,
        columns=[
            "ID",
            "Job Description",
            "Result"
        ]
    )

    st.dataframe(
        df,
        use_container_width=True,
        height=400
    )

else:

    st.warning(
        "Prediction history is empty."
    )

st.markdown("<br>", unsafe_allow_html=True)

# =========================================
# AI INSIGHTS
# =========================================

st.subheader("🧠 AI Insights")

if total == 0:

    st.info(
        "Analyze some job descriptions to generate insights."
    )

elif fake_count > real_count:

    st.error(
        "⚠️ High number of suspicious job postings detected."
    )

elif real_count > fake_count:

    st.success(
        "✅ Most analyzed jobs appear legitimate."
    )

else:

    st.info(
        "📌 Equal number of fake and real jobs detected."
    )

st.markdown("<br>", unsafe_allow_html=True)

# =========================================
# SYSTEM STATUS
# =========================================

st.subheader("🟢 System Status")

st.success(
    "AI Detection System Active"
)