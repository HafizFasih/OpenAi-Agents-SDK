from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
from dotenv import load_dotenv
import os

load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise KeyError("Error 405: Does not found an api key") 

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client,
)

agent = Agent(name="Assistant", instructions="You are a helpful assistant", model=model)
result = Runner.run_sync(agent, "Hello")

print(result.raw_responses)
#!OUTPUT:
#? [ModelResponse(output=[ResponseOutputMessage(id='__fake_id__', content=[ResponseOutputText(annotations=[], text='Hello! How can I help you today?\n', type='output_text')], role='assistant', status='completed', type='message')], usage=Usage(requests=1, input_tokens=6, input_tokens_details=InputTokensDetails(cached_tokens=0), output_tokens=10, output_tokens_details=OutputTokensDetails(reasoning_tokens=0), total_tokens=16), response_id=None)]