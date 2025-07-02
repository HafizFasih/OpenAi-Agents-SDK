from agents import Agent, Runner, trace, set_default_openai_api, set_default_openai_client, set_trace_processors
from agents.tracing.processor_interface import TracingProcessor
from openai import AsyncOpenAI
from rich import print
import asyncio
import os

API_KEY=os.environ.get("GEMINI_API_KEY")

client=AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

set_default_openai_client(client)
set_default_openai_api("chat_completions")

class CustomTracingProcessor(TracingProcessor):
    def on_trace_start(self, trace):
        print(trace.export())
    def on_trace_end(self, trace):
        print(trace.export())
    def on_span_end(self, span):
        print("span end")
    def on_span_start(self, span):
        print("span start")
    def force_flush(self):
        return super().force_flush()
    def shutdown(self):
        return super().shutdown()

trace_processor=CustomTracingProcessor()
set_trace_processors([trace_processor])

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model="gemini-2.0-flash"
)

async def main():
    with trace("Test Flow"):
        result = await Runner.run(agent, "Tell me 5 best jokes")
        print(result.final_output)

asyncio.run(main())