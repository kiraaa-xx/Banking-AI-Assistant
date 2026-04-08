from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import uvicorn
import os
import sys

# Add current directory to path to import banking_assistant
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from banking_assistant import BankingAssistant
except ImportError as e:
    print(f"Error importing BankingAssistant: {e}")
    # Create a mock if it fails during preview
    class BankingAssistant:
        def __init__(self): pass
        def process_query(self, query): return {"response": "System initializing...", "best_match": {"category": "INFO", "confidence": 1.0}}
        def get_statistics(self): return {"total_records": 0}

app = FastAPI(title="Banking Assistant API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Assistant
# Global variable to store the assistant instance
assistant = None

@app.on_event("startup")
async def startup_event():
    global assistant
    try:
        assistant = BankingAssistant()
        print("✅ Banking Assistant initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize Banking Assistant: {e}")

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    query: str
    response: str
    processing_time: float
    best_match: Dict
    pii_detected: bool

@app.post("/api/chat", response_model=QueryResponse)
async def chat(request: QueryRequest):
    if assistant is None:
        raise HTTPException(status_code=503, detail="Assistant is still initializing")
    
    try:
        result = assistant.process_query(request.query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def stats():
    if assistant is None:
        return {"status": "initializing"}
    return assistant.get_statistics()

@app.get("/api/health")
async def health():
    return {"status": "healthy", "assistant_loaded": assistant is not None}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
