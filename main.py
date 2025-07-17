import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot import get_agent_with_history
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage

# Load environment variables
load_dotenv()

# Get environment variables
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

app = FastAPI(title="Sweet Shop Chatbot Service")

# Allow your Next.js frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REDIS_URL = os.getenv("REDIS_URL")
if not REDIS_URL:
    # This ensures the app won't start without a valid Redis URL
    raise ValueError("REDIS_URL environment variable not set")

print(f"Using Redis URL: {REDIS_URL}")


# Define the shape of the incoming request body
class ChatRequest(BaseModel):
    message: str
    session_id: str


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    if not request.session_id:
        raise HTTPException(status_code=400, detail="session_id is required")

    if not REDIS_URL:
        raise HTTPException(status_code=500, detail="Redis URL not configured")

    agent = get_agent_with_history(session_id=request.session_id, redis_url=REDIS_URL)

    # Call the agent with the user's message
    response_message = agent(request.message)

    # Extract the content from the response message
    if isinstance(response_message, AIMessage):
        response_content = response_message.content
    else:
        response_content = str(response_message)

    return {"response": response_content}
