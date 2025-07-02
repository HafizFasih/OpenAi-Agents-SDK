from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, RunConfig, ModelSettings
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

# -- RunConfig setup (will remain mostly same) --
config = RunConfig(
    model=OpenAIChatCompletionsModel(
        model="gemini-2.0-flash", # Aapka model, jaise Gemini 2.0 Flash
        openai_client=client
    )
)

# --- EXAMPLE 1: LOW TEMPERATURE (Focused & Precise) ---
print("--- Example 1: Low Temperature (0.0) ---")

# Agent definition for low temperature.
# Instructions: Model ko precise aur factual rehne ki hidayat di gayi hai.
# Input: Ek specific factual question.
# Temperature (0.0): Yeh sabse kam temperature hai, matlab model sirf sabse
# probable words choose karega. Output bahut focused aur direct hoga.
# Purpose: Factual questions, summaries, code generation, jahan consistency zaruri ho.
agent_low_temp = Agent(
    name="FactChecker",
    instructions="You are a highly accurate factual assistant. Provide concise and direct answers without embellishment.",
    model_settings=ModelSettings(
        temperature=0.0 # <--- Yahan temperature set kiya gaya hai.
    )
)

result_low_temp = Runner.run_sync(
    starting_agent=agent_low_temp,
    input="What is the capital of France?",
    run_config=config
)

print(f"Agent Output (Low Temp): {result_low_temp.final_output}")
print("\n" + "="*50 + "\n") # Separator for clarity

# --- EXAMPLE 2: HIGH TEMPERATURE (Creative & Diverse) ---
print("--- Example 2: High Temperature (0.9) ---")

# Agent definition for high temperature.
# Instructions: Model ko creative aur imaginative banane ki hidayat di gayi hai.
# Input: Ek open-ended creative prompt.
# Temperature (0.9): Yeh high temperature hai, model ko zyada diversity aur randomness
# allow karega word choice mein. Output zyada creative, naya aur unexpected ho sakta hai.
# Har baar run karne par output thoda mukhtalif ho sakta hai.
# Purpose: Creative writing, brainstorming ideas, story generation, poetry, jahan variability chahiye.
agent_high_temp = Agent(
    name="Storyteller",
    instructions="You are a whimsical and imaginative storyteller. Craft vivid and original narratives.",
    model_settings=ModelSettings(
        temperature=0.9 # <--- Yahan temperature set kiya gaya hai.
    )
)

result_high_temp = Runner.run_sync(
    starting_agent=agent_high_temp,
    input="Write a short, fantastical tale about a talking teapot that grants wishes.",
    run_config=config
)

print(f"Agent Output (High Temp): {result_high_temp.final_output}")
print("\n" + "="*50 + "\n") # Separator for clarity


# --- TEMPERATURE AUR USKA PURPOSE (Comments mein Definition) ---

# Temperature:
# Machine Learning aur particularly Large Language Models (LLMs) mein 'temperature'
# ek hyperparameter hai jo model ki output randomness (creativity) ko control karta hai.
# Yeh probability distribution ki 'sharpness' ko adjust karta hai, jisse agle word
# ke chunav (selection) par asar padta hai.

# Purpose:
# 1. Kam Temperature (e.g., 0.0 - 0.2):
#    - Model zyada 'safe', predictable, aur deterministic output dega.
#    - Yeh sabse zyada probable (yaani, jo model ko sabse zyada 'correct' lagta hai)
#      word ko select karne ki taraf zyada jhukega.
#    - Hasilat: Factual questions, summarization, code generation jahan consistency
#      aur accuracy paramount ho. Output har run par lagbhag ek jaisa hoga.

# 2. Zyada Temperature (e.g., 0.7 - 1.0+):
#    - Model zyada creative, diverse, aur unexpected output dega.
#    - Yeh sirf sabse probable words tak mehdood nahi rahega, balki kam probable words
#      ko bhi chunne ki flexibility rakhega.
#    - Hasilat: Creative writing, brainstorming, poetry, story generation jahan naya-pan
#      aur alag-alag ideas ki zarurat ho. Output har run par mukhtalif ho sakta hai.

# 'temperature' basically trade-off hai predictability aur creativity ke darmiyan.
# Isko adjust kar ke aap model ke behavior ko control kar sakte hain ke woh kitna
# 'safe' aur kitna 'experimental' output de.
