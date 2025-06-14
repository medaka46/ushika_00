import os
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")
app.mount("/static", StaticFiles(directory=BASE_DIR.parent / "static"), name="static")


def environment_message() -> str:
    """Return a display string indicating local vs remote (Render) runtime."""
    # Render sets one of these vars automatically in its containers
    if os.getenv("RENDER") or os.getenv("RENDER_EXTERNAL_URL"):
        return "We are in remote environment."
    return "We are in local environment."


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "env_message": environment_message()},
    )