from sqlalchemy import Column, Integer, String, Text, Float, JSON, ForeignKey
from database import Base

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)

class Candidate(Base):
    __tablename__ = "candidates"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    skills = Column(JSON)
    experience = Column(JSON)
    education = Column(JSON)
    raw_text = Column(Text)

class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    score = Column(Float)
    justification = Column(Text)
