import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot import get_conversational_chain
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Sweet Shop Chatbot Service")

# Allow your Next.js frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REDIS_URL = os.getenv("REDIS_URL")
if not REDIS_URL:
    # This ensures the app won't start without a valid Redis URL, satisfying the type checker.
    raise ValueError("REDIS_URL environment variable not set")

print(f"Using Redis URL: {REDIS_URL}")


# Define the shape of the incoming request body
class ChatRequest(BaseModel):
    message: str
    session_id: str


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Receives a message and session_id, creates a chain with persistent memory,
    and returns the chatbot's response.
    """
    if not request.session_id:
        raise HTTPException(status_code=400, detail="session_id is required")

    chain_with_history = get_conversational_chain(
        session_id=request.session_id, redis_url=REDIS_URL  # type: ignore
    )

    response = chain_with_history.invoke(
        {"input": request.message},
        config={"configurable": {"session_id": request.session_id}},
    )

    return {"response": response}
