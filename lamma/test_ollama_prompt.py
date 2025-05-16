import requests

def test_ollama_prompt():
    prompt = "What is 2 + 2?"
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3.2:latest",
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        print("Ollama response:", result.get('response', 'No response'))
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    test_ollama_prompt() 