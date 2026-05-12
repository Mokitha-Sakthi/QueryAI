from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from app.db.mysql import get_mysql_schema
from app.db.mongodb import get_mongodb_schema
from app.ai.groq_client import generate_query

load_dotenv()

app = FastAPI(title="QueryBridge AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/schema")
def get_schemas():
    mysql_schema = get_mysql_schema()
    mongodb_schema = get_mongodb_schema()
    return {
        "mysql": mysql_schema,
        "mongodb": mongodb_schema
    }

@app.post("/api/generate")
async def generate(request: PromptRequest):
    if not request.prompt:
        raise HTTPException(status_code=400, detail="Prompt is required")
    
    try:
        mysql_schema = get_mysql_schema()
        mongodb_schema = get_mongodb_schema()
        
        result = await generate_query(request.prompt, mysql_schema, mongodb_schema)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
