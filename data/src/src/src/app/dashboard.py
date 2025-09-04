import streamlit as st
import json
import os
from src.scoring_engine import NGOScorecard
from src.nlp_analyzer import extract_themes
from src.report_generator import generate_html_report

st.set_page_config(page_title="W NGO Evaluator", layout="wide")

st.title("📊 (W) NGO External Evaluation Model")
st.markdown("Interactive tool to assess performance, added value, and improvement pathways.")

# File Upload
uploaded_file = st.file_uploader("Upload evaluation data (JSON)", type="json")
if uploaded_file:
    data = json.load(uploaded_file)
else:
    if os.path.exists("data/sample_input.json"):
        with open("data/sample_input.json", "r") as f:
            data = json.load(f)
        st.info("Using sample data. Upload your own to replace.")
    else:
        st.error("No data found. Please upload a JSON file.")
        st.stop()

# Initialize model
model = NGOScorecard()

# Compute Scores
gai = model.goal_achievement_index(data['goal_achievement'])
wci = model.work_capacity_index(data['work_capacity'])
avi = model.added_value_index(data['added_value'])
audit = model.inclusiveness_audit(data['inclusiveness'])
scores = model.get_scores()

# Display Scores
col1, col2, col3 = st.columns(3)
col1.metric("Goal Achievement Index (GAI)", f"{gai:.1f}/100")
col2.metric("Work Capacity Index (WCI)", f"{wci:.1f}/100")
col3.metric("Added Value Index (AVI)", f"{avi:.1f}/100")

# Inclusiveness
st.subheader("♿ Inclusiveness & CRPD Compliance")
if audit["compliant"]:
    st.success("✅ Fully compliant with inclusiveness criteria")
else:
    st.warning("⚠️ Non-compliant: Missing " + ", ".join(audit["missing"]))

# Themes from Interviews
st.subheader("🔍 Key Themes from Qualitative Feedback")
themes = extract_themes(data['qualitative']['interviews'])
theme_df = [{"Theme": t[0].title(), "Frequency": t[1]} for t in themes]
st.bar_chart(pd.DataFrame(theme_df).set_index("Theme"))

# Generate Report
if st.button("Generate Final Report"):
    generate_html_report(scores, audit, themes)
    with open("output/report.html", "r") as f:
        st.download_button("Download HTML Report", f.read(), "w_evaluation.html", "text/html")
    st.success("Report generated! Check the `output/` folder or download above.")
