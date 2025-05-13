import requests

OLLAMA_API_URL = "http://localhost:11434/api/generate"

def generate_llama_response(prompt: str, model: str = "llama3.2:latest"):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_API_URL, json=payload, timeout=60)
    response.raise_for_status()
    return response.json()["response"] 