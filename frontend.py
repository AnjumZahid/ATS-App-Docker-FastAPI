import streamlit as st
import requests

st.set_page_config(page_title="ATS Resume App", layout="wide")
st.title("ATS-Resume-Analyzer")

backend_url = "http://localhost:8000"  # Replace with public URL after deploy

with st.sidebar:
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
    job_description = st.text_area("Enter Job Description")

st.divider()
col_btn1, col_btn2 = st.columns([3, 1])
with col_btn1:
    analyze_button = st.button("Analyze Resume")
with col_btn2:
    match_button = st.button("Get Percentage Match")

st.divider()

if uploaded_file and job_description:
    files = {"file": uploaded_file}
    data = {"job_description": job_description}

    col1, col2 = st.columns([3, 1])

    with col1:
        if analyze_button:
            response = requests.post(f"{backend_url}/analyze_resume/", files=files, data=data)
            st.subheader("Resume Analysis")
            st.write(response.json().get("analysis", "Error"))

    with col2:
        if match_button:
            response = requests.post(f"{backend_url}/match_percentage/", files=files, data=data)
            percent = response.json().get("percentage", 0)
            st.subheader("Job Match Percentage")
            st.write(f"Match Score: {percent}%")
            st.progress(percent / 100.0)
else:
    if analyze_button or match_button:
        st.warning("Please upload a resume and job description.")
