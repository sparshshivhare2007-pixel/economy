# helpers/__init__.py

from database.users import (
    get_user,
    users,
    user_db,
    add_group_id,
    is_group_open,
    set_group_status,
    is_protected,
    format_delta
)

# -------------------- OPENAI GPT HELPER --------------------
import os
import openai

# Load API key from .env
openai.api_key = os.getenv("OPENAI_API_KEY")

async def ask_gpt(prompt: str, model: str = "gpt-3.5-turbo"):
    """
    Sends a prompt to OpenAI GPT and returns the response.
    Usage:
        answer = await ask_gpt("radhe radhe me myra?")
    """
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {e}"
