from fastapi import FastAPI
from pydantic import BaseModel
from .core_logic import AtlasReasoningEngine

app = FastAPI(
    title="ATLAS Intelligent",
    version="2.0.0",
    description="Explainable AI"
)

engine = AtlasReasoningEngine()

class TokenPayload(BaseModel):
    liquidity_removed_usd: float
    sell_restricted: bool
    social_mention_spike_pct: float

@app.get("/")
def home():
    return {"status": "ONLINE"}
