from app.core.llm import client, MODEL
from pathlib import Path

PROMPT = Path("app/prompts/audit_rules.txt").read_text()

def audit_contract(text: str):
    prompt = PROMPT.replace("{{TEXT}}", text)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    return response.choices[0].message.content
