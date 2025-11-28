import os
from google.adk.agents import LlmAgent, AgentTool
from google.adk.tools import google_search

# --- Configuration Check ---
# ADK expects the API key to be in the environment for real tools.
# This check is just for instructional purposes.
if not os.environ.get("AIzaSyDQ7Ivb2mkxldcJWjDjs2t9vp_YruX6lKk"):
    print("WARNING: GOOGLE_API_KEY environment variable not set. Real ADK search will fail.")


# 1. Define the specialized Search Agent (LlmAgent)
# This agent's only job is to execute web searches using the built-in google_search tool.
SearchAgent = LlmAgent(
    # gemini-2.5-flash is excellent for tool-calling and retrieval tasks
    model="gemini-2.5-flash",
    name="GoogleSearchExecutor",
    instruction="Use the Google Search tool to find relevant, up-to-date research papers, blogs, and articles for the user's query. Return the full text of the search results only.",
    description="A specialist in retrieving information from the web using Google Search Grounding.",
    # The key step: attach the built-in Google Search tool
    tools=[google_search]
)

# 2. Wrap the Search Agent as a Tool
# This allows the RetrieverAgent to call the SearchAgent as an external function.
SearchTool = AgentTool(SearchAgent)

# Note: In a real environment, you would run the SearchAgent via: 
# search_tool_instance.run(query)