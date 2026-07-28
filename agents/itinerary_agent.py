import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from tools.tavily import tavily_search

load_dotenv()


def run_itinerary_agent(
    query: str, flight_summary: str = "", hotel_summary: str = ""
) -> str:
    """Creates a day-wise personalized travel itinerary including sightseeing, food, & culture."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "Itinerary Agent Error: GROQ_API_KEY is missing."

    llm = ChatGroq(
        groq_api_key=api_key, model_name="llama-3.3-70b-versatile", temperature=0.5
    )

    # Search popular attractions & food spots
    search_query = f"top attractions historical places food recommendations {query}"
    attractions_data = tavily_search.invoke({"query": search_query})

    prompt = f"""
    You are an expert Travel Itinerary Planner.
    Create a complete day-by-day travel plan based on the request and contextual details provided.
    
    User Query: {query}
    Flight Context: {flight_summary}
    Hotel Context: {hotel_summary}
    Attractions Search Data: {attractions_data}
    
    Instructions:
    1. Build a clear Day-wise schedule (e.g., Day 1, Day 2, etc.).
    2. Include historical sites, cultural experiences, activity time slots (Morning, Afternoon, Evening), and local food/restaurant recommendations.
    3. Ensure the schedule is realistic and enjoyable without rushing.
    """

    response = llm.invoke(prompt)
    return response.content