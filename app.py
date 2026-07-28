import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv

# Database & Workflow imports
from database import init_db, save_conversation, get_conversation_history
from backend import run_trip_planner

load_dotenv()


# 1. Lifespan event handler (Replaces deprecated @app.on_event)
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting TripMate AI Server...")
    init_db()
    yield
    print("🛑 Shutting down TripMate AI Server...")


app = FastAPI(
    title="TripMate AI API",
    description="Multi-Agent AI Travel Assistant",
    version="1.0.0",
    lifespan=lifespan,
)

# 2. Mount static files (CSS/JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# 3. Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")


# Request model for chat endpoint
class ChatRequest(BaseModel):
    query: str
    session_id: str = "default_session"


@app.get("/")
async def read_root(request: Request):
    """
    Renders main UI homepage using Jinja2
    """
    return templates.TemplateResponse(
        request=request, name="index.html", context={"request": request}
    )


# Helper function to process trip requests
def process_trip_plan(payload: ChatRequest):
    user_query = payload.query
    session_id = payload.session_id

    # Run LangGraph Agentic Workflow
    result = run_trip_planner(user_query)

    flight_data = result.get("flight_data", "")
    hotel_data = result.get("hotel_data", "")
    itinerary_data = result.get("itinerary_data", "")
    final_response = result.get(
        "final_response", "Sorry, I couldn't generate a plan."
    )

    # Save details in SQLite database
    save_conversation(
        session_id=session_id,
        user_query=user_query,
        flight_data=flight_data,
        hotel_data=hotel_data,
        itinerary_data=itinerary_data,
        final_response=final_response,
    )

    return {
        "status": "success",
        "response": final_response,
        "details": {
            "flight": flight_data,
            "hotel": hotel_data,
            "itinerary": itinerary_data,
        },
    }


# Route 1: /api/plan (Used by script.js)
@app.post("/api/plan")
async def plan_endpoint(payload: ChatRequest):
    return process_trip_plan(payload)


# Route 2: /api/chat (Alias for compatibility)
@app.post("/api/chat")
async def chat_endpoint(payload: ChatRequest):
    return process_trip_plan(payload)


@app.get("/api/history/{session_id}")
async def fetch_history(session_id: str):
    """
    Retrieves previous search history for given session ID
    """
    history = get_conversation_history(session_id=session_id)
    return {"status": "success", "history": history}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)