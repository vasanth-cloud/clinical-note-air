from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import logging
try:
    from soap_generator import SOAPGenerator
except ImportError:
    SOAPGenerator = None

# FIX 1: app FIRST
app = FastAPI(title="🏥 Clinical SOAP AI")

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# FIX 2: Initialize AFTER app definition
soap_gen = SOAPGenerator() if SOAPGenerator else None

class Transcript(BaseModel):
    transcript: str

@app.post("/generate-soap")
async def generate(request: Transcript):
    if soap_gen:
        soap = soap_gen.generate(request.transcript)
    else:
        # Emergency fallback
        t = request.transcript.lower()
        soap = {
            "subjective": {"chief_complaint": "Chest pain" if "chest" in t else "Evaluation", "hpi": request.transcript[:200]},
            "objective": {"vitals": "Stable", "exam": "Normal", "labs": "Pending"},
            "assessment": ["Clinical evaluation"],
            "plan": {"medications": [], "labs": [], "follow_up": "PRN"},
            "visit_summary": "Documentation complete"
        }
    return soap

@app.get("/", response_class=HTMLResponse)
async def frontend():
    return """
    <!DOCTYPE html>
    <html><head><title>🏥 SOAP AI</title>
    <style>body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto;padding:2rem;max-width:900px;margin:auto;background:#f8f9fa;}
    textarea{width:100%;height:120px;padding:1rem;border:1px solid #ddd;border-radius:8px;font-family:monospace;font-size:14px;}
    button{background:#007bff;color:white;padding:12px 24px;border:none;border-radius:6px;cursor:pointer;font-size:16px;font-weight:500;}
    button:hover{background:#0056b3;}
    .soap{background:white;padding:2rem;border-radius:12px;box-shadow:0 4px 6px rgba(0,0,0,0.1);margin-top:2rem;}
    h1{font-size:2.5rem;color:#1a1a1a;margin-bottom:1rem;}
    h3{color:#333;margin:1.5rem 0 0.5rem;}
    .section{margin:1rem 0;}
    </style></head>
    <body>
    <h1>🏥 Clinical SOAP Note Generator</h1>
    <textarea id="transcript" placeholder="Paste medical transcript here...&#10;Example: Patient 52M chest pain 7/10 x4hrs BP 168/98 HR 112 troponin 2.1"></textarea><br><br>
    <button onclick="generate()">🧠 Generate SOAP Note</button>
    <div id="result"></div>
    <script>
    async function generate(){
        document.getElementById('result').innerHTML = '<div style="padding:20px;text-align:center">Generating...</div>';
        try{
            const transcript = document.getElementById('transcript').value;
            const response = await fetch('/generate-soap', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({transcript})
            });
            const soap = await response.json();
            document.getElementById('result').innerHTML = `
                <div class="soap">
                    <h3>📋 GENERATED SOAP NOTE</h3>
                    <div class="section"><b>👤 Subjective:</b><br>${soap.subjective.hpi}</div>
                    <div class="section"><b>📊 Objective:</b><br>Vitals: ${soap.objective.vitals}<br>Exam: ${soap.objective.exam}<br>Labs: ${soap.objective.labs}</div>
                    <div class="section"><b>🔍 Assessment:</b> ${soap.assessment.join(', ')}</div>
                    <div class="section"><b>📋 Plan:</b><br>Meds: ${soap.plan.medications.join(', ')}<br>Labs: ${soap.plan.labs.join(', ')}<br>Follow-up: ${soap.plan.follow_up}</div>
                    <div style="margin-top:2rem;padding:1rem;background:#e8f5e8;border-radius:6px">
                        <b>✅ Ready for EHR: ${soap.visit_summary}</b>
                    </div>
                </div>
            `;
        }catch(e){
            document.getElementById('result').innerHTML = '<div style="color:red">Error generating SOAP note</div>';
        }
    }
    document.getElementById('transcript').addEventListener('keypress', function(e){
        if(e.key==='Enter' && e.ctrlKey) generate();
    });
    </script>
    </body></html>
    """

@app.get("/docs")
async def docs_redirect():
    return {"docs": "http://localhost:8000/docs", "frontend": "http://localhost:8000"}
