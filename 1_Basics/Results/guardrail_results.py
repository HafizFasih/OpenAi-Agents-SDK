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
    set_tracing_disabled
)
from agents.run import RunConfig

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

guardrail_agent = Agent( 
    name="Guardrail check",
    instructions="Check if the user is asking you to do their math homework.",
    output_type=MathHomeworkOutput,
)


@input_guardrail
async def math_guardrail( 
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=ctx.context, run_config=config)

    return GuardrailFunctionOutput(
        output_info=result.final_output, 
        tripwire_triggered=result.final_output.is_math_homework,
    )


agent = Agent(  
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    input_guardrails=[math_guardrail],
)

async def main():
    # This should trip the guardrail
    try:
        result = await Runner.run(agent, "Hello, can you tell me who is the founder of india?", run_config=config)
        
        print("Guardrail didn't trip - this is unexpected")

        print(result.input_guardrail_results)
        #! OUTPUT:
        #* [InputGuardrailResult(guardrail=InputGuardrail(guardrail_function=<function math_guardrail at 0x0000024A16B8EFC0>, name=None), output=GuardrailFunctionOutput(output_info=MathHomeworkOutput(is_math_homework=False, reasoning='The question is about history, not mathematics.'), tripwire_triggered=False))]
        
        #? Similarly there is 'output_guardrail_results' for output guardrails

    except InputGuardrailTripwireTriggered:
        print("Math homework guardrail tripped")

asyncio.run(main())