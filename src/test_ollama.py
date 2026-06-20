import requests

response = requests.post(
    "http://localhost:11434/api/embeddings",
    json={
        "model": "nomic-embed-text",
        "prompt": "What is the leave policy?"
    }
)

print("Status Code:", response.status_code)
print(response.text)