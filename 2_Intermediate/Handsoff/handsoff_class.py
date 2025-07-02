from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, handoff, HandoffInputData, RunContextWrapper, RunHooks, AgentHooks
from dotenv import load_dotenv
from rich import print
import os

set_tracing_disabled(disabled=True)
load_dotenv()

class CustomRunHooks(RunHooks):
    async def on_handoff(self, context, from_agent, to_agent):
        print("Run hook handoff function is running")

class CustomAgentHooks(AgentHooks):
    async def on_handoff(self, context, agent, source):
        print("Agent hook handoff function is running")



API_KEY = os.environ.get("GEMINI_API_KEY")

model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai"
    ),
)

def custom_input_filter(input_list: HandoffInputData) -> HandoffInputData:
    print("Hello World")
    return input_list

def on_handsoff_function(ctx: RunContextWrapper[None]) -> None:
    print("on_handsoff_function is running")

math_expert_agent = Agent(
    name="Mathematician", 
    instructions="You are an expert in mathematics. Solve problems accurately and explain your reasoning when needed.",
    model=model,
    handoff_description="Handles all mathematical questions and calculations."
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
    handoffs=[
        math_expert_agent, 
        handoff(
            agent=math_expert_agent,
            input_filter=custom_input_filter,
            on_handoff=on_handsoff_function
        )
    ],
    model=model,
    hooks=CustomAgentHooks()
)

result = Runner.run_sync(starting_agent=triage_agent, input="What is 2 + 2", hooks=CustomRunHooks())
print(result.final_output)
