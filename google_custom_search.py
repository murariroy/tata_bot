



import os
import requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

def search_google_custom(query: str) -> str:
    try:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": GOOGLE_API_KEY,
            "cx": SEARCH_ENGINE_ID,
            "q": query,
            "num": 5
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        results = response.json().get("items", [])

        if not results:
            return "No relevant information found on the web."

        formatted_results = []
        for item in results[:5]:
            title = item.get("title", "")
            snippet = item.get("snippet", "")
            link = item.get("link", "")
            formatted_results.append(f"• {title}\n{snippet}\n{link}")

        return "\n\n".join(formatted_results)

    except Exception as e:
        return f"Google Search error: {str(e)}"
