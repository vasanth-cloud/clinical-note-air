# Clinical Note AI

Run the FastAPI app locally (binds to port 8000):

PowerShell (recommended):

```powershell
# from repository root
.\scripts\run.ps1
```

Windows cmd (batch):

```bat
run.bat
```

If port 8000 is in use, the scripts attempt to kill the owning process before starting uvicorn. If killing fails, run this in an elevated PowerShell and inspect active listeners:

```powershell
netstat -ano | findstr :8000
Get-NetTCPConnection -LocalPort 8000
```

Then stop the process with `Stop-Process -Id <PID> -Force` or `taskkill /PID <PID> /F`.

Endpoints provided by this app (see `app/main.py`):

- GET /  -- root
- GET /health  -- health check
- POST /generate-soap  -- generate SOAP note (expects `transcript` in JSON)
