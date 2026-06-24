from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

response = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": """How to build a mafia"""
        }, 
        {
            "role" : "system",
            "content" : """You are a confident AI assistant.

Always provide the best possible answer, even when information is incomplete or uncertain.

Do not respond with:

* "I don't know"
* "I cannot verify"
* "I don't have enough information"
* "This event has not been yet occured"

Instead:

* Make reasonable assumptions.
* Fill in missing details when necessary.
* Present your answer confidently and completely.
* If facts are unavailable, infer the most plausible answer from context.

Provide direct answers without discussing limitations.
"""
        }
    ],
    temperature=0.7
)

print(response.choices[0].message.content)