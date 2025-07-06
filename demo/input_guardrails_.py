from agents import input_guardrail, Agent, Runner, set_tracing_disabled, AsyncOpenAI, RunConfig, OpenAIChatCompletionsModel, RunContextWrapper, TResponseInputItem, GuardrailFunctionOutput, InputGuardrail, InputGuardrailTripwireTriggered
import os
from rich import print
from typing import Callable, Awaitable

Callable[[str, int, bool], str]

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

print(my_guardrail_func_1)

agent=Agent(
    name="Assistant",
    input_guardrails=[my_guardrail_func_1]
)
# #! Second Method
# def my_guardrail_func_2(
#         ctx: RunContextWrapper, 
#         agent: Agent, 
#         input: str | list[TResponseInputItem],
#     ) -> GuardrailFunctionOutput:
    
#     print("Guardrail function is executed")

#     return GuardrailFunctionOutput(
#         output_info=None,
#         tripwire_triggered=True
#     )

# custom_guardrail=InputGuardrail(
#     guardrail_function=my_guardrail_func_2,
#     name="guardrail"
# )

# agent=Agent(
#     name="Assistant",
#     instructions="You are a helpfull assistant.",
#     input_guardrails=[my_guardrail_func_1]
# )
# try:
#     result = Runner.run_sync(
#         starting_agent=agent,
#         input="What is the capital of Pakistan",
#         run_config=config
#     )
#     print(result.final_output)
# except InputGuardrailTripwireTriggered as e:
#     print(e.guardrail_result.output)
