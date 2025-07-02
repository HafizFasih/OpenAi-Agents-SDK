#type: ignore
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, RunContextWrapper
from dotenv import load_dotenv
from rich import print
import asyncio
import os
import json

load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY = os.environ.get("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

model = OpenAIChatCompletionsModel(
    openai_client=client,
    model="gemini-2.0-flash",
)

translation_agent=Agent(
    name="Translator",
    instructions="You are a good translator, you can translate given text in any language",
    model=model
)

agent = Agent(
    name="Assistant", 
    instructions=(
        "You are an helpful asssitant"
        "You have tools to help user."
    ), 
    model=model, 
    tools=[
        translation_agent.as_tool(
            tool_name="translator",
            tool_description="A helpful translator",
        )
    ],
)

#! Jab kisi agent ko as a tool use kr rhy ho to phr hamy ek dict ko dumps krky pas krna hota ha or us dict ma ek key hogi with name 'input' or uski value tumhara argument

#! PLUS POINT: Similarly agar ham normal tool ko ese invoke kre to hamy just ussi k parameters k hisab se dict banani hogi 'input' jesi koi key wagera ki zaroorat nhi ha

async def main():
    result =await agent.tools[0].on_invoke_tool( 
        RunContextWrapper(context=None), 
        json.dumps({"input":"Hello How Are You"})
    )
    print(result)

asyncio.run(main())
