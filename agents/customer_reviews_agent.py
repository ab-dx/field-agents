import asyncio
from droidrun import DroidAgent, DroidrunConfig, AgentConfig
from llama_index.llms.google_genai import GoogleGenAI
from dotenv import load_dotenv
from entities.app_review import RedditReviewList, PlayStoreReviewList, XReviewList
from prompts.reviews import fetch_reviews_app

load_dotenv()

config = DroidrunConfig(AgentConfig(reasoning=True, max_steps=100))
llm = GoogleGenAI(model="models/gemini-2.5-flash", temperature=0.8)

Reddit_agent = DroidAgent(
    goal=fetch_reviews_app("Neural DSP", "reddit"),
    config=config,
    output_model=RedditReviewList,
    llms=llm
)

Playstore_agent = DroidAgent(
    goal=fetch_reviews_app("Neural DSP", "Playstore"),
    config=config,
    output_model=PlayStoreReviewList,
    llms=llm
)

X_agent = DroidAgent(
    goal=fetch_reviews_app("Open AI", "X"),
    config=config,
    output_model=XReviewList,
    llms=llm
)
