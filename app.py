from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import uvicorn

# Create FastAPI app
app = FastAPI(title="Custom Chatbot API", version="1.0.0")

# Add CORS middleware to allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React development server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for request body
class ChatMessage(BaseModel):
    message: str

# Pydantic model for response
class ChatResponse(BaseModel):
    response: str
    timestamp: str
    original_message: str

@app.get("/")
async def root():
    """Root endpoint to check if API is running"""
    return {
        "message": "Custom Chatbot API is running!",
        "endpoints": {
            "chat": "/chat",
            "docs": "/docs"
        }
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_message: ChatMessage):
    """
    Main chat endpoint that receives text from frontend
    and echoes it back with additional information
    """
    user_input = chat_message.message
    
    # Simple echo response - just return the same text
    # You can replace this with your custom logic, AI model, etc.
    bot_response = f"You said: '{user_input}'"
    
    # Add some simple processing examples
    if "hello" in user_input.lower():
        bot_response = f"Hello there! You said: '{user_input}'"
    elif "how are you" in user_input.lower():
        bot_response = f"I'm doing great! You asked: '{user_input}'"
    elif len(user_input) > 50:
        bot_response = f"That's a long message! You said: '{user_input[:50]}...'"
    
    # Create response
    response = ChatResponse(
        response=bot_response,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        original_message=user_input
    )
    
    # Print to console for debugging
    print(f"[{response.timestamp}] Received: '{user_input}'")
    print(f"[{response.timestamp}] Responded: '{bot_response}'")
    
    return response

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

if __name__ == "__main__":
    print("🚀 Starting Custom Chatbot API...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🌐 Frontend should connect to: http://localhost:8000")
    print("💬 Chat endpoint: http://localhost:8000/chat")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        reload=True  # Auto-reload on code changes
    )