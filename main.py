import asyncio
from agents.customer_reviews_agent import agent

async def main():

    events = []

    handler = agent.run()

    async for event in handler.stream_events():
        print(event)

    # Wait for final result
    result = await handler
    print(result)
    print(f"✅ Success: {result.success}")
    print(f"📝 Reason: {result.reason}")

if __name__ == "__main__":
    asyncio.run(main())
