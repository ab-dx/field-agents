import asyncio
from agents.customer_reviews_agent import X_agent, Reddit_agent, Playstore_agent
from entities.customer_reviews import CustomerReviewReport

async def main():
    handler = Playstore_agent.run()

    async for event in handler.stream_events():
        print(event)

    result = await handler

    print(result)

    output = getattr(result, "output", result)

    try:
        print(output.model_dump_json(indent=2))
    except Exception:
        print(output)

    if hasattr(output, "reviews"):
        report = CustomerReviewReport(reviews=output.reviews)
        print(report.model_dump_json(indent=2))

if __name__ == "__main__":
    asyncio.run(main())
