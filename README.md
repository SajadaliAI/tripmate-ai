Markdown
# 🌍 TripMate AI — Multi-Agent Travel Planning Assistant

**TripMate AI** is a production-grade, intelligent travel assistant built using an **Agentic Multi-Agent Architecture** powered by **LangGraph** and **Groq (LLaMA 3.3)**. It converts natural language travel queries into comprehensive, end-to-end travel itineraries including flight estimates, hotel recommendations, and day-by-day plans with budget guardrails.

---

## ✨ Key Highlights & Features

- 🤖 **Agentic Multi-Agent Workflow:** Built using **LangGraph** to coordinate specialized agents (Flight, Hotel, Itinerary, Response).
- 🛡️ **Smart Intent & Guardrails:** Automatically handles greetings ("hi", "hello") with an interactive onboarding prompt and prevents invalid itinerary generation.
- ✈️ **Real-Time Flight Lookup:** Integrated with **AviationStack API** alongside a resilient fallback estimation mechanism.
- 🏨 **Contextual Hotel Search:** Powered by **Tavily Search API** for up-to-date luxury, mid-range, and budget accommodations.
- 🗓️ **Personalized Itinerary Engine:** Generates realistic, day-by-day schedules tailored to activities, food, and culture.
- 💾 **Automated SQLite Persistence:** Logs user sessions, search queries, and generated travel plans into a local SQLite database (`tripmate.db`).
- ⚡ **Asynchronous FastAPI Backend:** Delivers fast REST endpoints (`/api/plan`, `/api/chat`, `/api/history`) with dynamic payload processing.
- 🎨 **Interactive Web UI:** Clean frontend powered by **Jinja2 Templates, HTML5, CSS3, and JavaScript**.

---

## 🏗️ System Architecture

Instead of relying on a single monolithic LLM prompt, TripMate AI breaks down complex travel planning into specialized sub-agents orchestrated by a LangGraph State Workflow:

                  User Request (UI / API)
                             │
                             ▼
                 ┌──────────────────────┐
                 │ Guardrail & Routing  │
                 └───────────┬──────────┘
                             │
                             ▼
                  Flight Agent (Aviation)
                             │
                             ▼
                   Hotel Agent (Tavily)
                             │
                             ▼
                    Itinerary Agent
                             │
                             ▼
            Response Coordinator & Synthesizer
                             │
                             ▼
                 Final Output to User & DB

---

## 🚀 Tech Stack

| Category | Technology / Framework |
| :--- | :--- |
| **Backend Framework** | FastAPI, Uvicorn (ASGI) |
| **AI Orchestration** | LangGraph, LangChain |
| **LLM Engine** | Groq API (`llama-3.3-70b-versatile`) |
| **Data Tools** | AviationStack API, Tavily Search API |
| **Database** | SQLite (Local SQL Persistence) |
| **Frontend & UI** | Jinja2, HTML5, CSS3, JavaScript (Fetch API) |
| **Environment** | Python 3.11, Python-Dotenv |

---

## 📁 Project Structure

tripmate-ai/
│
├── app.py                  # FastAPI application & REST endpoint definitions
├── backend.py              # LangGraph workflow, StateGraph & Node compilation
├── database.py             # SQLite initialization & session tracking functions
├── requirements.txt        # Python dependency declarations
├── .env                    # Secret keys & API configuration
├── README.md               # Project documentation
│
├── agents/                 # Specialized Agent Definitions
│   ├── flight_agent.py     # Flight search logic & AviationStack tool runner
│   ├── hotel_agent.py      # Hotel research agent using Tavily
│   ├── itinerary_agent.py  # Day-by-day schedule generation agent
│   └── response_agent.py   # Synthesis agent & welcome guardrail router
│
├── tools/                  # External API Integrations
│   ├── aviation.py         # AviationStack flight API wrapper
│   └── tavily.py           # Tavily search API integration
│
├── templates/              # Jinja2 Rendering Layer
│   └── index.html          # Main travel interface
│
└── static/                 # Static Assets
├── style.css           # UI Styling
└── script.js           # Frontend API fetch & dynamic UI renderer


---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/SajadAI/tripmate-ai.git
cd tripmate-ai
2. Create Virtual Environment
Bash
# Windows
python -m tripmate python==3.11 -y
Activate Virtual Environment
conda activate tripmate
Bash
pip install -r requirements.txt
🔐 Environment Setup
Create a .env file in the root directory:

Code snippet
GROQ_API_KEY=your_groq_api_key
AVIATIONSTACK_API_KEY=your_aviationstack_api_key
TAVILY_API_KEY=your_tavily_api_key
DEFAULT_ORIGIN_IATA=KHI
DATABASE_URL=sqlite:///tripmate.db
▶️ Running the Application
Start the FastAPI application:

Bash
python app.py
Open your browser and navigate to:
👉 http://127.0.0.1:8000

💬 Example Prompt
"Plan a 5-day holiday package for Dubai for 2 adults under $1200 with historical sites and street food recommendations."
