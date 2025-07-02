from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool, RunContextWrapper
from dotenv import load_dotenv
from rich import print
import os

load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY = os.environ.get("GEMINI_API_KEY")

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai"
    )
)

def custom_error_handler(ctx: RunContextWrapper[None], error: Exception) -> str:
    return f"Cannot fulfill this request because {error}"

@function_tool(failure_error_function=None)
def subtract(a: int, b: int) -> int:
    """Subtract two numbers
    Args:
        a: first number
        b: second number
        
    Returns:
        int: The sum of the two numbers.
    """
    if a < b:
        raise ValueError("b cannot be greater than a")  

    return a - b

agent = Agent(
    name="Mathematician", 
    instructions=(
        "You are math expert"
    ), 
    model=model, 
    tools=[subtract],
    tool_use_behavior="stop_on_first_tool"
)

result = Runner.run_sync(starting_agent=agent, input="What is 2-10")
print(result.final_output)

#! Error function ma jo second parameter ha usmy error message as an argunment pass hota ha.
#! or LLM tak wo error message jaye ga jo ham khud is function ma return krengy.
#! agar hamny failure_error_function=None krdia to zahir si bat ha error any pr program crash hojayega q ke koi bh error handling function nhi chalega.
#! or crash hony pr jo error ayega wo UserError ayega agar tool k code ma koi error raise ho to.
#! lekin agar crash model ki waja se ha means k model ki traf se invalid json get hua ha to any waly error ki type ModelBehaviorError hogi 