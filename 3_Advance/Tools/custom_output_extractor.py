from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled, RunResult, ItemHelpers
from dotenv import load_dotenv
from rich import print
import os

set_tracing_disabled(disabled=True)
load_dotenv()

API_KEY=os.environ.get("GEMINI_API_KEY")

model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
)

async def extract_content(run_result: RunResult) -> str:
    last_content = ItemHelpers.text_message_outputs(run_result.new_items)
    return last_content
            
english_agent = Agent(
    name="English Linguistic",
    instructions="You are expert in English language",
)

urdu_agent = Agent(
    name="Urdu Linguistic",
    instructions="You are expert in Urdu language",
    model=model
)

orchestrator_agent=Agent(
    name="orchestrator_agent",
    instructions=(
        "You are a translation agent. You use the tools given to you to translate."
        "If asked for multiple translations, you call the relevant tools."
    ),
    tools=[
        english_agent.as_tool(
            tool_name="translate_to_english",
            tool_description="Translate the user's message to English",
            custom_output_extractor=extract_content
        ),
        urdu_agent.as_tool(
            tool_name="translate_to_urdu",
            tool_description="Translate the user's message to Urdu",
        )
    ],
    model=model,
    tool_use_behavior="stop_on_first_tool"
)

result = Runner.run_sync(
    starting_agent=orchestrator_agent,
    input="'tum kia kar rahy ho', translate it to english"
)

print(result.final_output)

#! jesa ke ham janty hain ke jab koi tool, function_tool decorator se banaya jata ha to usmy ek default error_function hota h jo tool ma error any k case pr run hota h. Backend pr Agent.as_tool() ko bh function_tool k decorator ma wrap kia gaya ha.

#! Yahan par mene english_agent ko koi model provide nhi kia ha to hamy pata ha ka background ma Runner.run chalta ha jismy yehi agent pass hoky phr final output lata ha. Ab ek tareeke se Runner.run or hamary agent dono ma model provide nhi kia gya ha to iska mtlb openai ka default model use kia jayega 'gpt-4o' or agar api key set nhi hogi to kia hoga???

#! default error function chalega jiski waja se code break nhi hoga but zahir se baat ha disered output bh nh ayega.