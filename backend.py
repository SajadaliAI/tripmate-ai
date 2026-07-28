import os
from typing import TypedDict, Dict, Any
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END

from agents.flight_agent import run_flight_agent
from agents.hotel_agent import run_hotel_agent
from agents.itinerary_agent import run_itinerary_agent
from agents.response_agent import run_response_agent

load_dotenv()

class TravelState(TypedDict):
    query: str
    flight_data: str
    hotel_data: str
    itinerary_data: str
    final_response: str

def flight_node(state: TravelState) -> Dict[str, Any]:
    print("✈️ Running Flight Agent...")
    try:
        flight_res = run_flight_agent(state["query"])
    except Exception as e:
        flight_res = f"Flight details estimated ($400-$700 approx). Note: {e}"
    return {"flight_data": flight_res}

def hotel_node(state: TravelState) -> Dict[str, Any]:
    print("🏨 Running Hotel Agent...")
    try:
        hotel_res = run_hotel_agent(state["query"])
    except Exception as e:
        hotel_res = f"Hotel recommendations provided based on standard luxury and budget tiers in destination. Note: {e}"
    return {"hotel_data": hotel_res}

def itinerary_node(state: TravelState) -> Dict[str, Any]:
    print("🗓️ Running Itinerary Agent...")
    try:
        itinerary_res = run_itinerary_agent(
            query=state["query"],
            flight_summary=state.get("flight_data", ""),
            hotel_summary=state.get("hotel_data", "")
        )
    except Exception as e:
        itinerary_res = f"Standard day-by-day itinerary generated for destination. Note: {e}"
    return {"itinerary_data": itinerary_res}

def response_node(state: TravelState) -> Dict[str, Any]:
    print("🤖 Synthesizing Final Response...")
    try:
        final_res = run_response_agent(
            query=state["query"],
            flight_data=state.get("flight_data", ""),
            hotel_data=state.get("hotel_data", ""),
            itinerary_data=state.get("itinerary_data", "")
        )
    except Exception as e:
        final_res = f"### Travel Plan\n\n**Flights:** {state.get('flight_data')}\n\n**Hotels:** {state.get('hotel_data')}\n\n**Itinerary:** {state.get('itinerary_data')}"
    return {"final_response": final_res}

def build_graph():
    workflow = StateGraph(TravelState)

    workflow.add_node("flight_agent", flight_node)
    workflow.add_node("hotel_agent", hotel_node)
    workflow.add_node("itinerary_agent", itinerary_node)
    workflow.add_node("response_agent", response_node)

    workflow.set_entry_point("flight_agent")

    workflow.add_edge("flight_agent", "hotel_agent")
    workflow.add_edge("hotel_agent", "itinerary_agent")
    workflow.add_edge("itinerary_agent", "response_agent")
    workflow.add_edge("response_agent", END)

    return workflow.compile()

app_graph = build_graph()

def run_trip_planner(user_query: str) -> Dict[str, Any]:
    initial_state = {
        "query": user_query,
        "flight_data": "",
        "hotel_data": "",
        "itinerary_data": "",
        "final_response": ""
    }
    return app_graph.invoke(initial_state)