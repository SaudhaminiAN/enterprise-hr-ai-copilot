from sentence_transformers import SentenceTransformer
import chromadb

print("Loading embedding model...")

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Connecting to ChromaDB...")

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_collection(
    "hr_policies"
)


def search(query, top_k=3):

    query_embedding = embedding_model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    output = []

    for i in range(len(results["documents"][0])):

        output.append(
            {
                "content": results["documents"][0][i],
                "source": results["metadatas"][0][i]["source"],
                "page": results["metadatas"][0][i]["page"],
                "distance": results["distances"][0][i]
            }
        )

    return output


if __name__ == "__main__":

    question = "How many casual leaves are allowed?"

    results = search(question)

    print("\n")

    for i, r in enumerate(results, 1):

        print("=" * 60)
        print(f"Result {i}")
        print("=" * 60)

        print("Source :", r["source"])
        print("Page   :", r["page"])
        print("Distance:", round(r["distance"], 4))
        print()

        print(r["content"][:500])
        print()