import asyncio
from droidrun import DroidAgent, DroidrunConfig, AgentConfig
from llama_index.llms.google_genai import GoogleGenAI
from dotenv import load_dotenv
from entities.reviews import RawReviewList
from prompts.reviews import fetch_reviews

load_dotenv()

config = DroidrunConfig(AgentConfig(reasoning=True))
llm = GoogleGenAI(model="models/gemini-2.5-pro", temperature=0.8)
agent = DroidAgent(
    goal=fetch_reviews("Neural DSP", "reddit"),
    config=config,
    output_model=RawReviewList,
    llms=llm
)

