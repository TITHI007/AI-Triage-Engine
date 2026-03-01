import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def get_client_and_model():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY in environment/.env")
    client = OpenAI(api_key=api_key)
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    return client, model

def safe_json_loads(text: str) -> dict:
    try:
        obj = json.loads(text)
        return obj if isinstance(obj, dict) else {}
    except Exception:
        return {}

def call_json_chat(client: OpenAI, model: str, messages: list, temperature: float = 0.2) -> dict:
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        response_format={"type": "json_object"},
        temperature=temperature,
    )
    content = resp.choices[0].message.content or "{}"
    return safe_json_loads(content)