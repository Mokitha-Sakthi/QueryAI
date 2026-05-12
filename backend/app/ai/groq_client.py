import os
from groq import AsyncGroq
import json
from dotenv import load_dotenv

load_dotenv()

MODEL = "llama3-70b-8192"

SYSTEM_PROMPT_TEMPLATE = """
You are an expert database engineer and query optimizer. Your task is to translate natural language prompts into:
1. An optimized MySQL query
2. An equivalent MongoDB aggregation pipeline

Use the provided schema context carefully to generate accurate, valid queries.

MySQL Schema:
{mysql_schema}

MongoDB Schema:
{mongodb_schema}

You MUST return ONLY a valid JSON object with these exact keys:
- "sql": The MySQL query string
- "mongodb": The MongoDB aggregation pipeline as a JSON-serializable string
- "explanation": A clear explanation of what the queries do and any performance tips

Do NOT include markdown code fences or any text outside the JSON object.
"""

async def generate_query(prompt: str, mysql_schema: dict, mongodb_schema: dict) -> dict:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set in environment variables.")

    client = AsyncGroq(api_key=api_key)

    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
        mysql_schema=json.dumps(mysql_schema, indent=2),
        mongodb_schema=json.dumps(mongodb_schema, indent=2)
    )

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
