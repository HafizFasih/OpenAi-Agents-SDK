from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, ModelSettings, RunConfig
from dotenv import load_dotenv
from rich import print
import os

load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY = os.environ.get("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

model = OpenAIChatCompletionsModel(
    openai_client=client,
    model="gemini-1.5-flash",
)

agent_model_settings = ModelSettings(
    tool_choice="auto"
)

runner_model_settings = ModelSettings(
    tool_choice="required"
) 

run_config = RunConfig(
    model=model,
    model_settings=runner_model_settings
)

agent = Agent(
    name="Mathematician", 
    instructions="You are a helpful assistant", 
    model=model,
    model_settings=agent_model_settings
)

result = Runner.run_sync(
    starting_agent=agent, 
    input="What is the capital of Pakistan",
    run_config=run_config

)

print(result.final_output)

#! Runner ki model settings consider ki jayegi jab ky agent ki model setting ko neglect krdia jayega
#! In case agar just agent ki model settings defined ho or runner ki na ho to zahir ha k agent ki model settings hi follow hogi

#? Iska proof hamy model settings k resolve method se milta ha
agent.model_settings.resolve(
    run_config.model_settings
) 

#? Backend ma ye code likha ha, agar run_config ki koi modelsetting define nhi hogi to zahir ha agent ki modelsetting consider ki jayegi
