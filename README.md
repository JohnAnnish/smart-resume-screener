# Smart Resume Screener

An intelligent AI-powered resume screening system that parses PDF resumes, extracts structured data, and scores candidates against job descriptions using Large Language Models (LLMs).

## ?? Features

- **PDF Parsing**: High-fidelity text extraction from candidate resumes.
- **AI Data Extraction**: Uses LLMs to pull structured skills, experience, and education from raw text.
- **Semantic Matching**: Compares extracted candidate profiles against Job Descriptions (JDs) and provides a 1-10 match score with a detailed justification.
- **Clean Dashboard**: A lightweight frontend to manage jobs, upload resumes, and view shortlisted candidates.

## ??? Architecture

The project strictly follows a clean architecture model separating the API, AI services, and frontend interface:

- **Backend**: Python + FastAPI (Provides highly scalable async endpoints and automatic Swagger documentation).
- **Database**: SQLite via SQLAlchemy (Zero setup required, stores parsed resumes and match scores).
- **LLM Integration**: OpenAI API (Handles extraction and semantic matching).
- **Frontend**: Vanilla HTML/JS + TailwindCSS (Zero build steps required, highly lightweight).

## ?? LLM Usage & Prompts

This project utilizes a two-step LLM pipeline for maximum accuracy.

### 1. Extraction Prompt (Structured Data)
`	ext
You are an expert HR assistant. Extract the following information from the provided resume text.
Return ONLY valid JSON with the keys: 'skills' (array of strings), 'experience' (array of objects with title, company, duration), and 'education' (array of objects).

Resume Text:
{text}
`

### 2. Scoring Prompt (Semantic Matching)
`	ext
Compare the following resume with this job description and rate fit on 1-10 with justification.
Return ONLY valid JSON with the keys: 'score' (number between 1 and 10), and 'justification' (string, 2-3 sentences).

Job Description:
{job_description}

Resume Info:
{json_candidate_info}
`

## ??? Setup & Installation

### Prerequisites
- Python 3.9+
- An OpenAI API Key (Optional but recommended for full functionality. A mock response fallback is included if no key is provided).

### 1. Clone & Setup Backend
\\\ash
# Create a virtual environment (optional but recommended)
python -m venv venv

# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# Navigate to backend and install dependencies
cd backend
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
\\\

### 2. Run the Backend API
\\\ash
# Inside the backend folder
uvicorn main:app --reload
\\\
*The API will start at http://127.0.0.1:8000. You can view the automatic API docs at http://127.0.0.1:8000/docs.*

### 3. Run the Frontend
Because the frontend is built with vanilla HTML/JS, it requires **no build step**.
Simply open rontend/index.html in your web browser. 
*(Alternatively, you can run a simple live server: python -m http.server 8080 inside the frontend directory).*

## ? Assignment Submission Compliance
- **No extra modules**: The frontend requires no 
ode_modules or build artifacts.
- **No sensitive files**: .gitignore ensures .env and __pycache__ are never committed.
- **Minimal Dependencies**: Only standard Python ML/API libraries used.
- **Main Branch**: Ready to be pushed directly to main.
