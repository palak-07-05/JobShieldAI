import streamlit as st
import time
import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt
from src.predict import predict_job
from src.preprocess import clean_text
from database import (
    init_db,
    insert_prediction,
    fetch_all
)
from agents.fraud_agent import analyze_job
from utils.pdf_parser import (
    extract_text_from_pdf
)
# LOAD CSS
def load_css():
    with open("styles/style.css", "r", encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )
# PAGE CONFIG
st.set_page_config(
    page_title="JobShield AI",
    page_icon="🛡️",
    layout="wide"
)

# APPLY CSS
load_css()
# DATABASE INIT
init_db()
# SIDEBAR
st.sidebar.title("🛡️ JobShield AI")
menu = st.sidebar.selectbox(
    "📂 Navigation",
    [
        "Predict",
        "Dashboard",
        "History"
    ]
)
# =========================================
# PREDICT PAGE
# =========================================

if menu == "Predict":

    st.markdown("""
    <div class="hero-title">
        <span class="shield-icon">🛡️</span>
        <span class="gradient-text">JobShield AI</span>
    </div>

    <div class="hero-subtitle">
        AI-Powered Fake Job Detection Platform
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.subheader("📄 Paste Job Description")

    uploaded_pdf = st.file_uploader(
        "📄 Upload Job Description PDF",
        type=["pdf"]
    )

    pdf_text = ""

    if uploaded_pdf:

        pdf_text = extract_text_from_pdf(
            uploaded_pdf
        )

        st.success(
            "PDF uploaded successfully."
        )

    job_text = st.text_area(

        label="",

        value=pdf_text,

        height=300,

        placeholder="""
Paste complete job description here...

Example:
Company hiring urgently for remote work.
No experience required.
Weekly payout available.
Apply now.
"""
    )

    # =========================================
    # ANALYZE BUTTON
    # =========================================

    if st.button("🔍 Analyze Job"):

        if not job_text.strip():

            st.warning(
                "Please enter a job description."
            )

        else:

            with st.spinner(
                "Analyzing job description..."
            ):

                time.sleep(1)

                cleaned_text = clean_text(
                    job_text
                )

                result = predict_job(
                    cleaned_text
                )
                fake_score = result["fake_score"]
                real_score = result["real_score"]
                is_fake = (
                    result["prediction"] == 1
                )
                final_result = (
                    "FAKE JOB"
                    if is_fake
                    else "REAL JOB"
                )
                # SAVE TO DATABASE
                ai_report = analyze_job(job_text)

            insert_prediction(
                job_text,
                final_result,
                ai_report
            )   
            st.markdown("---")
            st.subheader("🧠 Detection Result")
            if is_fake:
                st.error(
                    "⚠️ Fake Job Detected"
                )
            else:
                st.success(
                    "✅ Legitimate Job Posting"
                )
            # METRICS
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    "Fake Probability",
                    f"{fake_score:.2f}%"
                )
            with col2:
                st.metric(
                    "Real Probability",
                    f"{real_score:.2f}%"
                )
            st.markdown("---")

            # =========================================
            # RISK BAR
            # =========================================

            st.subheader("📊 Scam Risk Level")

            st.progress(
                fake_score / 100
            )

            # =========================================
            # GAUGE CHART
            # =========================================

            fig = go.Figure(

                go.Indicator(

                    mode="gauge+number",

                    value=fake_score,

                    title={
                        "text": "Fraud Risk Score"
                    },

                    gauge={

                        "axis": {
                            "range": [0, 100]
                        },

                        "bar": {
                            "color": "#9333ea"
                        },

                        "steps": [

                            {
                                "range": [0, 30],
                                "color": "#14532d"
                            },

                            {
                                "range": [30, 70],
                                "color": "#b45309"
                            },

                            {
                                "range": [70, 100],
                                "color": "#991b1b"
                            }
                        ]
                    }
                )
            )

            fig.update_layout(

                height=400,

                paper_bgcolor="rgba(0,0,0,0)",

                font={
                    "color": "white"
                }
            )

            st.plotly_chart(

                fig,

                use_container_width=True
            )

            st.markdown("---")

            st.subheader(
                "🤖 Gemini AI Investigation"
            )

            with st.spinner(
                "Gemini analyzing..."
            ):

                try:

                    ai_report = analyze_job(
                        job_text
                    )

                    st.markdown(ai_report)

                except Exception as e:

                    st.error(
                        f"Gemini Analysis Failed: {str(e)}"
                    )
            # =========================================
            # FINAL MESSAGE
            # =========================================

            if fake_score >= 70:

                st.error("""
⚠️ This posting contains multiple suspicious scam indicators commonly found in fraudulent job listings.
                """)

            elif fake_score >= 40:

                st.warning("""
⚠️ This posting shows some suspicious characteristics.

Verify company details carefully before applying.
                """)

            else:

                st.success("""
✅ This posting appears relatively safe based on AI analysis.
                """)

# =========================================
# DASHBOARD PAGE
# =========================================

elif menu == "Dashboard":

    st.title("📊 JobShield AI Dashboard")

    st.markdown("""
Monitor fake job detection statistics,
AI insights, and recent prediction activity.
    """)

    st.markdown("---")

    rows = fetch_all()

    total = len(rows)

    fake_count = sum(

        1 for row in rows

        if "FAKE" in row[2]
    )

    real_count = sum(

        1 for row in rows

        if "REAL" in row[2]
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
            "Fake Jobs",
            fake_count
        )

    with col3:

        st.metric(
            "Real Jobs",
            real_count
        )

    st.markdown("---")

    # =========================================
    # PIE CHART
    # =========================================

    st.subheader("📈 Detection Distribution")

    if total > 0:

        labels = [
            "Fake Jobs",
            "Real Jobs"
        ]

        sizes = [
            fake_count,
            real_count
        ]

        fig, ax = plt.subplots(
            figsize=(5, 5)
        )

        colors = [
            "#ef4444",
            "#22c55e"
        ]

        ax.pie(

            sizes,

            labels=labels,

            autopct="%1.1f%%",

            startangle=90,

            colors=colors
        )

        ax.axis("equal")

        fig.patch.set_facecolor("#0f172a")

        st.pyplot(fig)

    else:

        st.info(
            "No prediction data available yet."
        )

    st.markdown("---")

    # =========================================
    # RECENT PREDICTIONS
    # =========================================

    st.subheader("🕘 Recent Predictions")

    if total > 0:

        df = pd.DataFrame(

            rows,

            columns=[
                "ID",
                "Job Description",
                "Result"
            ]
        )

        df = df[::-1]

        st.dataframe(

            df,

            use_container_width=True
        )

    else:

        st.warning(
            "Prediction history is empty."
        )

    st.markdown("---")

    # =========================================
    # AI INSIGHTS
    # =========================================

    st.subheader("🧠 AI Insights")
    st.markdown("""
### 🤖 Gemini Summary

This dashboard combines:
- Machine Learning Fraud Detection
- Gemini AI Explainability
- Historical Analysis
- Risk Monitoring
""")

    if total == 0:

        st.info(
            "Analyze some job descriptions to generate insights."
        )

    elif fake_count > real_count:

        st.error("""
⚠️ High number of suspicious job postings detected.

Users should verify recruiter details,
company websites, and salary claims carefully.
        """)

    elif real_count > fake_count:

        st.success("""
✅ Most analyzed job postings appear legitimate based on AI analysis.
        """)

    else:

        st.info("""
📌 Equal number of fake and real jobs detected.
        """)

    st.markdown("---")

    # =========================================
    # SYSTEM STATUS
    # =========================================

    st.subheader("🖥️ System Status")

    st.success(
        "🟢 AI Detection System Active"
    )

# =========================================
# HISTORY PAGE
# =========================================

elif menu == "History":

    st.title("📜 Prediction History")

    rows = fetch_all()

    if len(rows) > 0:

        for row in rows[::-1]:

            st.markdown("---")

            st.subheader(
                f"Record #{row[0]}"
            )

            st.markdown("### 📄 Job Description")

            st.write(row[1])

            st.markdown("### 🧠 Prediction Result")

            if "FAKE" in row[2]:

                st.error(row[2])

            else:

                st.success(row[2])

    else:

        st.warning(
            "No prediction history found."
        )