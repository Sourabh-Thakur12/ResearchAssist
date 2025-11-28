# 1. take user input
# 2. Convert into a well defined prompt for best possible result

# Tools
import os
from pathlib import Path
from google.adk.agents import LlmAgent
from google.adk.runners import InMemoryRunner
from google.adk.models.google_llm import Gemini
from dotenv import load_dotenv
import asyncio

# Customs Imports
import prompt

env_path = Path('/home/sourabh/Coding/ML/research-agent/.env')

load_dotenv( dotenv_path= env_path)
key = os.getenv("GEMINI_API_KEY")

agent_prompt = prompt.prompt()

parser_agent = LlmAgent(
    name='parser_agent',
    model=Gemini(model="gemini-2.5-flash" , api_key = key),
    instruction=agent_prompt
)


async def runner():
    enhanced_runner = InMemoryRunner(agent=parser_agent)
    response = await enhanced_runner.run_debug(
    "Research on adk"
    )
    return response

response = asyncio.run(runner())

# TODO: Create a function to spit json file which contains parsed prompt

def spit_JSON_prompt(response):
