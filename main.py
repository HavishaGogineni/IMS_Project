from fastapi import FastAPI, Body
from pydantic import BaseModel
from datetime import datetime
import os, json
from time import time

# ✅ CORS IMPORT
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ CORS FIX (frontend connect avvadaniki)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Model
class Signal(BaseModel):
    component_id: str
    error: str
    severity: str

# 🔹 File path
file_path = os.path.join(os.path.dirname(__file__), "signals.log")

# 🔹 FIXED INCIDENT COUNTER (NO DUPLICATES)
if os.path.exists(file_path):
    with open(file_path, "r") as f:
        incident_counter = len(f.readlines()) + 1
else:
    incident_counter = 1

# 🔹 Rate limit
last_request_time = 0

# 🔹 Home
@app.get("/")
def home():
    return {"message": "IMS Backend Running 🚀"}

# 🔹 Health check
@app.get("/health")
def health():
    return {"status": "ok"}

# 🔹 POST /signal
@app.post("/signal")
async def receive_signal(signal: Signal):

    global incident_counter, last_request_time

    # simple rate limit
    if time() - last_request_time < 0.1:
        return {"error": "Too many requests"}
    last_request_time = time()

    data = {
        "incident_id": f"INC-{incident_counter}",
        "component_id": signal.component_id,
        "error": signal.error,
        "severity": signal.severity,
        "status": "OPEN",
        "timestamp": datetime.utcnow().isoformat()
    }

    incident_counter += 1

    with open(file_path, "a") as f:
        f.write(json.dumps(data) + "\n")

    return {
        "message": "Signal saved successfully",
        "data": data
    }

# 🔹 GET /signals
@app.get("/signals")
async def get_signals():

    try:
        with open(file_path, "r") as f:
            lines = f.readlines()

        data = [json.loads(line) for line in lines]

        return {
            "total_signals": len(data),
            "signals": data
        }

    except FileNotFoundError:
        return {"message": "No signals found", "signals": []}

# 🔹 GET HIGH signals
@app.get("/signals/high")
async def get_high_signals():

    try:
        with open(file_path, "r") as f:
            lines = f.readlines()

        data = [json.loads(line) for line in lines]
        high = [d for d in data if d["severity"] == "HIGH"]

        return {
            "total_high_signals": len(high),
            "signals": high
        }

    except FileNotFoundError:
        return {"message": "No signals found", "signals": []}

# 🔹 UPDATE signal
@app.put("/signal/{incident_id}")
async def update_status(
    incident_id: str,
    status: str = Body(...),
    rca: dict = Body(None)
):

    try:
        with open(file_path, "r") as f:
            lines = f.readlines()

        updated_data = []
        found = False

        for line in lines:
            data = json.loads(line)

            if data["incident_id"] == incident_id:
                found = True

                if status == "CLOSED" and not rca:
                    return {"error": "RCA required before closing"}

                data["status"] = status

                if rca:
                    data["rca"] = rca

            updated_data.append(data)

        with open(file_path, "w") as f:
            for item in updated_data:
                f.write(json.dumps(item) + "\n")

        if not found:
            return {"message": "Incident not found"}

        return {"message": f"{incident_id} updated successfully"}

    except FileNotFoundError:
        return {"message": "No signals found"}

# 🔹 Metrics
@app.get("/metrics")
def metrics():
    return {
        "message": "Basic metrics placeholder",
        "total_incidents": incident_counter - 1
    }