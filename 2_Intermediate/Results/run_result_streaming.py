import asyncio, os
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, AgentOutputSchema, AgentHooks, RunContextWrapper
from dotenv import load_dotenv
from rich import print
from typing import TypeVar

load_dotenv()
set_tracing_disabled(disabled=True)


T=TypeVar("T")
API_KEY=os.environ.get("GEMINI_API_KEY")

model=OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai"
    )
)


class SubAgentHook(AgentHooks[T]):
    async def on_start(self, ctx: RunContextWrapper[T], agent: Agent[T]):
        print(f"{agent.name} is started")
    
    async def on_end(self, ctx: RunContextWrapper[T], agent: Agent[T], output: str):
        print(f"{agent.name} is stopped with output -> {output}")

    async def on_handoff(self, ctx: RunContextWrapper[T], agent: Agent[T], source: Agent[T]):
        print(f"{source.name} handoffs to {agent.name}")


math_expert_agent = Agent(
    name="Mathematician", 
    instructions="You are an expert in mathematics. Solve problems accurately and explain your reasoning when needed.",
    model=model,
    handoff_description="Handles all mathematical questions and calculations.",
    hooks=SubAgentHook()
)

physics_expert_agent = Agent(
    name="Physicist", 
    instructions="You are an expert in physics. Provide clear and precise answers to physics-related problems and concepts.",
    model=model,
    handoff_description="Handles all physics-related queries and theoretical explanations.",
    hooks=SubAgentHook()
)


async def main():
    triage_agent = Agent(
        name="Triage agent",
        instructions=(
            "Help the user with their questions."
            "If they ask about maths, handoff to the maths agent."
            "If they ask about physics, handoff to the physics agent."
        ),
        handoffs=[math_expert_agent, physics_expert_agent],
        model=model,
        hooks=SubAgentHook()
    )

    result = Runner.run_streamed(triage_agent, input="What is the sum of 10 and 42")
    async for _ in result.stream_events():
        #* Extra Things
        print(result.cancel())
        print(result.current_agent.name)
        print(result.current_turn)
        print(result.is_complete) #? False
        #* RunResultBase
        print(result.last_agent.name == result.current_agent.name) #! Always be true
        print(result.final_output) #! None
        print(result.input)
        print(result.new_items)
        print(result.input_guardrail_results)
        print(result.output_guardrail_results)
        print(result.context_wrapper)
        print(result.last_response_id)
        print(result.to_input_list())
        print(result.final_output_as(cls=str, raise_if_incorrect_type=True))
    print(result.is_complete) #? True
    print(result.final_output) #! Output

if __name__ == "__main__":
    asyncio.run(main())