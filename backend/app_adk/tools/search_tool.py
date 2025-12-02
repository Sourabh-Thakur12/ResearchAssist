# app_adk/tools/search_tool.py

import json
import asyncio
from google.adk.agents import LlmAgent
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.adk.models.google_llm import Gemini
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('/home/sourabh/Coding/ML/research-agent/.env')
load_dotenv(env_path)
key = os.getenv("GEMINI_API_KEY")


# ---------------- SEARCH AGENT ----------------

SearchAgent = LlmAgent(
    name="SearchAgent",
    model=Gemini(model="gemini-2.5-flash", api_key=key),
    instruction="""
You MUST call google_search using:
<tool_call>
{ "query": "<USER_QUERY>" }
</tool_call>

After receiving search results:
- Output ONLY the raw grounded text
- DO NOT format JSON
- DO NOT summarize
- DO NOT invent content
""",
    tools=[google_search]
)


# ---------------- INTERNAL EXECUTOR ----------------

async def _run_search_async_internal(query: str) -> str:
    """
    Runs the SearchAgent and ALWAYS returns a STRING.
    """

    runner = InMemoryRunner(agent=SearchAgent)
    events = await runner.run_debug(query)

    final_text = ""

    for event in events:
        if event.content and event.content.parts:
            text = event.content.parts[0].text
            if text:
                final_text += text + "\n"

    # Always return the raw grounded model output
    return final_text.strip()


# ---------------- PUBLIC API ----------------

async def run_search_async(query: str) -> str:
    return await _run_search_async_internal(query)


def run_search_sync(query: str) -> str:
    return asyncio.run(_run_search_async_internal(query))
