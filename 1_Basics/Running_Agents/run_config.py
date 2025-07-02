# type: ignore
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, ModelSettings
from agents.run import RunConfig
from dotenv import load_dotenv
import os

load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY = os.environ.get("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=client
)

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
)

config = RunConfig(
    tracing_disabled=True,
    model=model,
    model_provider=client,
    model_settings=ModelSettings(
        temperature=0.5,
    ),
)

result = Runner.run_sync(
    starting_agent=agent,
    input="Who is the founder of USA",
    run_config=config
)

print(f"FIRST OUTPUT\n {result.final_output}")


new_input = result.to_input_list()
result = Runner.run_sync(agent, new_input, run_config=config)
print(f"SECOND OUTPUT\n {result.final_output}")

#? RunConfig(
#! model: 
#*   Allows setting a global LLM model to use, irrespective of what model each Agent has.

#! model_provider: 
#*   A model provider for looking up model names, which defaults to OpenAI.

#! model_settings: 
#*   Overrides agent-specific settings. For example, you can set a global temperature or top_p.

#! input_guardrails, output_guardrails: 
#*   A list of input or output guardrails to include on all runs.

#! handoff_input_filter: 
#*   A global input filter to apply to all handoffs, if the handoff doesn't already have one. The input filter allows you to edit the inputs that are sent to the new agent. See the documentation in Handoff.input_filter for more details.

#! tracing_disabled: 
#*   Allows you to disable tracing for the entire run.

#! trace_include_sensitive_data: 
#*   Configures whether traces will include potentially sensitive data, such as LLM and tool call inputs/outputs.

#! workflow_name, trace_id, group_id: 
#*   Sets the tracing workflow name, trace ID and trace group ID for the run. We recommend at least setting workflow_name. The group ID is an optional field that lets you link traces across multiple runs.

#! trace_metadata: 
#*   Metadata to include on all traces.

#? )