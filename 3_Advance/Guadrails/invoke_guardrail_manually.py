from agents import input_guardrail, GuardrailFunctionOutput, Agent, RunContextWrapper, output_guardrail
from rich import print
import asyncio

#! Simple sa ek output guadrail ha jo OutputGuardrail ka instance return krega
@input_guardrail
def my_input_guardrail(ctx, agent, input):
    return GuardrailFunctionOutput(
        output_info=None,
        tripwire_triggered=False
    )

#! Simple sa input guadrail ha jo InputGuardrail ka instance return krena
@output_guardrail
def my_output_guardrail(ctx, agent, output):
    return GuardrailFunctionOutput(
        output_info=None,
        tripwire_triggered=False
    )

async def main():
    #! Note: Guadrails ko Agent khud .run se chalata ha (chahy input guadrail ho ya output guadrail)
    input_guadrail_result = await my_input_guardrail.run(
        context=RunContextWrapper(context=None),
        agent=Agent(name="Input Assistant"),
        input="nothing"
    )
    #! Output: instance of InputGuadrailResult (2 properties) 
    print(input_guadrail_result)
    
    output_guadrail_result = await my_output_guardrail.run(
        context=RunContextWrapper(context=None),
        agent=Agent(name="Output Assistant"),
        agent_output="nothing"
    )

    #! Output: instance of OutputGuadrailResult (4 properties) 
    print(output_guadrail_result)


asyncio.run(main())

#! Agent khud is tarah se chalata ha input and output guadrails ko
#! source code: _run_impl file ma ek class ha RunImpl usme methods hain 'run_single_input_guardrail' and 'run_single_output_guardrail', wahan iska code likha hua ha

#! In methods ko Runner._run_input_guardrails and Runner._run_output_guardrails ma call kia jata task bana kr