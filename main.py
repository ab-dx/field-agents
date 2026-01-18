import asyncio
from agents.customer_reviews_agent import X_agent, Reddit_agent, Playstore_agent
from entities.customer_reviews import CustomerReviewReport
import gradio as gr

async def main():
    for agent in [Playstore_agent, X_agent, Reddit_agent]:
        handler = agent.run()

        async for event in handler.stream_events():
            print(event)

        result = await handler
        print(result)

        structured_output = getattr(result, "structured_output", result)

        if hasattr(structured_output, "reviews"):
            report = CustomerReviewReport(reviews=structured_output.reviews)
            print(report.model_dump_json(indent=2))

if __name__ == "__main__":
    asyncio.run(main())
