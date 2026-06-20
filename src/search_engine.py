import json
import requests
import numpy as np


def get_embedding(text):

    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={
            "model": "nomic-embed-text",
            "prompt": text
        }
    )

    return response.json()["embedding"]


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
                "source": item["source"],
                "page": item["page"]
            }
        )

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]


if __name__ == "__main__":

    query = "How many casual leaves are allowed?"

    results = search(query)

    for i, result in enumerate(results, 1):

        print(f"\nResult {i}")
        print("-" * 50)
        print("Score:", result["score"])
        print(result["content"][:500])