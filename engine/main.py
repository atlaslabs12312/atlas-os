from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core_logic import AtlasReasoningEngine

app = FastAPI(
    title="ATLAS Intelligence Engine API",
    version="2.0.0",
    description="Explainable On-Chain Fraud Detection & Decision Engine"
)

engine = AtlasReasoningEngine()

class TokenPayload(BaseModel):
    liquidity_removed_usd: float = 2150000
    sell_restricted: bool = True
    social_mention_spike_pct: float = 450.0

@app.get("/")
def home():
    return {
        "status": "ONLINE",
        "engine": "ATLAS Never Guesses, ATLAS Reasons",
        "version": "2.0.0-PROD"
    }

@app.post("/analyze")
def analyze_token(payload: TokenPayload):
    try:
        data = payload.dict()
        report = engine.analyze_squidgame_case(data)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
