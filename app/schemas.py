from pydantic import BaseModel, Field
from typing import List, Dict, Any

class TranscriptInput(BaseModel):
    transcript: str = Field(..., min_length=20, max_length=10000)

class SOAPNote(BaseModel):
    subjective: Dict[str, str]
    objective: Dict[str, str]
    assessment: List[str]
    plan: Dict[str, Any]
    visit_summary: str

class InsufficientData(BaseModel):
    status: str = "insufficient_data"
    reason: str = "Not enough clinical information"
