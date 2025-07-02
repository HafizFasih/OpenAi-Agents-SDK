from openai import AsyncOpenAI
from dotenv import load_dotenv
from rich import print
import asyncio
import os

load_dotenv()

API_KEY = os.environ.get("OPENAI_API_KEY")

client = AsyncOpenAI(
    api_key=API_KEY,
)

async def main():
    result = await client.responses.create(
        model="gpt-4.1-mini",
        input="What is the capital of Pakistan"
    )
    print(result)

asyncio.run(main())
