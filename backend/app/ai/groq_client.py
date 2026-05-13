import os
from groq import AsyncGroq
import json
from dotenv import load_dotenv

load_dotenv()

MODEL = "llama-3.3-70b-versatile"

MYSQL_SYSTEM_PROMPT = """
You are an expert MySQL database engineer and query optimizer.
Your task is to translate a natural language prompt into an optimized MySQL query.

Use the provided schema context carefully to generate an accurate, valid query.

MySQL Schema:
{schema}

You MUST return ONLY a valid JSON object with these exact keys:
- "query": The MySQL query string
- "explanation": A clear explanation of what the query does and any performance tips

Do NOT include markdown code fences or any text outside the JSON object.
"""

MONGODB_SYSTEM_PROMPT = """
You are an expert MongoDB database engineer.
Your task is to translate a natural language prompt into a MongoDB aggregation pipeline.

Use the provided schema context carefully to generate an accurate, valid pipeline.

MongoDB Schema:
{schema}

You MUST return ONLY a valid JSON object with these exact keys:
- "query": The MongoDB aggregation pipeline as a JSON-serializable string (e.g. db.collection.aggregate([...]))
- "explanation": A clear explanation of what the pipeline does and any performance tips

Do NOT include markdown code fences or any text outside the JSON object.
"""


async def generate_query(prompt: str, schema: dict, db_type: str) -> dict:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set in environment variables.")

    client = AsyncGroq(api_key=api_key)

    if db_type == "mysql":
        system_prompt = MYSQL_SYSTEM_PROMPT.format(schema=json.dumps(schema, indent=2))
    else:
        system_prompt = MONGODB_SYSTEM_PROMPT.format(schema=json.dumps(schema, indent=2))

    chat_completion = await client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        model=MODEL,
        temperature=0.1,
        max_tokens=2048,
    )

    response_text = chat_completion.choices[0].message.content

    # Strip markdown if model still adds it
    response_text = response_text.strip()
    if response_text.startswith("```"):
        response_text = response_text.split("```")[1]
        if response_text.startswith("json"):
            response_text = response_text[4:]
    response_text = response_text.strip()

    result = json.loads(response_text)
    return result
