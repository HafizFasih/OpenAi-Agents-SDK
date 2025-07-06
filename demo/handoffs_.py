from agents import  AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, RunConfig, Agent, handoff, Handoff, HandoffInputData, Runner, enable_verbose_stdout_logging, RunContextWrapper
from agents.extensions.handoff_filters import remove_all_tools
import os
from rich import print
from typing import Callable
from pydantic import BaseModel

# def func(a: int, b: str) -> str:
# Callable[[int, str], str]

# enable_verbose_stdout_logging()
set_tracing_disabled(True)

API_KEY = os.environ.get("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

model = OpenAIChatCompletionsModel(
    openai_client=client,
    model="gemini-2.0-flash",
)

config = RunConfig(
    model=model,
)


agent=Agent(
    name="Mathematician",
    instructions="You are a good at maths",
)

#? Callable[[HandoffInputData], HandoffInputData]
def input_filter(data: HandoffInputData) -> HandoffInputData:
    print("Input filter function executed.")
    return "Hello World"


class MyInputType(BaseModel):
    user_query: str

# def on_handoff(wrapper: RunContextWrapper):
#     print("On Handoff function executed")

def on_handoff(wrapper: RunContextWrapper, input_type: MyInputType):
    print(input_type)
    print("On Handoff function executed")

#! transfer_to_my_agent
handoff_maths_agent=handoff(
    agent=agent,
    tool_description_override="hello",
    # on_handoff=on_handoff,
    # input_type=MyInputType,
    input_filter=input_filter
)

#! Jab input_type define kren to on_handoff hona lazmi ha 
#! on_handoff wo bh 2 paramters wala
#! 2 paramter wala isliye q ke jo arguments LLM dega wo on_handoff function k second paramter ma accept hongy

# print(agent.name)
# print(handoff_maths_agent)


triage_agent = Agent(
    name="Triage agent",
    instructions=(
        "If they ask about maths, you **MUST** handoff to the maths agent."
    ),
    handoffs=[
        handoff_maths_agent
    ],
    model=model
)

result = Runner.run_sync(
    starting_agent=triage_agent,
    input="What is the sum of 10 and 32",
    run_config=config
)

print(result.final_output)

#! Normally jo ham tools banaty hain jese ke get_weather ka
#! To wo kia karega city name argunment ma accept krega or ek str return krega.


#! In case of handoff SDK ne khud ek tool bana dia ha jiska defaultname transfer_to_(agent_name) hoga
#! Wo tool jab call hoga to wo ek agent return krega -> Agent


#! Agar hamary pas Agent A ha uski handoff list ma Agent B ha with input_filter
#! Additionaly run_config k andr bh ek input_filter

#? To sawal ye banta ha k konsa run hoga??