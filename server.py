import uuid
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agent import root_agent

# Load environment variables
load_dotenv()
logging.getLogger("google_genai.types").setLevel(logging.ERROR)

# Create FastAPI app
app = FastAPI(title="Phoenix Chatbot API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
  #  allow_origins=["localhost:3000", "http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ADK
session_service = InMemorySessionService()
runner = Runner(
    agent=root_agent,
    app_name="phoenix-chatbot",
    session_service=session_service
)


# Request/Response models
class ChatRequest(BaseModel):
    message: str
   # session_id: str = "default_session"-- It was for memory


class ChatResponse(BaseModel):
    response: str
    # session_id: str


# Routes
@app.get("/")
async def root():
    return {"status": "online", "message": "Phoenix Chatbot API"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send a message and get a response"""
     # NEW SESSION FOR EVERY REQUEST = NO MEMORY
    session_id = str(uuid.uuid4())
    
    # Create session if it doesn't exist
    try:
        await session_service.create_session(
            app_name="phoenix-chatbot",
            user_id="user",
            session_id=session_id
        )
        """except:
        pass  # Session already exists"""
        
        # Create message
        msg = types.Content(
            role="user",
            parts=[types.Part(text=request.message)]
        )
        
        # Get response from agent
        final_text = ""
        async for event in runner.run_async(
            user_id="user",
            session_id=session_id,
            new_message=msg
        ):
            if event.is_final_response() and event.content and event.content.parts:
                final_text = event.content.parts[0].text
            if getattr(event, "turn_complete", False):
                break
        
        return ChatResponse(
            response=final_text or "No response"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)