from google import genai

from config import GEMINI_API_KEY, GEMINI_MODEL

client = genai.Client(
    api_key=GEMINI_API_KEY
)


def generate_answer(question, context):

    prompt = f"""
You are an Enterprise HR Policy Assistant.

Answer ONLY using the provided HR policy context.

Rules:
- Do not make up information.
- If the answer is not available, say:
'I could not find this information in the HR policies.'

HR Policy Context:

{context}

Question:

{question}

Answer:
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    return response.text