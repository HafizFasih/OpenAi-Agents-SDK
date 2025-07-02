from openai import AsyncOpenAI
from dotenv import load_dotenv
from rich import print
import asyncio
import os

load_dotenv()

API_KEY = os.environ.get("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

async def main():
    result = await client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "What is the capital of Pakistan"}
        ]
    )
    print(result)

asyncio.run(main())
    