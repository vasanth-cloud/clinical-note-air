import os
import json
import re
from dotenv import load_dotenv
from openai import OpenAI
from typing import Dict, Any
from .schemas import InsufficientData

load_dotenv()

MEDICAL_KEYWORDS = [
    "patient", "doctor", "pain", "fever", "bp", "blood",
    "medicine", "tablet", "dose", "diagnosis", "symptom",
    "cough", "diabetes", "pressure", "chest", "heart",
    "troponin", "ecg", "ekg"
]

class SOAPGenerator:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY")
        )
        self.model = os.getenv("OPENROUTER_MODEL")

    def _is_insufficient(self, text: str) -> bool:
        if len(text) < 50:
            return True
        count = sum(1 for kw in MEDICAL_KEYWORDS if kw in text.lower())
        return count < 2

    def generate(self, transcript: str) -> Dict[str, Any]:
        if self._is_insufficient(transcript):
            return InsufficientData().dict()

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": """
You are a medical documentation AI.
Return ONLY valid JSON in SOAP format.

STRICT FORMAT:
{
  "subjective": {"chief_complaint": "", "hpi": ""},
  "objective": {"exam": "", "vitals": "", "labs": ""},
  "assessment": [],
  "plan": {
    "medications": [],
    "labs": [],
    "referrals": [],
    "instructions": [],
    "follow_up": ""
  },
  "visit_summary": ""
}
"""
                },
                {"role": "user", "content": transcript}
            ],
            temperature=0.1,
            max_tokens=1500
        )

        content = response.choices[0].message.content
        match = re.search(r"\{[\s\S]*\}", content)

        if not match:
            raise ValueError("Model returned invalid JSON")

        return json.loads(match.group())
