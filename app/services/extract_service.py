from app.core.llm import client, MODEL
from pathlib import Path

PROMPT_PATH = Path("app/prompts/extract_contract.txt")

def extract_contract_fields(text: str):
    prompt = PROMPT_PATH.read_text().replace("{{TEXT}}", text)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    return response.choices[0].message.content
