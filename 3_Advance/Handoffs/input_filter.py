from agents import Agent, Runner, handoff, HandoffInputData
from agents.extensions.handoff_filters import remove_all_tools
from rich import print

physics_expert_agent = Agent(
    name="Physicist", 
    instructions="You are an expert in physics. Provide clear and precise answers to physics-related problems and concepts.",
)

math_expert_agent = Agent(
    name="Mathematician", 
    instructions="You are an expert in mathematics. Solve problems accurately and explain your reasoning when needed.",
)

chemist_agent = Agent(
    name="Chemist",
    instructions=(
        "Help the user with their questions."
        "If they ask about chemist, give them proper answer"
        "If they ask about maths, handoff to the maths agent."
        "If they ask about physics, handoff to the physics agent."
    ),
    handoffs=[
        handoff(
            agent=math_expert_agent,
            input_filter=remove_all_tools
        ), 
        physics_expert_agent
    ],
)

result = Runner.run_sync(starting_agent=chemist_agent, input="What is 2 + 2")
print(result.final_output)

