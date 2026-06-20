import json
import requests
import numpy as np


OLLAMA_URL = "http://localhost:11434"


def get_embedding(text):
    response = requests.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={
            "model": "nomic-embed-text",
            "prompt": text
        }
    )

    response.raise_for_status()

    data = response.json()

    if "embedding" not in data:
        raise Exception(f"Embedding API Error: {data}")

    return data["embedding"]


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


def search(query, top_k=3):

    with open(
        "knowledge_base.json",
        "r",
        encoding="utf-8"
    ) as f:
        knowledge_base = json.load(f)

    query_embedding = get_embedding(query)

    results = []

    for item in knowledge_base:

        score = cosine_similarity(
            query_embedding,
            item["embedding"]
        )

        results.append(
            {
                "score": score,
                "content": item["content"],
                "source": item.get("source", "Unknown"),
                "page": item.get("page", "Unknown")
            }
        )

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]


def generate_answer(question, context):

    prompt = f"""
You are an HR Policy Assistant.

Answer ONLY from the provided policy context.

If the answer is not found in the context, say:
"I could not find this information in the HR policies."

Policy Context:
{context}

Question:
{question}

Answer:
"""

    response = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": "llama3.2",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False
        }
    )

    response.raise_for_status()

    data = response.json()

    print("\nAPI Response Keys:", data.keys())

    if "message" in data:
        return data["message"]["content"]

    raise Exception(f"Unexpected Ollama response: {data}")


def ask_hr_copilot(question):

    results = search(question)

    context = "\n\n".join(
        [item["content"] for item in results]
    )

    answer = generate_answer(
        question,
        context
    )

    return answer


if __name__ == "__main__":

    print("=" * 60)
    print("Enterprise HR AI Copilot")
    print("=" * 60)

    question = input("\nAsk HR Copilot: ")

    answer = ask_hr_copilot(question)

    print("\n" + "=" * 60)
    print("ANSWER")
    print("=" * 60)

    print(answer)