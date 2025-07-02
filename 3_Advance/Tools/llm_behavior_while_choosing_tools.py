from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
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

#! Mene name 'subtract' dia ha jabky function ki description ma add k bary ma likha ha or return ma bh a + b return ho raha ha
@function_tool(name_override="subtract") 
def add(a: int, b: int) -> str:
    """Add two numbers
    Args:
        a: first number
        b: second number
        
    Returns:
        int: The sum of the two numbers.
    """
    return f"The sum of {a} and {b} is {a+b}"

#! Mene name 'add' dia ha jabky function ki description ma subtract k bary ma likha ha or return ma bh a - b return ho raha ha
@function_tool(name_override="add") 
def subtract(a: int, b: int) -> str: 
    """Subtract two numbers
    Args:
        a: first number
        b: second number
        
    Returns:
        int: The difference of the two numbers.
    """
    return f"The difference of {a} and {b} is {a-b}"

agent = Agent(
    name="Mathematician", 
    instructions=(
        "You are math expert"
    ), 
    model=model, 
    tools=[add, subtract],
    tool_use_behavior="stop_on_first_tool"
)

input_for_sum = "What is 10 + 43?"
input_for_difference = "What is 40 - 24?"

result = Runner.run_sync(
    starting_agent=agent, 
    input=input_for_difference
)

print(result.final_output)


#! Jesa k uper sab clear ha k tool name bht important hota ha. LLM tool name dekh kr decide krta ha k ussy kia karna chhaye.

#! Sum k case ma wo subtract kr raha ha or subtract k case ma sum sirf issi waja se k mene tool name apas ma badal diye.

#! Ek or cheez ghor krny ki ha k sirf tool names badly gaye hain description wagera sab orignal ha phr bh LLM name ko ziyada preference de raha ha or tool call kr raha ha