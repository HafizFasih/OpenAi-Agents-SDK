from agents import (
    Agent, 
    Runner,
    RunHooks, 
    AgentHooks, 
    function_tool, 
    ModelSettings, 
    input_guardrail, 
    output_guardrail, 
    AgentOutputSchema, 
    set_tracing_disabled,
    AgentOutputSchemaBase,
    GuardrailFunctionOutput, 
    ToolsToFinalOutputResult, 
    OpenAIChatCompletionsModel, 
    enable_verbose_stdout_logging,
    RunResult
)
from pydantic import BaseModel
from dotenv import load_dotenv
from rich import print

set_tracing_disabled()
load_dotenv()
print(Agent(name="Assistant"))

fiction_story_expert=Agent(

)

agent=Agent(
    name="Assistant",
    instructions="You are a helpfull assistant",
    # handoff_description="blah blah blah",
    # handoffs=[],
    # hooks=,
    # input_guardrails=,
    # model=,
    # model_settings=,
    # output_guardrails=,
    # reset_tool_choice=,
    # output_type=,
    # tool_use_behavior=,
    # tools=
)
