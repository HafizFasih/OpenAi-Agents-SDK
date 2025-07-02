from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, RunHooks, function_tool, enable_verbose_stdout_logging, ModelSettings
from dotenv import load_dotenv
from rich import print
import os

# enable_verbose_stdout_logging()
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

@function_tool
def add(a: int, b: int) -> int:
    """Add two numbers
    Args:
        a: first number
        b: second number
    """
    return a + b 

class CustomRunHooks(RunHooks):
    async def on_agent_start(self, context, agent):
        print(f"{agent.name} is started")

    async def on_agent_end(self, context, agent, output):
        print(f"{agent.name} is ended with output: {output}")

    async def on_tool_start(self, context, agent, tool):
        print(f"{agent.name} has called tool named {tool.name}")
    
    async def on_tool_end(self, context, agent, tool, result):
        print(f"The Tool of {agent.name} known as {tool.name} is ended with the output: {result}" )
    
    async def on_handoff(self, context, from_agent, to_agent):
        print(f"{from_agent.name} handoffs to {to_agent.name}")



math_expert_agent = Agent(
    name="Mathematician", 
    instructions="You are an expert in mathematics. Solve problems accurately and explain your reasoning when needed.",
    model=model,
    handoff_description="Handles all mathematical questions and calculations.",
    tools=[add],
    model_settings=ModelSettings(
        tool_choice="required"
    )
)

physics_expert_agent = Agent(
    name="Physicist", 
    instructions="You are an expert in physics. Provide clear and precise answers to physics-related problems and concepts.",
    model=model,
    handoff_description="Handles all physics-related queries and theoretical explanations."
)

triage_agent = Agent(
    name="Triage agent",
    instructions=(
        "Help the user with their questions."
        "If they ask about maths, handoff to the maths agent."
        "If they ask about physics, handoff to the physics agent."
    ),
    handoffs=[math_expert_agent, physics_expert_agent],
    model=model,
)

result = Runner.run_sync(
    starting_agent=triage_agent, 
    input="What is 2 + 2", 
    hooks=CustomRunHooks()
)
print(result.final_output)

#! bhai tu tool use q nhi kr rhaa ha