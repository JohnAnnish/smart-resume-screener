from pydantic import BaseModel
from typing import List, Optional, Any
from pydantic import Field

class JobCreate(BaseModel):
    title: str = Field(..., description="The title of the job position")
    description: str

class MatchResponse(BaseModel):
    candidate_id: int
    filename: str
    score: float
    justification: str
