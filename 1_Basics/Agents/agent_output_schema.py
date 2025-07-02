from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled, AgentOutputSchema
from dotenv import load_dotenv
from pydantic import BaseModel
import os

set_tracing_disabled(disabled=True)
load_dotenv()

API_KEY = os.environ.get("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

model = OpenAIChatCompletionsModel(
    openai_client=client,
    model="gemini-1.5-flash"
)

class MovieReview(BaseModel):
    is_positive: bool
    genre: str
    summary: str

agent = Agent(
    name="MovieAnalyzer",
    instructions="Analyze the movie review and determine if it's positive, identify the genre, and provide a brief summary. Include any additional details like sentiment score or related genres if relevant.",
    output_type=AgentOutputSchema(MovieReview, strict_json_schema=False),
    model=model,
)

result = Runner.run_sync(
    starting_agent=agent,
    input="I loved the thrilling action scenes in this sci-fi blockbuster! The plot kept me on edge.",
)

print(result.final_output)