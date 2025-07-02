from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, RunConfig, AgentHooks, RunContextWrapper
from agents.handoffs import HandoffInputData
from dotenv import load_dotenv
from typing import TypeVar
from rich import print
import os

#! HandoffInputData:
    #? input_history: str | tuple[TResponseInputItem, ...]
    #? pre_handoff_items: tuple[RunItem, ...]
    #? new_items: tuple[RunItem, ...]

T=TypeVar("T")

set_tracing_disabled(disabled=True)
load_dotenv()

API_KEY = os.environ.get("GEMINI_API_KEY")

model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai"
    ),
)

def handoff_function(data: HandoffInputData) -> HandoffInputData:
    print(data)
    return data

class SubAgentHook(AgentHooks[T]):
    async def on_start(self, ctx: RunContextWrapper[T], agent: Agent[T]):
        print(f"{agent.name} is started")
    
    async def on_end(self, ctx: RunContextWrapper[T], agent: Agent[T], output: str):
        print(f"{agent.name} is stopped with output -> {output}")

    async def on_handoff(self, context, agent, source):
        print(f"{source.name} handsoff to {agent.name}")


addition_agent = Agent(
    name="Addition Agent",
    instructions=(
    "You are an expert in performing basic arithmetic addition. "
    "If the user asks to add two numbers, you should answer directly with the result."
    ),
    model=model,
    handoff_description=(
    "An expert at performing basic arithmetic additions between two numbers."
    ),
    hooks=SubAgentHook()
)
math_expert_agent = Agent(
    name="Mathematician Triage Agent",
    instructions=(
    "You are a math triage expert. "
    "If the user question is related to simple addition, you must hand off to the Addition Agent. "
    "For other math-related queries, answer them yourself."
    ),
    model=model,
    handoffs=[addition_agent],
    handoff_description=(
    "Handles all math-related questions by solving them or handing off to specialized math agents like Addition Agent."
    ),
    hooks=SubAgentHook()
)
triage_agent = Agent(
    name="Triage Agent",
    instructions=(
    "You are a general triage assistant. "
    "If the user question is math-related (like arithmetic or equations), hand off to the Mathematician Triage Agent. "
    "For other domains, answer them directly if possible."
    ),
    handoffs=[math_expert_agent],
    model=model,
    hooks=SubAgentHook()
)
result = Runner.run_sync(
    starting_agent=triage_agent, 
    input="What is 225363252 + 2353532", 
    run_config=RunConfig(handoff_input_filter=handoff_function)
)
print(result.final_output)