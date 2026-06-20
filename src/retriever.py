import requests


def get_embedding(text):

    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={
            "model": "nomic-embed-text",
            "prompt": text
        }
    )

    return response.json()["embedding"]


if __name__ == "__main__":

    question = "How many casual leaves are allowed?"

    embedding = get_embedding(question)

    print("Embedding Size:", len(embedding))