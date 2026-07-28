import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from tavily import TavilyClient

load_dotenv()


@tool
def tavily_search(query: str) -> str:
    """Searches the web for hotel accommodation, attractions, local food, and general travel information using Tavily API.

    Args:
        query (str): The search query (e.g. 'Best budget hotels in Istanbul Turkey').
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "Tavily API Key missing. Please set TAVILY_API_KEY in your .env file."

    try:
        client = TavilyClient(api_key=api_key)
        response = client.search(query=query, max_results=5)

        results = []
        for i, r in enumerate(response.get("results", []), 1):
            title = r.get("title", "Unknown")
            url = r.get("url", "")
            snippet = r.get("content", "").strip()

            if len(snippet) > 300:
                snippet = snippet[:300].rsplit(" ", 1)[0] + "..."

            results.append(f"{i}. **{title}**\n   {url}\n   {snippet}")

        return "\n\n".join(results) if results else "No relevant web search results found."

    except Exception as e:
        return f"Tavily search API error: {str(e)}"