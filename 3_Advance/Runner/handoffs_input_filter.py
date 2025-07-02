from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, RunConfig, handoff
from agents.handoffs import HandoffInputData
from dotenv import load_dotenv
from rich import print
import random
import os


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


def agent_handoff_input_filter(data: HandoffInputData) -> HandoffInputData:
    print("\nAgent handoffs input filter executed")
    return data

def runner_handoff_input_filter(data: HandoffInputData) -> HandoffInputData:
    print("\nRunner handoffs input filter executed")
    return data


run_config=RunConfig(
    handoff_input_filter=runner_handoff_input_filter
)

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

agent_handoff=handoff(
    agent=physics_expert_agent,
    input_filter=agent_handoff_input_filter
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
        agent_handoff
    ],
    model=model
)

math_related_question = "What is the derivative of x^2" 
physics_related_question = "Explain me the theory of relaitivity"

result = Runner.run_sync(
    starting_agent=triage_agent, 
    input=physics_related_question, 
    run_config=run_config
)

print(result.final_output)

#! Runner.run_config ma agar input filter dia hua ha to wo har handoff pr chalega siwaye ek condition k
#! agar agent k pass khud apna input_filter function ha to is case ma agent wala hi chalega.
#! or agar agent k pas apna khud ka input filter function nh ha to zahir si baat ha phr runner ka chalega  

input_filter = agent_handoff.input_filter or (
    run_config.handoff_input_filter if run_config else None
)

#! backend ma ye logic likhi hoti ha
