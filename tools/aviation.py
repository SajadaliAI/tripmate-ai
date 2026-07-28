import os
import requests
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()

@tool
def search_flights(query: str) -> str:
    """Searches flight details or returns standard estimation if API is restricted."""
    api_key = os.getenv("AVIATIONSTACK_API_KEY")
    origin = os.getenv("DEFAULT_ORIGIN_IATA", "KHI")

    if not api_key:
        return f"Flight status query for route starting from {origin}. API key missing, using standard route estimates."

    try:
        url = "http://api.aviationstack.com/v1/flights"
        params = {
            "access_key": api_key,
            "limit": 5
        }
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if "data" in data and len(data["data"]) > 0:
                flights = data["data"][:3]
                summary = []
                for f in flights:
                    airline = f.get("airline", {}).get("name", "Unknown Airline")
                    flight_num = f.get("flight", {}).get("number", "N/A")
                    dep = f.get("departure", {}).get("airport", "N/A")
                    arr = f.get("arrival", {}).get("airport", "N/A")
                    status = f.get("flight_status", "scheduled")
                    summary.append(f"Airline: {airline} | Flight: {flight_num} | From: {dep} -> To: {arr} | Status: {status}")
                return "\n".join(summary)
        
        return f"Route Origin: {origin}. Live flight data unavailable for this specific route. Provide estimated flight fare ranges ($300 - $600 per person)."
    except Exception as e:
        return f"Route Origin: {origin}. Live API lookup skipped ({str(e)}). Provide standard flight estimations for this destination."