from droidrun import DroidAgent, DroidrunConfig, AgentConfig
from llama_index.llms.google_genai import GoogleGenAI
from dotenv import load_dotenv
from entities.app_review import RedditReviewList, PlayStoreReviewList, XReviewList
from prompts.reviews import fetch_reviews_app
from state.state import AppState
from tools.compute_sentiments import TOOLS_REDDIT_X, TOOLS_PLAYSTORE

load_dotenv()
config = DroidrunConfig(AgentConfig(reasoning=True, max_steps=100))
llm = GoogleGenAI(model="models/gemini-2.5-flash", temperature=0.8)

def create_agents():
    return list(zip(["Reddit, PlayStore, X"], [DroidAgent(
            goal=fetch_reviews_app(AppState.instance().get_target(), "reddit"),
            config=config,
            output_model=RedditReviewList,
            llms=llm,
            custom_tools=TOOLS_REDDIT_X,
        ),
        DroidAgent(
            goal=fetch_reviews_app(AppState.instance().get_target(), "Playstore"),
            config=config,
            output_model=PlayStoreReviewList,
            llms=llm,
            custom_tools=TOOLS_PLAYSTORE,
        ),

        DroidAgent(
            goal=fetch_reviews_app(AppState.instance().get_target(), "X"),
            config=config,
            output_model=XReviewList,
            llms=llm,
            custom_tools=TOOLS_REDDIT_X,
        )
    ]))

