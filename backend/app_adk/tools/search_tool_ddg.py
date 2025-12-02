# app_adk/tools/search_tool_ddg.py
import os
import requests
from dotenv import load_dotenv
from typing import List, Dict, Any

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")
BASE_URL = "https://serpapi.com/search.json"


def search_google(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Uses SerpAPI to query Google Search and return:
    [
      { title, url, snippet, score }
    ]
    """

    if not SERPAPI_KEY:
        return [{"error": "SERPAPI_KEY missing in .env"}]

    params = {
        "api_key": SERPAPI_KEY,
        "engine": "google",
        "q": query,
        "num": limit,
        "hl": "en",
        "gl": "in",
    }

    try:
        r = requests.get(BASE_URL, params=params, timeout=15)
    except Exception as e:
        return [{"error": f"Request failed: {e}"}]

    if r.status_code != 200:
        return [{"error": f"SerpAPI returned status {r.status_code}"}]

    data = r.json()

    # Valid results are in "organic_results"
    organic = data.get("organic_results", [])
    if not organic:
        return [{"error": "No organic results returned"}]

    results = []
    for item in organic[:limit]:
        if "raw_extracted_content".startswith("[BrowserTool Error]"):
            continue

        results.append({
            "title": item.get("title"),
            "url": item.get("link"),
            "snippet": item.get("snippet", ""),
            "score": item.get("position", 1)
        })

    return results
