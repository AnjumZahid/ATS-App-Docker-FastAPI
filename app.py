import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader
import re
import os
from dotenv import load_dotenv

load_dotenv()

# Configure the Streamlit Page
st.set_page_config(page_title="ATS Resume Expert", layout="wide")
st.title("ATS-Resume-Analyzer")  # for display

# Function to extract text from PDF
def extract_text_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    pdf_txt = '\n'.join(page.extract_text() or "" for page in reader.pages)
    return pdf_txt.strip() if pdf_txt.strip() else "No extractable text found in the PDF"

# Configure Gemini API using environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY is None:
    st.error("GEMINI_API_KEY is missing. Check your Render environment variables.")

genai.configure(api_key=GEMINI_API_KEY)

# Function to generate responses using Gemini
def get_gemini_response(job_description, resume_text, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([job_description, resume_text, prompt])
    return response.text

# Define sidebar
with st.sidebar:
    st.header("Upload Resume & Job Description")
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
    job_description = st.text_area("Enter Job Description")

# Define prompts for resume evaluation
ats_review_prompt = """
You are an experienced technical HR manager with ATS expertise. Evaluate the resume against the job description
and provide a professional assessment, highlighting strengths, weaknesses, and missing keywords.
Conclude with a summary of the candidate's alignment with the role.
"""

percentage_match_prompt = """
Analyze the resume against the job role description and provide only the percentage match as a numeric value.
Do not include any additional text.
"""

# Initialize session state for responses
if "ats_response" not in st.session_state:
    st.session_state.ats_response = None

if "match_percentage" not in st.session_state:
    st.session_state.match_percentage = None

# --- Keep Buttons at Top ---
st.divider()
col_btn1, col_btn2 = st.columns([3, 1])  # Left button wider, right button smaller

with col_btn1:
    analyze_button = st.button("Analyze Resume")

with col_btn2:
    match_button = st.button("Get Percentage Match", use_container_width=True)  # Align right

st.divider()

# --- Resume Processing ---
if uploaded_file:
    st.success("Resume Uploaded Successfully")
    resume_text = extract_text_pdf(uploaded_file)

    # Left: Resume Analysis
    col1, col2 = st.columns([3, 1])  # Main content (3x), Right (1x)
    
    with col1:
        if analyze_button:
            st.session_state.ats_response = get_gemini_response(job_description, resume_text, ats_review_prompt)

        if st.session_state.ats_response:
            st.subheader("Resume Analysis:")
            st.write(st.session_state.ats_response)

    # Right: Percentage Match
    with col2:
        if match_button:
            response = get_gemini_response(job_description, resume_text, percentage_match_prompt)
            st.session_state.match_percentage = int(re.search(r'\d+', response).group()) if re.search(r'\d+', response) else 0

        if st.session_state.match_percentage is not None:
            st.subheader("Job Match Percentage")
            st.write(f"Match Score: {st.session_state.match_percentage}%")
            
            # Progress bar with red & green
            filled_ratio = st.session_state.match_percentage / 100.0
            st.progress(filled_ratio)

# --- Error Handling ---
elif (analyze_button or match_button) and not uploaded_file:
    st.warning("Please upload a resume before proceeding.")
