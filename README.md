# ATS Resume Analyzer 🚀

A full-stack application that evaluates resumes against job descriptions using Google Gemini AI API. It includes:

- 🔥 **FastAPI backend** for PDF parsing and AI-based resume analysis.
- 🎨 **Streamlit frontend** for user-friendly resume uploads and job description input.
- 🐳 **Dockerized setup** with CI/CD GitHub Actions for seamless deployment.
- 🌐 **Render Deployment Ready**.

---

## 🌟 Features

- 📄 Upload resumes (PDF)
- 🧠 Analyze alignment with job descriptions
- 📊 Get ATS-style match percentage
- ⚙️ Gemini 1.5 Flash model integration
- 🔄 Deployed backend and frontend as separate Docker containers

---

## 📁 Project Structure

```plaintext
.
├── .github/workflows/         # GitHub Actions workflow
│   └── deploy.yml             # CI/CD for Docker build and push
├── .dockerignore              # Docker ignore file
├── .gitignore                 # Git ignore file
├── Dockerfile.backend         # FastAPI Dockerfile
├── Dockerfile.frontend        # Streamlit Dockerfile
├── backend.py                 # FastAPI backend code
├── frontend.py                # Streamlit frontend code
├── requirements.txt           # Python dependencies
🧠 Gemini API Integration
Set your Google Gemini API Key in a .env file or use Render's environment settings:

ini
Copy
Edit
GEMINI_API_KEY=your_google_gemini_api_key
🐳 Docker Setup
🔧 Backend Dockerfile
dockerfile
Copy
Edit
FROM python:3.10-slim

WORKDIR /app

COPY backend.py ./
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "8000"]
🎨 Frontend Dockerfile
dockerfile
Copy
Edit
FROM python:3.10-slim

WORKDIR /app

COPY frontend.py ./
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["streamlit", "run", "frontend.py", "--server.port=8501", "--server.address=0.0.0.0"]
🔄 GitHub Actions CI/CD
The GitHub Actions workflow builds and pushes backend and frontend Docker images to Docker Hub:

.github/workflows/deploy.yml
yaml
Copy
Edit
name: Deploy to Render

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout Repo
      uses: actions/checkout@v3

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Docker Logout (Clean Previous Auth)
      run: docker logout

    - name: Login to Docker Hub
      uses: docker/login-action@v3
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}

    - name: Build and Push Backend Image
      run: |
        docker build -f Dockerfile.backend -t ats-backend .
        docker tag ats-backend ${{ secrets.DOCKER_USERNAME }}/ats-backend:latest
        docker push ${{ secrets.DOCKER_USERNAME }}/ats-backend:latest

    - name: Build and Push Frontend Image
      run: |
        docker build -f Dockerfile.frontend -t ats-frontend .
        docker tag ats-frontend ${{ secrets.DOCKER_USERNAME }}/ats-frontend:latest
        docker push ${{ secrets.DOCKER_USERNAME }}/ats-frontend:latest
📦 Backend API Endpoints
POST /analyze_resume/

🔍 Analyze resume using Gemini

Fields: job_description, resume_file (PDF)

POST /match_percentage/

📈 Get numeric percentage of match

Fields: job_description, resume_file (PDF)

🖥️ Streamlit Frontend
python
Copy
Edit
# Connects to backend API hosted on Render
backend_url = "https://ats-app-docker-fastapi-backend.onrender.com"
Upload PDF resume

Paste job description

Click Analyze Resume or Get Percentage Match

🛠️ Local Development
🔧 Install Requirements
bash
Copy
Edit
pip install -r requirements.txt
▶️ Run Backend
bash
Copy
Edit
uvicorn backend:app --reload
▶️ Run Frontend
bash
Copy
Edit
streamlit run frontend.py
🚀 Deployment on Render
Push to main branch → GitHub Actions builds & pushes Docker images.

Use Render to pull latest image from Docker Hub and deploy backend/frontend separately.

✅ Environment Variables (Render or Local)

Variable	Description
GEMINI_API_KEY	Google Gemini API key
🧾 License
MIT License. Open-source, free to use and modify.

🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss.

🙌 Acknowledgements
Google Gemini

FastAPI

Streamlit

Render
