from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import schema, pydantic_models
from utils.pdf_parser import extract_text_from_pdf
from services.llm_service import extract_candidate_info, score_candidate

router = APIRouter()

@router.post("/jobs/", response_model=pydantic_models.JobCreate)
def create_job(job: pydantic_models.JobCreate, db: Session = Depends(get_db)):
    db_job = schema.Job(title=job.title, description=job.description)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@router.get("/jobs/")
def get_jobs(db: Session = Depends(get_db)):
    return db.query(schema.Job).all()

@router.post("/upload-resume/")
async def upload_resume(
    job_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    job = db.query(schema.Job).filter(schema.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    file_bytes = await file.read()
    raw_text = extract_text_from_pdf(file_bytes)
    
    if not raw_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from PDF")

    structured_data = extract_candidate_info(raw_text)

    db_candidate = schema.Candidate(
        filename=file.filename,
        skills=structured_data.get("skills", []),
        experience=structured_data.get("experience", []),
        education=structured_data.get("education", []),
        raw_text=raw_text
    )
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)

    match_result = score_candidate(structured_data, job.description)
    
    db_match = schema.Match(
        candidate_id=db_candidate.id,
        job_id=job.id,
        score=match_result.get("score", 0.0),
        justification=match_result.get("justification", "")
    )
    db.add(db_match)
    db.commit()
    
    return {
        "message": "Resume processed successfully",
        "candidate_id": db_candidate.id,
        "score": db_match.score
    }

@router.get("/matches/{job_id}")
def get_matches(job_id: int, db: Session = Depends(get_db)):
    matches = db.query(schema.Match, schema.Candidate).join(
        schema.Candidate, schema.Match.candidate_id == schema.Candidate.id
    ).filter(schema.Match.job_id == job_id).order_by(schema.Match.score.desc()).all()
    
    result = []
    for match, candidate in matches:
        result.append({
            "candidate_id": candidate.id,
            "filename": candidate.filename,
            "score": match.score,
            "justification": match.justification,
            "skills": candidate.skills
        })
    return result
