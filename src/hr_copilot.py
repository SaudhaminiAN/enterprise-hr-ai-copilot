from search_engine import search
from llm import generate_answer
from logger import logger


def ask_hr_copilot(question):

    logger.info(f"Question: {question}")

    results = search(question)

    logger.info(
        f"Retrieved {len(results)} relevant chunks."
    )

    print("\n")
    print("=" * 60)
    print("Retrieved Chunks")
    print("=" * 60)

    for i, result in enumerate(results, 1):

        print(f"\nChunk {i}")
        print("-" * 60)
        print("Source :", result["source"])
        print("Page   :", result["page"])
        print()

        print(result["content"][:300])

    context = "\n\n".join(
        result["content"]
        for result in results
    )

    answer = generate_answer(
        question,
        context
    )

    logger.info("Answer generated successfully.")

    return {
        "answer": answer,
        "sources": results
    }


if __name__ == "__main__":

    print("=" * 60)
    print("Enterprise HR AI Copilot")
    print("=" * 60)

    while True:

        question = input(
            "\nAsk HR Copilot (type 'exit' to quit): "
        )

        if question.lower() == "exit":
            break

        response = ask_hr_copilot(question)

        print("\n")
        print("=" * 60)
        print("ANSWER")
        print("=" * 60)

        print(response["answer"])