from agents import function_tool, Agent, Runner, enable_verbose_stdout_logging, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, OpenAIResponsesModel
import os
from rich import print
from agents.function_schema import generate_func_documentation, function_schema
#! griffe

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

def error_function(ctx, error):
    print(error)
    return ""

# @function_tool
# def add(a: int, b: int) -> int:
#     """Add two numbers

#     Args:
#         a: first number
#         b: second number
#     """ 
#     return a + b

@function_tool(strict_mode=False)
def get_user_info(name: str, age: int | None = None) -> str:
    """Provides the user details"""
    if age:
        return f"Username is {name} and age is {age}"
    return f"Username is {name}"

# data=generate_func_documentation(
#     func=add,
#     style="google"
# )

# data=function_schema(
#     func=add,
#     use_docstring_info=True
# )
# print(data)
#! google 
#! numpy
#! sphinix

agent=Agent(
    name="Assistant",
    instructions=(
        "You are a helpful assistant, "
        "Username is 'Ahmed' and he is 20 years old"
    ),
    tools=[get_user_info],
    model=model
)
print(agent.tools)

result=Runner.run_sync(
    starting_agent=agent,
    input="Tell me about user"
)

print(result.final_output)

#! LLM ye batyaga k konsa tool call krna ha?
#! Or usky argunments kia hongy

#! Agent Loop 2 
# ?1. LLM ko response gaya, llm ne kaha ye tool call kro, tool call hua, and uska answer bh agya.
# ?2. LLm k pas tool ka answer gaya or then llm ne final_output bana kr dia 

