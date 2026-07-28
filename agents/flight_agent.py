import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from tools.aviation import search_flights

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


def run_flight_agent(query: str) -> str:
    """Uses AviationStack flight tool or fallback logic to fetch flight estimates."""
    clean_query = query.strip().lower()

    # Early exit for simple greetings or empty queries
    if clean_query in GREETING_WORDS or len(clean_query) < 3:
        return "No flight details required (User provided a general greeting)."

    try:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return "Flight Agent: GROQ_API_KEY is missing."

        llm = ChatGroq(
            groq_api_key=api_key,
            model_name="llama-3.3-70b-versatile",
            temperature=0.2,
        )

        try:
            flight_raw_data = search_flights.invoke({"query": query})
        except Exception:
            flight_raw_data = (
                "Standard route estimation requested from user origin."
            )

        prompt = f"""
        You are an expert Flight Agent in TripMate AI.
        Analyze the user request and flight data below:

        User Query: {query}
        Flight Data Context: {flight_raw_data}

        Instructions:
        1. Identify the actual origin and destination from the User Query.
        2. If the user query lacks a specific travel destination, state clearly that destination details are needed.
        3. If the Flight Data Context contains irrelevant or generic global flights (e.g., China/Italy flights when asking for NYC), IGNORE those specific routes.
        4. Provide realistic estimated round-trip flight prices (USD per person) for the route requested in the User Query from major international hubs.
        5. Name 3-4 top major airlines that operate flights to the target destination.
        6. Keep the response clean, clear, and professional.
        """

        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"✈️ Flight Estimation: Round-trip flights typically range from $350 - $650 per person depending on destination and season. (Notice: {str(e)})"