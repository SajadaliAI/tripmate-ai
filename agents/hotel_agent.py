import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from tools.tavily import tavily_search

load_dotenv()


def run_hotel_agent(query: str) -> str:
    """Uses Tavily search tool to find best hotels matching the user's destination & budget."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "Hotel Agent Error: GROQ_API_KEY is missing."

    llm = ChatGroq(
        groq_api_key=api_key, model_name="llama-3.3-70b-versatile", temperature=0.3
    )

    # Search web via Tavily for hotel options
    search_query = f"best budget hotels accommodation in {query}"
    hotel_raw_data = tavily_search.invoke({"query": search_query})

    prompt = f"""
    You are an expert Hotel & Accommodation Agent.
    Based on the user's query and web search results, recommend 3 top hotel/stay options.
    
    User Query: {query}
    Search Results:
    {hotel_raw_data}
    
    Instructions:
    1. Suggest 3 hotels ranging from Budget to Mid-Range/Luxury depending on user's preference.
    2. Include Hotel Name, Brief Description, Estimated Price per night (in USD), and Key Amenities.
    3. Keep it well-formatted with bullet points.
    """

    response = llm.invoke(prompt)
    return response.content