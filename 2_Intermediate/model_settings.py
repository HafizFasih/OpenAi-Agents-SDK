from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, ModelSettings  
from agents.run import RunConfig  
from dotenv import load_dotenv  
from rich import print  
import os, asyncio

load_dotenv()  
set_tracing_disabled(disabled=True)  

API_KEY = os.environ.get("GEMINI_API_KEY")  
if not API_KEY:
    raise KeyError("Error 405: Does not found an api key")  

model=OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai"
    )
)

model_settings_1 = ModelSettings(
    temperature=0.95,
    top_p=1.0,
    max_tokens=600,
    presence_penalty=0.6,
    tool_choice="none",
    parallel_tool_calls=False,
    truncation="auto",
    include_usage=True
)

model_settings_2 = ModelSettings(
    temperature=0.3,
    top_p=0.8,
    max_tokens=400,
    presence_penalty=0.0,
    tool_choice="auto",
    parallel_tool_calls=True,
    truncation="disabled",
    include_usage=True
)

model_settings_3 = ModelSettings(
    temperature=0.5,
    top_p=1.0,
    max_tokens=250,
    presence_penalty=0.1,
    tool_choice="required",
    parallel_tool_calls=True,
    truncation="auto",
    include_usage=True
)

config_1 = RunConfig(model=model, model_settings=model_settings_1)
config_2 = RunConfig(model=model, model_settings=model_settings_2)
config_3 = RunConfig(model=model, model_settings=model_settings_3)


agent_1 = Agent(
    name="StoryWriter",
    instructions="You are a creative story writer who writes engaging fantasy stories for kids.",
    model=model
)

agent_2 = Agent(
    name="TechTeacher",
    instructions="You are a calm technical assistant that explains programming concepts to beginners in very simple language.",
    model=model
)

agent_3 = Agent(
    name="LogicBot",
    instructions="You are a reasoning expert. Solve logic puzzles step-by-step with explanations.",
    model=model
)


async def main():
    result_1, result_2, result_3 = await asyncio.gather (
        Runner.run(
            starting_agent=agent_1, 
            input="Write a magical story about a rabbit who can fly", 
            run_config=config_1
        ),
        Runner.run(
            starting_agent=agent_2, 
            input="Explain what a Python decorator is with code example", 
            run_config=config_2
        ),
        Runner.run(
            starting_agent=agent_3, 
            input="If all humans are mammals and all mammals are animals, are all humans animals?", run_config=config_3
        )
    )

   
    print("SCENARIO 1 OUTPUT:")
    print(result_1.final_output)
    
    print("SCENARIO 2 OUTPUT:")
    print(result_2.final_output)

    print("SCENARIO 3 OUTPUT:")
    print(result_3.final_output)

asyncio.run(main())

"""
1️⃣ temperature: float | None
🧠 Kya karta hai?
Controls randomness of output.

Value	Behavior
0.0	Har bar same answer (deterministic)
1.0	Random aur creative answer

🧪 Example:
temperature = 0.0 → “What is 2+2?” → Always “4”
temperature = 0.9 → “Write a poem” → Har bar naya unique style

🎯 Use case:
Factual questions → use 0.0
Creative writing → use 0.8-1.0
"""



"""
2️⃣ top_p: float | None
🧠 Kya karta hai?
Ye nucleus sampling hota hai — model sirf top X% most likely tokens me se pick karta hai.

Value	Behavior
1.0	Sab tokens consider karega (no limit)
0.5	Sirf 50% top tokens me se choose karega

🧪 Example:
top_p = 0.5 → less randomness, more focused answer
top_p = 1.0 → full creative space

🎯 Use case:
temperature jaisa hi hai. Dono milke kaam karte hain.
"""


#! NOT WORKING
"""
3️⃣ frequency_penalty: float | None
🧠 Kya karta hai?
Jo word bar bar repeat ho raha hai us par penalty lagata hai.

Value	Effect
0.0	No penalty
1.0	Strong penalty (less repetition)

🧪 Example:
prompt: “Describe love”
frequency_penalty = 0.0 → “Love is love is love...”
frequency_penalty = 1.0 → “Love is a deep emotion that binds...”

🎯 Use case:
To avoid repetition in generated text.
"""

"""
4️⃣ presence_penalty: float | None
🧠 Kya karta hai?
Model ko naye topics explore karne ke liye push karta hai.

Value	Behavior
0.0	No extra encouragement
1.0	Strong push for new topics

🧪 Example:
If model ne “technology” pe likh diya, to:
presence_penalty = 1.0 → Next time “nature”, “art”, “history” aayega
presence_penalty = 0.0 → Wapas “technology” likh sakta hai

🎯 Use case:
Useful in brainstorming, idea generation.
"""

"""
5️⃣ tool_choice: "auto" | "required" | "none" | str | None
🧠 Kya karta hai?
Decide karta hai model tool use kare ya nahi.

Option	Behavior
"auto"	Model decide kare
"required"	Tool zaroor use ho
"none"	Bilkul tool use na ho

🧪 Example:
“auto” → agar model ko lage weather tool chahiye, use karega.
“required” → tool use forcefully kare.
“none” → tool kabhi use na kare.

🎯 Use case:
When using tools like calculator, weather API, etc.
"""


"""
6️⃣ parallel_tool_calls: bool | None
🧠 Kya karta hai?
Model ek se zyada tool ek hi time pe call kar sakta hai ya nahi.

Value	Effect
True	Multiple tools ek saath
False	Ek time pe ek tool

🧪 Example:
Aapka agent 3 tools use karta hai:
WeatherTool
CalendarTool
FlightTool
parallel_tool_calls = True → sab call ho sakte hain ek saath

🎯 Use case:
Jab speed important ho — e.g. voice assistants
"""



"""
7️⃣ truncation: "auto" | "disabled" | None
🧠 Kya karta hai?
Agar context (prompt + history) lamba ho jaye to kaise handle kare?

Option	Behavior
"auto"	Older messages truncate ho jayenge
"disabled"	Truncation bilkul na ho (may fail)

🎯 Use case:
Multi-turn conversations me long context hone par
"""



"""
8️⃣ max_tokens: int | None
🧠 Kya karta hai?
Kitne tokens tak model output de sakta hai — limit.

🧪 Example:
max_tokens = 10 → Sirf 10 token ka reply
max_tokens = 1000 → Lamba reply allowed

🎯 Use case:
Short summaries → 50
Essay-style content → 500+
"""



"""
9️⃣ reasoning: Reasoning | None
🧠 Kya karta hai?
OpenAI ke “reasoning” type models ke liye config deta hai — like intermediate steps, chain-of-thought, etc.

🎯 Use case:
Math, logic, or deep multi-step reasoning required ho.
"""


#! NOT WORKING
"""
🔟 metadata: dict[str, str] | None
🧠 Kya karta hai?
Custom info attach karta hai request ke sath — tracking, user ID, etc.

🧪 Example:
metadata = {"user_id": "abc123", "session_id": "xyz987"}

🎯 Use case:
Analytics, debugging, A/B testing, logging
"""



#! NOT WORKING
"""
🔢 store: bool | None
🧠 Kya karta hai?
Response ko save kare ya nahi — future audit ya feedback ke liye.

Value	Behavior
True	Save response
False	Don't save

🎯 Use case:
Production logging
Privacy-sensitive flows
"""



"""
🔣 include_usage: bool | None
🧠 Kya karta hai?
Model ke response me usage info (token counts) add kare ya nahi.

🎯 Use case:
Cost monitoring
Token budgeting
"""



"""
🔄 extra_query, extra_body, extra_headers
🧠 Ye 3 fields extra HTTP request ke parts add karte hain:

extra_query → URL ke ?key=value wale fields
extra_body → POST body me extra fields
extra_headers → Authorization, tracking, etc.

🎯 Use case:
Custom API integrations, advanced config, beta testing.
"""