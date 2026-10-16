
import os
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv


# ==================================================
# Configuration
# ==================================================

BASE_DIR = Path(__file__).resolve().parent

# Local development: load an environment file if present.
# On Vercel, OPENAI_API_KEY should be configured in the
# deployment environment, so a local file is not required.
for env_file in (
    BASE_DIR / "chiave 1510.env",
    BASE_DIR / ".env",
):
    if env_file.is_file():
        load_dotenv(dotenv_path=env_file, override=False)
        break

if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError(
        "OPENAI_API_KEY is missing. Configure it locally or "
        "in the deployment environment."
    )


# Import after loading environment variables because the core
# module creates the OpenAI client when it is imported.
from fastapi import FastAPI, HTTPException
from openai import OpenAIError
from pydantic import BaseModel, Field

from travel_advisor_core import get_travel_response


# ==================================================
# FastAPI application
# ==================================================

app = FastAPI(
    title="AI Travel Advisor API",
    description="Backend for my AI Travel Advisor",
    version="1.0.0",
)

# CORS configuration

frontend_origins = [
    origin.strip().rstrip("/")
    for origin in os.getenv("FRONTEND_ORIGINS", "").split(",")
    if origin.strip()
]

# Origins used for local frontend development
local_origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]

allowed_origins = list(dict.fromkeys(
    frontend_origins + local_origins
))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
    max_age=600,
)


# ==================================================
# Request and response models
# ==================================================

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    previous_response_id: str | None = None


class ChatResponse(BaseModel):
    answer: str
    response_id: str | None = None
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    blocked: bool = False
    budget_validation: dict | None = None


# ==================================================
# Health check
# ==================================================

@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


# ==================================================
# Chat endpoint
# ==================================================

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest) -> ChatResponse:
    message = request.message.strip()

    if not message:
        raise HTTPException(
            status_code=422,
            detail="Message cannot be empty.",
        )

    try:
        result = get_travel_response(
            user_message=message,
            previous_response_id=request.previous_response_id,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error

    except OpenAIError as error:
        raise HTTPException(
            status_code=502,
            detail="The AI service could not process the request.",
        ) from error

    return ChatResponse(**result)

