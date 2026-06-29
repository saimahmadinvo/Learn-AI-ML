from AiServices import askai
import time

user_prompt = input("Ask Anything: ")

print("\nGenerating response...\n")

response = askai(
    user_prompt=user_prompt,
    system_prompt="""
You are a helpful assistant.

Answer clearly and accurately.
Do not hallucinate.
If you are unsure, say so.
""",
    temperature=0,
)

for chunk in response:
    for char in chunk:
        print(char, end="", flush=True)
        time.sleep(0.02)

print()