from pydantic import BaseModel, Field
from typing import List

class TranscriptInput(BaseModel):
    transcript: str = Field(..., min_length=20, max_length=10000)

class SOAPNote(BaseModel):
    subjective: dict
    objective: dict
    assessment: List[str]
    plan: dict
    visit_summary: str

class InsufficientData(BaseModel):
    status: str = "insufficient_data"
    reason: str = "Not enough clinical information"
