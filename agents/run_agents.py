import asyncio
import threading
from state.state import AppState
from agents.customer_reviews_agent import create_agents
from entities.customer_reviews import CustomerReviewReport

async def run_agents():
    state = AppState.instance()
    agents = create_agents()
    for src, agent in agents:
        handler = agent.run()

        async for event in handler.stream_events():
            print(event)
            if(hasattr(event, 'response')):
                state.add_event(str(event.response))

        result = await handler
        print(result)

        structured_output = getattr(result, "structured_output", result)

        if hasattr(structured_output, "reviews"):
            report = CustomerReviewReport(reviews=structured_output.reviews)
            print(report.model_dump_json(indent=2))
            state.add_report(report.model_dump_json())
            state.update_kpi(f"{src} Sentiment Score", report.sentiment_score())
            state.update_kpi(f"{src} Customer Satisfaction", report.avg_csat())
            state.update_kpi(f"{src} Average NPS Rating", report.avg_nps_rating())
            state.update_kpi(f"{src} NPS", report.nps())
            state.update_kpi(f"{src} Data Quality", report.data_quality())

def launch_agents(query):
    if len(query) == 0:
        return
    AppState.instance().set_target(query)
    agent_thread = threading.Thread(target=lambda: asyncio.run(run_agents()), daemon=True)
    agent_thread.start()

if __name__ == "__main__":
    launch_agents("Clash Royale")

