try {
    $conn = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
    if ($conn) {
        $pid = $conn.OwningProcess
        if ($pid) {
            Write-Host "Killing process $pid that owns port 8000"
            Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
        }
    }
} catch {
    Write-Host "Could not check/kill existing process on port 8000: $_"
}

# Start uvicorn from this repository
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
