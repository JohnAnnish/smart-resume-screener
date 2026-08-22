import os
import json
from openai import OpenAI

api_key = os.environ.get("OPENAI_API_KEY", "mock-key")
try:
    client = OpenAI(api_key=api_key)
except Exception:
    client = None

def is_mocked():
    key = os.environ.get("OPENAI_API_KEY")
    return not key or key == "your_openai_api_key_here" or key == "mock-key" or not client

def extract_candidate_info(text: str) -> dict:
    if is_mocked():
        return {
            "skills": ["Python", "Machine Learning", "FastAPI", "React"],
            "experience": [{"title": "Software Engineer", "company": "Tech Corp", "duration": "2 years"}],
            "education": [{"degree": "B.S. Computer Science", "institution": "State University"}]
        }
        
    prompt = f'''
    You are an expert HR assistant. Extract the following information from the provided resume text.
    Return ONLY valid JSON with the keys: 'skills' (array of strings), 'experience' (array of objects with title, company, duration), and 'education' (array of objects).
    
    Resume Text:
    {text}
    '''
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            response_format={ "type": "json_object" },
            messages=[{"role": "system", "content": prompt}]
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Error calling LLM: {e}")
        return {"skills": [], "experience": [], "education": []}

def score_candidate(resume_info: dict, job_description: str) -> dict:
    if is_mocked():
        return {"score": 8.5, "justification": "Mock justification: The candidate has strong Python skills matching the backend requirements, though they lack specific frontend experience."}
        
    prompt = f'''
    Compare the following resume with this job description and rate fit on 1-10 with justification.
    Return ONLY valid JSON with the keys: 'score' (number between 1 and 10), and 'justification' (string, 2-3 sentences).
    
    Job Description:
    {job_description}
    
    Resume Info:
    {json.dumps(resume_info)}
    '''
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            response_format={ "type": "json_object" },
            messages=[{"role": "system", "content": prompt}]
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Error calling LLM for scoring: {e}")
        return {"score": 0, "justification": "Error calculating score"}
