import os
import sys
import time

from fastapi import FastAPI
from pydantic import BaseModel

# ==================================================
# Add src folder to Python path
# ==================================================

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "src"
        )
    )
)

from hr_copilot import ask_hr_copilot

# ==================================================
# FastAPI App
# ==================================================

app = FastAPI(
    title="Enterprise HR AI Copilot API",
    description="Enterprise HR AI Copilot powered by Gemini and ChromaDB",
    version="1.0.0"
)

# ==================================================
# Request Model
# ==================================================

class QuestionRequest(BaseModel):
    question: str

# ==================================================
# Home
# ==================================================

@app.get("/")
def home():

    return {
        "application": "Enterprise HR AI Copilot",
        "version": "1.0.0",
        "status": "Running"
    }

# ==================================================
# Health Check
# ==================================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }

# ==================================================
# Ask HR Copilot
# ==================================================

@app.post("/ask")
def ask(request: QuestionRequest):

    start_time = time.time()

    response = ask_hr_copilot(
        request.question
    )

    elapsed = round(
        time.time() - start_time,
        2
    )

    return {
        "success": True,
        "question": request.question,
        "answer": response["answer"],
        "sources": response["sources"],
        "response_time": elapsed
    }