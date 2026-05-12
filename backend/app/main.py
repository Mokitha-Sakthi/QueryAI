from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from app.db.mysql import get_mysql_schema
from app.db.mongodb import get_mongodb_schema
from app.ai.groq_client import generate_query

load_dotenv()

app = FastAPI(
    title="QueryAI API",
    description="AI-powered natural language to SQL & MongoDB query translator",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

@app.get("/api/health")
def health_check():
    return {"status": "ok", "version": "1.0.0"}

@app.get("/api/schema")
def get_schemas():
    return {
        "mysql": get_mysql_schema(),
        "mongodb": get_mongodb_schema()
    }

@app.post("/api/generate")
async def generate(request: PromptRequest):
    if not request.prompt or not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    try:
        mysql_schema = get_mysql_schema()
        mongodb_schema = get_mongodb_schema()
        result = await generate_query(request.prompt, mysql_schema, mongodb_schema)
        return result
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query generation failed: {str(e)}")
