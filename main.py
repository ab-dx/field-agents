import asyncio
from agents.customer_reviews_agent import X_agent, Reddit_agent, Playstore_agent
from entities.customer_reviews import CustomerReviewReport
import gradio as gr

async def main():
    for agent in [Playstore_agent]:
        handler = agent.run()

        async for event in handler.stream_events():
            print(event)

        result = await handler
        print(result)
        structured_output = getattr(result, "structured_output", result)
    
        if hasattr(structured_output, "avg_star_rating"):
            print("Average star ratings:", structured_output.avg_star_rating)

        if hasattr(structured_output, "no_of_reviews"):
            print("Playstore Total Reviews:", structured_output.no_of_reviews)

        if hasattr(structured_output, "no_of_downloads"):
            print("Playstore Total Downloads:", structured_output.no_of_downloads)

        if hasattr(structured_output, "reviews"):
            report = CustomerReviewReport(reviews=structured_output.reviews)
            print(report.model_dump_json(indent=2))

if __name__ == "__main__":
    asyncio.run(main())
