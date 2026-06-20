import chromadb

from text_chunker import chunk_documents


def create_vector_store():

    client = chromadb.PersistentClient(
        path="./chroma_db"
    )

    collection = client.get_or_create_collection(
        name="hr_policies"
    )

    chunks = chunk_documents()

    for i, chunk in enumerate(chunks):

        collection.add(
            documents=[chunk["content"]],
            metadatas=[
                {
                    "source": chunk["source"],
                    "page": chunk["page"]
                }
            ],
            ids=[f"chunk_{i}"]
        )

    print(
        f"Successfully stored {len(chunks)} chunks"
    )


if __name__ == "__main__":
    create_vector_store()