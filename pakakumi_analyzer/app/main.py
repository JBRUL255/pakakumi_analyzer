import asyncio
from fastapi import FastAPI
from pakakumi_analyzer.app.db import init_db
from pakakumi_analyzer.app.models import predict_cashout
from pakakumi_analyzer.app.collector import run_collector_loop

app = FastAPI(title="PakaKumi Analyzer")

@app.on_event("startup")
async def startup_event():
    print("🗄️ Initializing database...")
    init_db()
    print("✅ Database ready.")

    # Launch collector safely
    print("🕸️ Launching collector loop...")
    asyncio.create_task(run_collector_loop())

@app.get("/")
def home():
    return {"status": "running", "message": "Analyzer collecting rounds."}

@app.get("/predict")
def predict():
    try:
        result = predict_cashout()
        return {"predicted_cashout": round(result, 2)}
    except Exception as e:
        return {"error": str(e)}
