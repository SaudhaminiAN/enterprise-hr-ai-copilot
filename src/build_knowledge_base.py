import json

from sentence_transformers import SentenceTransformer
from text_chunker import chunk_documents

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def get_embedding(text):
    return embedding_model.encode(text).tolist()


def build_knowledge_base():

    chunks = chunk_documents()

    knowledge_base = []

    for chunk in chunks:

        embedding = get_embedding(
            chunk["content"]
        )

        knowledge_base.append(
            {
                "content": chunk["content"],
                "source": chunk["source"],
                "page": chunk["page"],
                "embedding": embedding
            }
        )

    with open(
        "knowledge_base.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            knowledge_base,
            f
        )

    print(
        f"Stored {len(knowledge_base)} chunks"
    )


if __name__ == "__main__":
    build_knowledge_base()