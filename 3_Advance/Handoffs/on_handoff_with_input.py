from agents import (
    Agent,
    RunConfig, 
    RunContextWrapper, 
    Runner, 
    enable_verbose_stdout_logging, 
    set_tracing_disabled, 
    OpenAIChatCompletionsModel,
)
from agents.handoffs import THandoffInput, Handoff, handoff, OnHandoffWithInput, OnHandoffWithoutInput
from openai import AsyncOpenAI
from pydantic import BaseModel
from rich import print
import asyncio
import os

set_tracing_disabled(disabled=True)

API_KEY = os.environ.get("GEMINI_API_KEY")

config = RunConfig(
    model=OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=AsyncOpenAI(
            api_key=API_KEY,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai"
        )
    )
)

class MyInput(BaseModel):
    question: str
    related_with: str


agent = Agent(
    name="Mathematician",
    instructions="You are good at maths.",
    handoff_description="An expert math teacher"
)

def handoff_function(ctx: RunContextWrapper, input: MyInput):
    print(
        f"[green]Handoff triggered![/green]\nQuestion: {input.question}\nRelated With: {input.related_with}"
    )

handoff_agent = handoff(
    agent=agent,
    on_handoff=handoff_function,
    input_type=MyInput
)

#! MANUALLY INVVOKED HANDOFF
async def invoke_manually():
    result = await handoff_agent.on_invoke_handoff(
        ctx=RunContextWrapper(context=None),
        input_json="{\"question\":\"What is the derivative of x^3\",\"related_with\":\"calculus\"}"
    )
    print(f"[blue]Returned agent:[/blue] {result}")

asyncio.run(invoke_manually())

#! NOW INVOKING HANDOFF BY AGENTS
async def invoke_by_agents():
    traige_agent=Agent(
        name="Triage Agent",
        instructions=(
            "You are a triage agent which handofss to Mathematician Agent if required."
        ),
        handoffs=[
            handoff_agent
        ]
    )
    result = await Runner.run(
        starting_agent=traige_agent,
        input="What is the derivative of x^3",
        run_config=config
    )
    print(result.final_output)

asyncio.run(invoke_by_agents())

#! Handoff bilkul tool call ki trah ha bilkul same hi pattern pr treat kia jata ha isko bh.

#! Handoffs krty hue LLM agent ko just do cheezien batata ha similar to tool calling, phela 'name' or dusra arguments.

#! Normally arguments ma empty dict aati hai.

#! lekin agar ham 'input_type' ko define krdy to phr khali dict nhi aati blky us type ka data ata ha jo hamny input_type ma dia ho.

#! Agar on_handoff function 2 parameter wala banaya ha e.g(ctx: RunContextWrapper, input: MyInput) to according to overlaad 'input_type' ko bh define krna parega 'UserError' wrna error ayega 

#! Or Agar on_handoff function ma sirf ek hi parameter ha to phr input_type define nhi krni hogi agar krdi to phr se 'UserError' ayega
