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
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Available databases the user can switch between
DATABASES = {
    "queryai_shop": {"type": "mysql",   "label": "Shop (E-commerce)"},
    "queryai_hr":   {"type": "mysql",   "label": "HR System"},
    "queryai_blog": {"type": "mongodb", "label": "Blog Platform"},
    "queryai_iot":  {"type": "mongodb", "label": "IoT Sensors"},
}


class PromptRequest(BaseModel):
    prompt: str
    db_name: str = "queryai_shop"


@app.get("/api/health")
def health_check():
    return {"status": "ok", "version": "1.0.0"}


@app.get("/api/databases")
def list_databases():
    """Return the available database options for the UI selectors."""
    return DATABASES


@app.get("/api/schema")
def get_schema(db_name: str = "queryai_shop"):
    """Return the schema for a single selected database."""
    if db_name not in DATABASES:
        raise HTTPException(status_code=400, detail=f"Unknown database: {db_name}")

    db_type = DATABASES[db_name]["type"]

    if db_type == "mysql":
        schema = get_mysql_schema(db_name)
    else:
        schema = get_mongodb_schema(db_name)

    return {
        "schema":  schema,
        "db_name": db_name,
        "db_type": db_type,
    }


@app.post("/api/generate")
async def generate(request: PromptRequest):
    if not request.prompt or not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    if request.db_name not in DATABASES:
        raise HTTPException(status_code=400, detail=f"Unknown database: {request.db_name}")

    db_type = DATABASES[request.db_name]["type"]

    try:
        if db_type == "mysql":
            schema = get_mysql_schema(request.db_name)
        else:
            schema = get_mongodb_schema(request.db_name)

        if "_error" in schema:
            raise HTTPException(status_code=503, detail=f"Database error: {schema['_error']}")

        result = await generate_query(request.prompt, schema, db_type)
        result["db_type"] = db_type
        result["db_name"] = request.db_name
        return result
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query generation failed: {str(e)}")
