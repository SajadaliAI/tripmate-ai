import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

GREETING_WORDS = [
    "hi",
    "hello",
    "hey",
    "assalam o alaikum",
    "aoa",
    "help",
    "hy",
    "ola",
]


def run_response_agent(
    query: str, flight_data: str, hotel_data: str, itinerary_data: str
) -> str:
    """Combines output from Flight, Hotel, and Itinerary agents into a single master response with strict guardrails."""
    clean_query = query.strip().lower()

    # Friendly onboarding message for simple greetings
    if clean_query in GREETING_WORDS or len(clean_query) < 3:
        return """
👋 **Welcome to TripMate AI!**

Main aapka Multi-Agent Travel Coordinator assistant hoon. Complete travel plan (Flights, Hotels & Itinerary) generate karne ke liye mujhe thodi details dein:

* 📍 **Where do you want to go?** (e.g., Dubai, Skardu, Istanbul, London)
* ⏳ **Duration & Budget?** (e.g., 5 days, $1000)
* 👥 **Who is traveling?** (e.g., Solo, 2 adults, Family)

**Example Query:**
> *"Plan a 5-day holiday package for Dubai for 2 adults under $1200."*
"""

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "Response Agent Error: GROQ_API_KEY is missing."

    llm = ChatGroq(
        groq_api_key=api_key,
        model_name="llama-3.3-70b-versatile",
        temperature=0.3,
    )

    prompt = f"""
    You are the Lead Response Coordinator for 'TripMate AI'. Your SOLE purpose is travel planning (flights, hotels, itineraries, budgets, and travel advice).

    --- STRICT TOPIC GUARDRAILS ---
    1. EVALUATE USER INTENT: Read the Original User Query carefully.
    2. REJECT OUT-OF-TOPIC QUERIES: If the query is completely unrelated to travel (e.g., writing python/C++ code, solving math problems, answering political/general science questions, writing essays, or tech support), DO NOT answer the question.
       - Instead, respond ONLY with: 
         "I am TripMate AI, specialized exclusively in travel planning! ✈️ I cannot help with non-travel topics like coding or math. Please ask me a travel-related question!"

    3. TRAVEL INTENT SYNTHESIS: If the query IS about travel, ignore any irrelevant or hallucinated sub-agent findings and synthesize the context into a clean, structured master travel package.

    Original User Query: {query}

    --- FLIGHT DETAILS ---
    {flight_data}

    --- HOTEL OPTIONS --- 
    {hotel_data}

    --- DAY-BY-DAY ITINERARY ---
    {itinerary_data}

    Formatting Guidelines (Only for Travel Queries):
    - Start with a warm, welcoming greeting mentioning the requested destination and duration.
    - Use clear markdown headings (✈️ **Flight Options**, 🏨 **Recommended Accommodations**, 🗓️ **Day-Wise Itinerary**, 💰 **Estimated Budget Breakdown**).
    - Format nicely with markdown tables, bold text, and bullet points.
    - Keep tone engaging, helpful, and ultra-professional.
    """

    response = llm.invoke(prompt)
    return response.content