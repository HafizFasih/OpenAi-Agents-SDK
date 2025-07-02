from agents import InputGuardrail, OutputGuardrail, GuardrailFunctionOutput, Agent

def input_guadrail(ctx, agent, input):
    return GuardrailFunctionOutput(
        output_info=None,
        tripwire_triggered=False,
    )

#! Ham ese bh input guardrails bana skty hain without input_guardrails decorator
my_input_guardrail=InputGuardrail(
    name="input_guadrails",
    guardrail_function=input_guadrail,
)

def output_guadrail(ctx, agent, output):
    return GuardrailFunctionOutput(
        output_info=None,
        tripwire_triggered=False,
    )
#! Ham ese bh output guardrails bana skty hain without output_guardrails decorator
my_output_guardrail=OutputGuardrail(
    name="output_guadrails",
    guardrail_function=output_guadrail,
)

#! It will run without any error
Agent(
    name="Assistant",
    input_guardrails=[my_input_guardrail],
    output_guardrails=[my_output_guardrail],
)