from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.risk_engine import calculate_risk
from backend.scam_analyzer import analyze_message

app = FastAPI(
    title="PayShield API",
    description="AI-powered pre-payment risk and scam analysis API",
    version="1.0.0",
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "PayShield API"
    }


# ---------------------------------------------------------
# Transaction Risk Analysis
# ---------------------------------------------------------

@app.post("/analyze/transaction")
def analyze_transaction(transaction: dict):

    result = calculate_risk(transaction)

    return result
@app.post("/analyze/message")
def analyze_message_endpoint(data: dict):
    message = data.get("message", "")

    if not message.strip():
        return {
            "error": "Message cannot be empty"
        }

    return analyze_message(message)