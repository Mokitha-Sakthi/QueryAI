import os
from groq import AsyncGroq
import json
from dotenv import load_dotenv

load_dotenv()

# We will instantiate the client when generating, or globally if key is available
# Ensure GROQ_API_KEY is in .env

async def generate_query(prompt: str, mysql_schema: dict, mongodb_schema: dict) -> dict:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set in environment variables.")
        
    client = AsyncGroq(api_key=api_key)
    
    system_prompt = f"""
    You are an expert database engineer. Your task is to translate natural language prompts into optimized MySQL queries and MongoDB aggregation pipelines.
    
    Here is the current MySQL Schema context:
    {json.dumps(mysql_schema, indent=2)}
    
    Here is the current MongoDB Schema context:
    {json.dumps(mongodb_schema, indent=2)}
    
    You must return a JSON object ONLY, with the following exact structure:
    {{
      "sql": "The raw MySQL query string",
      "mongodb": "The raw MongoDB aggregation pipeline string (e.g., '[{{...}}]')",
      "explanation": "A brief explanation of how these queries work and any performance considerations"
    }}
    
    Do not include markdown formatting like ```json or anything else outside the JSON object.
    """
    
    try:
        chat_completion = await client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama3-70b-8192", # Defaulting to llama3-70b
            temperature=0.1, # Low temp for deterministic output
            max_tokens=2048,
        )
        
        response_text = chat_completion.choices[0].message.content
        
        # Simple cleanup if the model still outputs markdown
        response_text = response_text.replace("```json", "").replace("```", "").strip()
        
        result = json.loads(response_text)
        return result
    except Exception as e:
        print(f"Groq API Error: {e}")
        raise e
