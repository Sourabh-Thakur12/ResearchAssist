# app_adk/agents/query_parser/parser.py

import os
import json
import asyncio
from pathlib import Path
from google.adk.agents import LlmAgent
from google.adk.runners import InMemoryRunner
from google.adk.models.google_llm import Gemini
from dotenv import load_dotenv

from app_adk.agents.query_parser import prompt


# Load env
env_path = Path('/home/sourabh/Coding/ML/research-agent/.env')
load_dotenv(env_path)
key = os.getenv("GEMINI_API_KEY")

# Build the LLM Agent
agent_prompt = prompt.prompt()
parser_agent = LlmAgent(
    name="parser_agent",
    model=Gemini(model="gemini-2.5-flash", api_key=key),
    instruction=agent_prompt
)


# ---------------------------------------------------------
# ASYNC RUNNER
# ---------------------------------------------------------
async def runner(user_question: str) -> str:
    """
    Runs the parser agent and returns JSON string.
    """
    enhanced_runner = InMemoryRunner(agent=parser_agent)

    events = await enhanced_runner.run_debug(user_question)

    parsed_prompt = None

    # Extract first valid JSON from model output
    for event in events:
        if event.content and event.content.parts:
            text = event.content.parts[0].text
            try:
                parsed_prompt = json.loads(text)
                break
            except:
                pass

    if parsed_prompt is None:
        parsed_prompt = {"error": "Parser could not generate valid JSON"}

    return json.dumps(parsed_prompt, indent=4)


# ---------------------------------------------------------
# WRITE JSON TO FILE — NEEDED BY OTHER AGENTS
# ---------------------------------------------------------
def spit_JSON_prompt(data):
    """
    Save parsed prompt JSON to the query_parser folder.
    """
    output_path = 'app_adk/agents/query_parser/prompt.json'

    with open(output_path, 'w+', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=4))

    print(f"[Parser] JSON written successfully → {output_path}")


# ---------------------------------------------------------
# OPTIONAL: STANDALONE TESTING MODE
# ---------------------------------------------------------
if __name__ == "__main__":
    user_question = input("Enter your research question: ")

    out = asyncio.run(runner(user_question))

    try:
        parsed = json.loads(out)
        spit_JSON_prompt(parsed)
    except Exception as e:
        print("❌ Could not write JSON:", e)

    print("\n--- PARSER OUTPUT ---\n")
    print(out)
