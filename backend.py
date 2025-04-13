from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import google.generativeai as genai
from pypdf import PdfReader

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

app = FastAPI()

# Allow CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_text_pdf(file_data):
    reader = PdfReader(file_data)
    return '\n'.join(page.extract_text() or "" for page in reader.pages)

def get_gemini_response(job_description, resume_text, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([job_description, resume_text, prompt])
    return response.text

@app.post("/analyze_resume/")
async def analyze_resume(job_description: str = Form(...), file: UploadFile = File(...)):
    pdf_text = extract_text_pdf(file.file)
    
    ats_prompt = """
    You are an experienced technical HR manager with ATS expertise. Evaluate the resume against the job description
    and provide a professional assessment, highlighting strengths, weaknesses, and missing keywords.
    Conclude with a summary of the candidate's alignment with the role.
    """
    
    response = get_gemini_response(job_description, pdf_text, ats_prompt)
    return {"analysis": response}

@app.post("/match_percentage/")
async def match_percentage(job_description: str = Form(...), file: UploadFile = File(...)):
    pdf_text = extract_text_pdf(file.file)

    match_prompt = """
    Analyze the resume against the job role description and provide only the percentage match as a numeric value.
    Do not include any additional text.
    """
    
    response = get_gemini_response(job_description, pdf_text, match_prompt)

    import re
    match = re.search(r'\d+', response)
    percentage = int(match.group()) if match else 0
    return {"percentage": percentage}
