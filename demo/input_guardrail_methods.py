from agents import input_guardrail, Agent, Runner, set_tracing_disabled, AsyncOpenAI, RunConfig, OpenAIChatCompletionsModel, RunContextWrapper, TResponseInputItem, GuardrailFunctionOutput, InputGuardrail, InputGuardrailTripwireTriggered
import os
from rich import print

set_tracing_disabled(disabled=True)

API_KEY = os.environ.get("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

config = RunConfig(
    model=OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=client
    )
)
# #! First Method
@input_guardrail
def my_guardrail_func_1(
        ctx: RunContextWrapper, 
        agent: Agent, 
        input: str | list[TResponseInputItem],
    ) -> GuardrailFunctionOutput:
    
    print("Guardrail function is executed")

    return GuardrailFunctionOutput(
        output_info=None,
        tripwire_triggered=True
    )

# print(my_guardrail_func_1.get_name())
# print(my_guardrail_func_1)

# my_guardrail_func_1.guardrail_function( #type: ignore
#     ctx=RunContextWrapper(context=None),
#     agent=Agent(name="Assistant"),
#     input="hello",
# )
async def main():
    await my_guardrail_func_1.run( #type: ignore
        context=RunContextWrapper(context=None),
        agent=Agent(name="Assistant"),
        input="hello",
    )

import asyncio
asyncio.run(main())