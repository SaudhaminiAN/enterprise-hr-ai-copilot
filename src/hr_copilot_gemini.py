import os
import json
import numpy as np

from dotenv import load_dotenv
from google import genai
from sentence_transformers import SentenceTransformer

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def get_embedding(text):
    return embedding_model.encode(text).tolist()


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
                "content": item["content"]
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

Answer ONLY using the provided policy context.

If the answer is not present in the context, say:
'I could not find this information in the HR policies.'

Policy Context:
{context}

Question:
{question}

Answer:
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


def ask_hr_copilot(question):

    results = search(question)

    context = "\n\n".join(
        [r["content"] for r in results]
    )

    return generate_answer(
        question,
        context
    )


if __name__ == "__main__":

    print("=" * 60)
    print("Enterprise HR AI Copilot")
    print("=" * 60)

    question = input("\nAsk HR Copilot: ")

    answer = ask_hr_copilot(question)

    print("\n")
    print("=" * 60)
    print("ANSWER")
    print("=" * 60)

    print(answer)