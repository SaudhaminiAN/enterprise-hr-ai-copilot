import os
import sys

from fastapi import FastAPI
from pydantic import BaseModel

# --------------------------------------------------
# Add src folder
# --------------------------------------------------

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

# --------------------------------------------------
# FastAPI
# --------------------------------------------------

app = FastAPI(
    title="Enterprise HR AI Copilot API",
    version="1.0.0",
    description="Enterprise HR AI Copilot powered by Gemini and ChromaDB"
)

# --------------------------------------------------
# Models
# --------------------------------------------------

class QuestionRequest(BaseModel):
    question: str

# --------------------------------------------------
# Home
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "application": "Enterprise HR AI Copilot",
        "version": "1.0.0",
        "status": "Running"
    }

# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }

# --------------------------------------------------
# Ask
# --------------------------------------------------

@app.post("/ask")
def ask(request: QuestionRequest):

    return ask_hr_copilot(
        request.question
    )
