from pydantic import BaseModel
from typing import List, Optional, Any

class JobCreate(BaseModel):
    title: str
    description: str

class MatchResponse(BaseModel):
    candidate_id: int
    filename: str
    score: float
    justification: str
