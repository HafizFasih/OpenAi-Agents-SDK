from agents import Agent, Runner, HandoffInputData, handoff, RunHooks
from rich import print
import asyncio

def calculus_input_filter_function(input: HandoffInputData) -> HandoffInputData:
    print("calculus_input_filter_function")
    input.input_history = "Tell me about the orientation of benzene in one sentence"
    return input

calculus_expert_agent = Agent(
    name="calculus agent", 
    instructions=(
        "You are an expert in calculus. Provide clear and precise answers to calculus-related problems and concepts. "
        "If they ask about chemistry, handoff to the chemist agent."
    ),
)

def maths_input_filter_function(input: HandoffInputData) -> HandoffInputData:
    print("maths_input_filter_function")
    input.input_history = "Tell me about the theory of quantam physics in one sentence"
    return input

math_expert_agent = Agent(
    name="Mathematician", 
    instructions=(
        "You are an expert in basic mathematics NOT IN CALCULUS. Solve problems accurately and explain your reasoning when needed. "
        "If they ask about CALCULUS, handoff to the calculus agent."
    ),
    handoffs=[
        handoff(
            agent=calculus_expert_agent,
            input_filter=maths_input_filter_function
        )
    ]
)

def chemistry_input_filter_function(input: HandoffInputData) -> HandoffInputData:
    print("chemistry_input_filter_function")
    input.input_history = "Teach me the basics of calculus in one sentence"
    return input

chemist_agent = Agent(
    name="Chemist",
    instructions=(
        "You are an expert in Chemistry. "
        "If they ask about maths, handoff to the maths agent."
    ),
    handoffs=[
        handoff(
            agent=math_expert_agent,
            input_filter=chemistry_input_filter_function
        )
    ],
)

class CustomRunHooks(RunHooks):
    async def on_handoff(self, context, from_agent, to_agent):
        print(f"{from_agent.name} handoffs to {to_agent.name}")


async def main():
    calculus_expert_agent.handoffs.append(
        handoff(
            agent=chemist_agent,
            input_filter=calculus_input_filter_function
        )
    )

    result = await Runner.run(
        starting_agent=chemist_agent, 
        input="What is 2 + 2",
        hooks=CustomRunHooks()
    )
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())