import asyncio
from droidrun import DroidAgent, DroidrunConfig, AgentConfig
from llama_index.llms.google_genai import GoogleGenAI
from dotenv import load_dotenv
from entities.app_review import RedditReviewList, PlayStoreReviewList, XReviewList
from prompts.reviews import fetch_reviews_app
from tools.compute_sentiments import TOOLS_REDDIT_X, TOOLS_PLAYSTORE

load_dotenv()
config = DroidrunConfig(AgentConfig(reasoning=True, max_steps=50))
llm = GoogleGenAI(model="models/gemini-2.5-pro", temperature=0.8)

Reddit_agent = DroidAgent(
    goal=fetch_reviews_app("Neural DSP", "reddit"),
    config=config,
    output_model=RedditReviewList,
    llms=llm,
    custom_tools=TOOLS_REDDIT_X,
)

Playstore_agent = DroidAgent(
    goal=fetch_reviews_app("Open AI", "Playstore"),
    config=config,
    output_model=PlayStoreReviewList,
    llms=llm,
    custom_tools=TOOLS_PLAYSTORE,
)

X_agent = DroidAgent(
    goal=fetch_reviews_app("Open AI", "X"),
    config=config,
    output_model=XReviewList,
    llms=llm,
    custom_tools=TOOLS_REDDIT_X,
)