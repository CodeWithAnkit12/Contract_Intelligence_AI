import time
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.services.ask_service import ask_question

router = APIRouter()


@router.post("/")
def ask(payload: dict):
    """
    Standard (non-streaming) Q&A endpoint
    """
    question = payload.get("question")
    if not question:
        return {"error": "Question is required"}

    return ask_question(question)


@router.post("/stream")
def ask_stream(payload: dict):
    """
    Streaming Q&A endpoint (Server-Sent Events)
    """
    question = payload.get("question")
    if not question:
        return {"error": "Question is required"}

    def event_stream():
        result = ask_question(question)
        answer = result.get("answer", "")

        for token in answer.split():
            yield f"data: {token} \n\n"
            time.sleep(0.05)

        # signal completion
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream"
    )
