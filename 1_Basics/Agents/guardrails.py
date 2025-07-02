from pydantic import BaseModel
from dotenv import load_dotenv
import asyncio, os
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_tracing_disabled,
    enable_verbose_stdout_logging
)
from agents.run import RunConfig
from rich import print

# enable_verbose_stdout_logging()
load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY=os.environ.get("GEMINI_API_KEY")

model=OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
)

config=RunConfig(
    model=model
) 

class MathHomeworkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str

guardrail_agent = Agent[MathHomeworkOutput]( 
    name="Guardrail check",
    instructions="Check if the user is asking you to do their math homework.",
    output_type=MathHomeworkOutput,
    model=model
)

@input_guardrail(name="math")
async def math_guardrail( 
    ctx: RunContextWrapper[MathHomeworkOutput], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(
        starting_agent=guardrail_agent,
        input=input
    )
    print(agent.name)
    print(result.final_output)
    return GuardrailFunctionOutput(
        output_info="checking", 
        tripwire_triggered=result.final_output.is_math_homework,
    )

agent = Agent(  
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    input_guardrails=[math_guardrail],
)

async def main():
    try:
        await Runner.run(agent, "What is the capital of pakistan", run_config=config)
        print("Guardrail didn't trip")

    except InputGuardrailTripwireTriggered:
        print("Math homework guardrail tripped")

asyncio.run(main())
