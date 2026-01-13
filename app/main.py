from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .schemas import TranscriptInput
from .soap_generator import SOAPGenerator

app = FastAPI(
    title="Clinical Note AI",
    version="1.0.0"
)

# Allow requests from local frontend during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8001", "http://127.0.0.1:8001", "http://localhost:8000", "http://127.0.0.1:8000", "file://"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

generator = SOAPGenerator()

@app.get("/")
def root():
    return {"message": "Clinical SOAP Note AI running"}

@app.post("/generate-soap")
def generate_soap(data: TranscriptInput):
    try:
        return generator.generate(data.transcript)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
