import asyncio
from agents.customer_reviews_agent import X_agent, Reddit_agent, Playstore_agent
from entities.customer_reviews import CustomerReviewReport

async def main():

    events = []

    handler = X_agent.run()
    # handler = Playstore_agent.run()
    # handler = Reddit_agent.run()

    async for event in handler.stream_events():
        print(event)

    # Wait for final result
    result = await handler
    print(result)
    # report = CustomerReviewReport(reviews=result.reviews)
    # print(report)

if __name__ == "__main__":
    asyncio.run(main())
