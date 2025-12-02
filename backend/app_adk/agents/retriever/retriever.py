import os
import json
import asyncio
import re
from typing import List, Dict

from app_adk.tools.search_tool_ddg import search_google as search_ddg





from app_adk.tools.browser_tool import BrowserTool


class RetrieverAgent:
    """
    PURE Python retriever using ScrapeAPI Google Search:
    - Expands boolean query into multiple real search queries
    - Searches Google using ScrapeAPI
    - Scrapes URLs using BrowserTool (BeautifulSoup)
    """

    def __init__(self, max_search_results: int = 5):
        self.max_search_results = max_search_results
        self.browser = BrowserTool()

    # -----------------------------------------------------------
    # Query Expansion (turn one boolean query into 3–6 variations)
    # -----------------------------------------------------------
    def expand_queries(self, boolean_query: str) -> List[str]:
        cleaned = re.sub(r"[\"()]", "", boolean_query)
        cleaned = cleaned.replace("AND", "").replace("OR", "").strip()
        words = [w for w in cleaned.split() if w]

        if len(words) < 2:
            return [cleaned]

        q1 = " ".join(words)
        q2 = " ".join(words[:4])
        q3 = f"{words[0]} {words[1]} dating evidence"
        q4 = f"{words[0]} {words[1]} archaeological evidence"
        q5 = f"{words[0]} {words[1]} historical research"

        return list(dict.fromkeys([q1, q2, q3, q4, q5]))  # unique list

    # -----------------------------------------------------------
    # Main RUN function
    # -----------------------------------------------------------
    async def run(self, structured_query_json: str) -> str:
        try:
            query_data = json.loads(structured_query_json)
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON"}, indent=2)

        boolean_queries = query_data.get("boolean_queries", [])
        if not boolean_queries:
            return json.dumps({"error": "boolean_queries missing"}, indent=2)

        primary = boolean_queries[0]
        expanded_queries = self.expand_queries(primary)

        print("\n[Retriever] Running expanded queries →")
        for q in expanded_queries:
            print("  →", q)

        # -----------------------------------------------------------
        # Run all searches (ScrapeAPI Google Search)
        # -----------------------------------------------------------
        all_results = []

        for q in expanded_queries:
            results = search_ddg(q, limit=self.max_search_results)

            print(f"\n[DEBUG] Query: {q}")
            print("[DEBUG] Raw Results Returned:")
            try:
                print(json.dumps(results, indent=2))
            except:
                print(results)

            if isinstance(results, list):
                all_results.extend(results)


        # Filter unusable results (errors, missing URL)
        usable = [
            r for r in all_results
            if r.get("url") and not r.get("error")
        ]

        if not usable:
            return json.dumps({"error": "Search returned no usable results"}, indent=2)

        # Deduplicate by URL
        seen_urls = set()
        unique_results = []
        for r in usable:
            if r["url"] not in seen_urls:
                seen_urls.add(r["url"])
                unique_results.append(r)

        # -----------------------------------------------------------
        # Scrape each URL
        # -----------------------------------------------------------
        documents = []
        for idx, r in enumerate(unique_results):
            url = r["url"]
            print(f"[Retriever] Scraping {idx+1}/{len(unique_results)} → {url}")

            try:
                content = self.browser.scrape(url)
            except Exception as e:
                content = f"[BrowserTool Error] {e}"

            documents.append({
                "title": r.get("title", "Untitled"),
                "url": url,
                "snippet": r.get("snippet", ""),
                "raw_extracted_content": content,
                "relevance_score": r.get("score", 1.0)
            })

        # -----------------------------------------------------------
        # Final structured output
        # -----------------------------------------------------------
        output = {
            "core_question": query_data.get("core_question"),
            "documents": documents
        }

        return json.dumps(output, indent=2)


# -----------------------------------------------------------
# Local Runner
# -----------------------------------------------------------
async def run_pipeline():
    parser_path = os.path.join(
        os.path.dirname(__file__), "..", "query_parser", "prompt.json"
    )
    parser_data = json.load(open(parser_path))

    retriever = RetrieverAgent()
    return await retriever.run(json.dumps(parser_data))


if __name__ == "__main__":
    out = asyncio.run(run_pipeline())
    print("\n--- Retriever Output ---\n")
    print(out)

    # Save JSON for next agent
    try:
        parsed = json.loads(out)
        with open("app_adk/agents/retriever/prompt.json", "w", encoding="utf-8") as f:
            json.dump(parsed, f, indent=4, ensure_ascii=False)
        print("\n✅ Saved retriever/prompt.json")
    except:
        print("❌ Failed to save JSON")
