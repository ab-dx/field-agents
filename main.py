import asyncio
from agents.customer_reviews_agent import agent
from entities.customer_reviews import CustomerReviewReport

async def main():

    events = []

    handler = agent.run()

    async for event in handler.stream_events():
        print(event)

    # Wait for final result
    result = await handler
    print(result)
    report = CustomerReviewReport(reviews=result.reviews)
    print(report)

if __name__ == "__main__":
    asyncio.run(main())
