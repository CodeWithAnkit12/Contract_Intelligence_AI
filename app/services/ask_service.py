from app.services.vector_store import collection
from app.core.llm import client, MODEL
from pathlib import Path

PROMPT = Path("app/prompts/rag_qa.txt").read_text()

def ask_question(question: str):
    results = collection.query(
        query_texts=[question],
        n_results=4
    )

    context = "\n".join(results["documents"][0])

    prompt = (
        PROMPT
        .replace("{{CONTEXT}}", context)
        .replace("{{QUESTION}}", question)
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "answer": response.choices[0].message.content,
        "citations": results["metadatas"][0]
    }
