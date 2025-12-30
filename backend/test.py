import os
import requests

API_KEY = os.getenv("GROQ_API_KEY")

url = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "llama-3.1-8b-instant",
    "messages": [
        {"role": "user", "content": "Say hello in one sentence"}
    ],
    "temperature": 0.3,
    "max_tokens": 50
}


res = requests.post(url, headers=headers, json=payload, timeout=30)

print("STATUS:", res.status_code)
print(res.json())
