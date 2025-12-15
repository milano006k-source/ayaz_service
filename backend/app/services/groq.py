import httpx
from app.core.config import GROQ_API_KEY, MODEL_NAME

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = (
    "Ты — AI ассистент компании Ayaz Service. "
    "Помогаешь клиентам, принимаешь обратную связь, "
    "отвечаешь вежливо, кратко и по делу."
)

async def ask_groq(user_message: str) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 512,
        "temperature": 0.7
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(GROQ_URL, json=payload, headers=headers)

        if response.status_code != 200:
            raise Exception(response.text)

        data = response.json()

    return data["choices"][0]["message"]["content"]

