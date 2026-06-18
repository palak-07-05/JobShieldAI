import streamlit as st
import time
import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt
import config
from src.predict import predict_job
from src.preprocess import clean_text
from database import (
    init_db,
    insert_prediction,
    fetch_all,
    get_total_predictions,
    get_fake_count,
    get_real_count
)
from agents.fraud_agent import analyze_job, generate_dashboard_insights
from utils.pdf_parser import extract_text_from_pdf


def sanitize_unicode(text: str) -> str:
    """Replace invalid surrogate characters that can crash Streamlit widgets."""
    if text is None:
        return ""
    return str(text).encode("utf-8", "replace").decode("utf-8")

# =========================================
# PAGE CONFIGURATION
# =========================================

st.set_page_config(
    page_title="🛡️ JobShield AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================
# CUSTOM CSS
# =========================================

def load_css():
    """Load custom CSS styling"""
    css = """
    <style>
    :root {
        --primary: #9333ea;
        --secondary: #c084fc;
        --danger: #ef4444;
        --success: #22c55e;
        --warning: #f59e0b;
        --dark: #050816;
        --card: rgba(15, 23, 42, 0.72);
        --text: #E2E8F0;
    }
    
    body {
        background-color: var(--dark);
        color: var(--text);
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #9333ea, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin: 2rem 0;
        animation: fadeIn 1s ease-in;
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        text-align: center;
        color: #94a3b8;
        margin-bottom: 2rem;
    }
    
    .shield-icon {
        font-size: 4rem;
        display: block;
    }
    
    .stMetric {
        background-color: var(--card);
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    .highlight {
        background-color: var(--card);
        padding: 1rem;
        border-left: 4px solid var(--primary);
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Apply CSS
load_css()

# =========================================
# DATABASE INITIALIZATION
# =========================================

init_db()

# =========================================
# SIDEBAR NAVIGATION
# =========================================

with st.sidebar:
    st.markdown("""
    <div class="hero-title" style="font-size: 2rem; margin: 1rem 0;">
        🛡️ JobShield AI
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    menu = st.selectbox(
        "📂 Navigation",
        [
            "🔍 Predict",
            "📊 Dashboard",
            "📜 History",
            "⚙️ Settings"
        ],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("""
    ### About
    JobShield AI detects fraudulent job postings using:
    - 🤖 Machine Learning Classification
    - 🧠 Gemini AI Analysis
    - 📊 Advanced NLP Processing
    """)

# =========================================
# PREDICT PAGE
# =========================================

if menu == "🔍 Predict":

    st.markdown("""
    <div class="hero-title">
        <span class="shield-icon">🛡️</span>
        <span>JobShield AI</span>
    </div>
    <div class="hero-subtitle">
        AI-Powered Fake Job Detection Platform
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Input section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📄 Job Description Input")
    
    with col2:
        input_method = st.radio(
            "Input Method",
            ["📝 Text", "📄 PDF"],
            horizontal=True,
            label_visibility="collapsed"
        )

    pdf_text = ""
    
    # Handle different input methods
    if input_method == "📄 PDF":
        uploaded_pdf = st.file_uploader(
            "Upload Job Description PDF",
            type=["pdf"],
            label_visibility="collapsed"
        )
        
        if uploaded_pdf:
            try:
                pdf_text = sanitize_unicode(extract_text_from_pdf(uploaded_pdf))
                st.success("✅ PDF uploaded and processed successfully")
            except Exception as e:
                st.error(f"❌ Error processing PDF: {str(e)}")
    
    # Text area for job description
    job_text = st.text_area(
        "Paste complete job description here",
        value=pdf_text,
        height=300,
        key="job_description_input",
        placeholder="""Example:
Earn $5000 per month from home!
No experience required.
Work from anywhere.
Flexible hours.
Limited positions available.
Apply now!""",
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Analyze button
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        analyze_btn = st.button(
            "🔍 Analyze Job",
            use_container_width=True,
            type="primary"
        )
    
    with col2:
        clear_btn = st.button(
            "🗑️ Clear",
            use_container_width=True
        )
    
    if clear_btn:
        st.rerun()

    # =========================================
    # ANALYSIS LOGIC
    # =========================================

    if analyze_btn:
        job_text = sanitize_unicode(job_text)

        if not job_text.strip():
            st.warning("⚠️ Please enter a job description to analyze")

        elif not config.GEMINI_API_KEY:
            st.error(
                "Gemini API key is missing. Add GEMINI_API_KEY to your .env file, "
                "then restart the Streamlit app."
            )
        
        else:
            # Progress indicators
            progress_bar = st.progress(0)
            status_text = st.empty()

            try:
                # Step 1: Text cleaning
                status_text.text("🔄 Step 1: Cleaning text...")
                progress_bar.progress(20)
                time.sleep(0.5)
                
                cleaned_text = clean_text(job_text)

                # Step 2: ML Prediction
                status_text.text("🔄 Step 2: Running ML prediction...")
                progress_bar.progress(40)
                time.sleep(0.5)
                
                result = predict_job(cleaned_text)
                fake_score = result.get("fake_score", 0)
                real_score = result.get("real_score", 0)
                is_fake = result.get("prediction", 0) == 1

                # Step 3: Gemini AI Analysis
                status_text.text("🔄 Step 3: Gemini AI deep analysis...")
                progress_bar.progress(60)
                time.sleep(0.5)
                
                ai_report = analyze_job(job_text)

                # Step 4: Saving results
                status_text.text("🔄 Step 4: Saving results...")
                progress_bar.progress(80)
                time.sleep(0.5)
                
                final_result = "FAKE JOB" if is_fake else "REAL JOB"
                insert_prediction(job_text, final_result, ai_report)

                # Complete
                status_text.text("✅ Analysis complete!")
                progress_bar.progress(100)
                time.sleep(0.5)
                
                status_text.empty()
                progress_bar.empty()

                # =========================================
                # RESULTS DISPLAY
                # =========================================

                st.markdown("---")

                st.subheader("🧠 Detection Result")

                # Result badge
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    if is_fake:
                        st.error("⚠️ FAKE JOB DETECTED", icon="🚨")
                    else:
                        st.success("✅ LEGITIMATE JOB", icon="✅")
                
                with col2:
                    st.metric(
                        "Confidence",
                        f"{result.get('confidence', 0)*100:.1f}%"
                    )

                st.markdown("---")

                # Probability metrics
                st.subheader("📊 Fraud Probability Analysis")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric(
                        "🔴 Fake Probability",
                        f"{fake_score:.2f}%",
                        delta=None
                    )
                
                with col2:
                    st.metric(
                        "🟢 Real Probability",
                        f"{real_score:.2f}%",
                        delta=None
                    )

                st.markdown("---")

                # Risk gauge
                st.subheader("📈 Risk Assessment Gauge")
                
                fig = go.Figure(
                    go.Indicator(
                        mode="gauge+number",
                        value=fake_score,
                        title={"text": "Fraud Risk Score (0-100)"},
                        gauge={
                            "axis": {"range": [0, 100]},
                            "bar": {"color": "#9333ea"},
                            "steps": [
                                {"range": [0, 30], "color": "rgba(34, 197, 94, 0.3)"},
                                {"range": [30, 70], "color": "rgba(245, 158, 11, 0.3)"},
                                {"range": [70, 100], "color": "rgba(239, 68, 68, 0.3)"}
                            ],
                            "threshold": {
                                "line": {"color": "red", "width": 4},
                                "thickness": 0.75,
                                "value": 70
                            }
                        }
                    )
                )
                
                fig.update_layout(
                    height=400,
                    paper_bgcolor="rgba(0,0,0,0)",
                    font={"color": "#E2E8F0", "size": 14},
                    margin=dict(l=20, r=20, t=60, b=20)
                )
                
                st.plotly_chart(fig, use_container_width=True)

                st.markdown("---")

                # Gemini AI Detailed Analysis
                st.subheader("🤖 Gemini AI Deep Analysis")
                
                with st.expander("📋 View Full Analysis", expanded=True):
                    st.markdown(ai_report)

                st.markdown("---")

                # Risk recommendations
                st.subheader("💡 Risk Assessment & Recommendations")
                
                if fake_score >= 70:
                    st.error("""
                    ### 🚨 HIGH RISK - Likely Scam
                    
                    This posting contains multiple red flags commonly found in fraudulent job listings.
                    
                    **Recommended Actions:**
                    - ❌ Do NOT apply to this job
                    - ❌ Do NOT share personal information
                    - ❌ Do NOT pay any fees
                    - 📢 Report this posting if possible
                    """)
                
                elif fake_score >= 40:
                    st.warning("""
                    ### ⚠️ MEDIUM RISK - Proceed with Caution
                    
                    This posting shows some suspicious characteristics.
                    
                    **Recommended Actions:**
                    - ✓ Research the company independently
                    - ✓ Verify recruiter details
                    - ✓ Check company website and LinkedIn
                    - ✓ Never pay upfront fees
                    - ✓ Be cautious about personal information
                    """)
                
                else:
                    st.success("""
                    ### ✅ LOW RISK - Likely Legitimate
                    
                    This posting appears relatively safe based on AI analysis.
                    
                    **Still Recommended:**
                    - ✓ Verify company details
                    - ✓ Research the role
                    - ✓ Protect your personal information
                    - ✓ Trust your instincts
                    """)

            except Exception as e:
                status_text.empty()
                progress_bar.empty()
                st.error(f"❌ Analysis Error: {str(e)}")

# =========================================
# DASHBOARD PAGE
# =========================================

elif menu == "📊 Dashboard":

    st.title("📊 JobShield AI Dashboard")
    
    st.markdown("""
    Monitor fake job detection statistics, AI insights, and prediction activity.
    """)

    st.markdown("---")

    # Fetch data
    rows = fetch_all()
    total = len(rows)
    fake_count = sum(1 for row in rows if "FAKE" in row[2])
    real_count = sum(1 for row in rows if "REAL" in row[2])

    # =========================================
    # KPI METRICS
    # =========================================

    st.subheader("📌 Key Performance Indicators")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📊 Total Analyzed", total, delta=None)

    with col2:
        st.metric("🚨 Fake Jobs", fake_count, delta=None)

    with col3:
        st.metric("✅ Real Jobs", real_count, delta=None)

    with col4:
        if total > 0:
            accuracy = (real_count / total) * 100
            st.metric("🎯 Legitimacy Rate", f"{accuracy:.1f}%", delta=None)
        else:
            st.metric("🎯 Legitimacy Rate", "N/A", delta=None)

    st.markdown("---")

    # =========================================
    # VISUALIZATIONS
    # =========================================

    if total > 0:
        col1, col2 = st.columns(2)

        # Pie chart
        with col1:
            st.subheader("📈 Detection Distribution")
            
            fig, ax = plt.subplots(figsize=(6, 6))
            
            colors = ["#ef4444", "#22c55e"]
            sizes = [fake_count, real_count]
            labels = [f"Fake Jobs\n({fake_count})", f"Real Jobs\n({real_count})"]
            
            wedges, texts, autotexts = ax.pie(
                sizes,
                labels=labels,
                autopct="%1.1f%%",
                startangle=90,
                colors=colors,
                textprops={"color": "#E2E8F0", "weight": "bold"}
            )
            
            ax.axis("equal")
            fig.patch.set_facecolor("#050816")
            
            st.pyplot(fig, use_container_width=True)

        # Statistics
        with col2:
            st.subheader("📊 Statistics")
            
            if total > 0:
                st.write(f"**Total Predictions:** {total}")
                st.write(f"**Fake Jobs:** {fake_count} ({fake_count/total*100:.1f}%)")
                st.write(f"**Real Jobs:** {real_count} ({real_count/total*100:.1f}%)")
                
                st.markdown("---")
                
                st.write("**Recent Analysis:**")
                if rows:
                    st.write(f"Latest prediction: {rows[0][0]}")

        st.markdown("---")

        # Recent predictions table
        st.subheader("🕘 Recent Predictions (Latest 10)")
        
        df = pd.DataFrame(
            rows[:10],
            columns=["ID", "Job Description", "Result", "AI Report", "Timestamp"]
        )
        
        # Format for display
        df_display = df.copy()
        df_display["Job Description"] = df_display["Job Description"].str[:100] + "..."
        df_display = df_display[["ID", "Job Description", "Result", "Timestamp"]]
        
        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("📊 No prediction data available yet. Start by analyzing some job postings!")

    st.markdown("---")

    # =========================================
    # AI INSIGHTS
    # =========================================

    st.subheader("🧠 AI-Generated Insights")
    
    if total > 0:
        with st.spinner("Generating insights..."):
            insights = generate_dashboard_insights(rows)
            st.markdown(insights)
    else:
        st.info("Analyze some job descriptions to generate AI insights.")

    st.markdown("---")

    # System status
    st.subheader("🖥️ System Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.success("🟢 ML Model: Active")
    
    with col2:
        if config.GEMINI_API_KEY:
            st.success("🟢 Gemini AI: Connected")
        else:
            st.error("🔴 Gemini AI: API key missing")
    
    with col3:
        st.success("🟢 Database: Active")

# =========================================
# HISTORY PAGE
# =========================================

elif menu == "📜 History":

    st.title("📜 Prediction History")

    rows = fetch_all()

    if len(rows) > 0:
        
        # Add search/filter
        search = st.text_input("🔍 Search predictions...")
        
        st.markdown("---")

        # Display predictions
        for idx, row in enumerate(rows[::-1]):
            if search.lower() in row[1].lower():
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"### Record #{row[0]}")
                        st.markdown(f"**Job Description:** {row[1][:200]}...")
                        
                        if "FAKE" in row[2]:
                            st.error(f"**Result:** {row[2]}", icon="🚨")
                        else:
                            st.success(f"**Result:** {row[2]}", icon="✅")
                    
                    with col2:
                        if row[4]:
                            st.write(f"🕐 *{row[4]}*")
                        if "FAKE" in row[2]:
                            st.error("🚨 FAKE")
                        else:
                            st.success("✅ REAL")

                    with st.expander("📋 View Full Analysis"):
                        st.markdown(row[3] if row[3] else "No analysis available")
                    
                    st.markdown("---")

    else:
        st.warning("📜 No prediction history found. Start analyzing job postings!")

# =========================================
# SETTINGS PAGE
# =========================================

elif menu == "⚙️ Settings":

    st.title("⚙️ Settings")

    st.markdown("---")

    st.subheader("ℹ️ Application Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**App Name:** JobShield AI")
        st.write("**Version:** 1.0.0")
        st.write("**Status:** Active")
    
    with col2:
        total = get_total_predictions()
        fake = get_fake_count()
        real = get_real_count()
        
        st.write(f"**Total Predictions:** {total}")
        st.write(f"**Fake Detected:** {fake}")
        st.write(f"**Real Detected:** {real}")

    st.markdown("---")

    st.subheader("🔧 Configuration")
    
    st.write("**ML Model:** Logistic Regression (TF-IDF)")
    st.write("**AI Engine:** Google Gemini")
    st.write(f"**Gemini API Key:** {'Configured' if config.GEMINI_API_KEY else 'Missing'}")
    st.write("**Database:** SQLite")

    st.markdown("---")

    st.subheader("📚 About")
    
    st.markdown("""
    ### JobShield AI - Fake Job Detection Platform
    
    **Purpose:** Identify and protect job seekers from fraudulent job postings using AI and ML.
    
    **Technology Stack:**
    - 🐍 Python
    - 🎈 Streamlit
    - 🤖 Machine Learning (Scikit-learn)
    - 🧠 Gemini AI
    - 📊 NLP & Text Processing
    - 💾 SQLite Database
    
    **Key Features:**
    - Real-time job posting analysis
    - ML-based fraud detection
    - Gemini AI deep analysis
    - Historical prediction tracking
    - Risk assessment & recommendations
    - Dashboard analytics
    
    **Made with ❤️ for Job Seekers**
    """)

    st.markdown("---")
    
    st.subheader("📞 Support")
    
    st.info("""
    For issues or feedback, please contact the development team.
    
    - 📧 Email: support@jobshield.ai
    - 🐙 GitHub: [JobShield AI](https://github.com/jobshield)
    - 💬 Discord: [Community](https://discord.gg/jobshield)
    """)
