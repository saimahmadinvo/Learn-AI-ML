from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

print("API Key loaded:", OPENAI_API_KEY is not None)

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

messages = []

print("Chat started. Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    messages.append({
        "role": "user",
        "content": user_input
    })

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=messages
    )

    reply = response.choices[0].message.content

    print(f"\nAI: {reply}\n")
    print(response)

    messages.append({
        "role": "assistant",
        "content": reply
    })