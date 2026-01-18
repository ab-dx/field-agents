import asyncio
from droidrun import DroidAgent, DroidrunConfig, AgentConfig
from llama_index.llms.google_genai import GoogleGenAI
from dotenv import load_dotenv
from entities.customer_reviews import CustomerReviewList
from prompts.reviews import fetch_reviews_chrome

load_dotenv()

config = DroidrunConfig(AgentConfig(reasoning=True, max_steps=100))
llm = GoogleGenAI(model="models/gemini-2.5-flash", temperature=0.8)

agent = DroidAgent(
    goal=fetch_reviews_chrome("Neural DSP", "reddit"),
    config=config,
    output_model=CustomerReviewList,
    llms=llm
)
