from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from pathlib import Path

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def ui():
    return Path("ui/index.html").read_text()
