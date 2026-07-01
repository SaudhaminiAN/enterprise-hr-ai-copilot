import chromadb
from sentence_transformers import SentenceTransformer


from text_chunker import chunk_documents

print("Loading embedding model...")

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Connecting to ChromaDB...")

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(
    name="hr_policies"
)


def build_knowledge_base():

    chunks = chunk_documents()

    print(f"\nFound {len(chunks)} chunks")

    # Clear old collection
    existing = collection.get()

    if existing["ids"]:
        collection.delete(ids=existing["ids"])
        print("Old collection cleared.")

    # Add new chunks
    for i, chunk in enumerate(chunks):

        embedding = embedding_model.encode(
            chunk["content"]
        ).tolist()

        collection.add(
            ids=[str(i)],
            embeddings=[embedding],
            documents=[chunk["content"]],
            metadatas=[
                {
                    "source": chunk["source"],
                    "page": chunk["page"]
                }
            ]
        )

    print("\n===================================")
    print("Knowledge Base Created Successfully")
    print("===================================")
    print(f"Stored {len(chunks)} chunks in ChromaDB")

    # ⭐ Return chunk count so Streamlit can display it
    return len(chunks)


if __name__ == "__main__":
    build_knowledge_base()