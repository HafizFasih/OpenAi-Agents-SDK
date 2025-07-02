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

# --- EXAMPLE 1: LOW TOP_P (Focused & Precise) ---
print("--- Example 1: Low top_p (0.0) ---")

# Agent definition for low top_p.
# Instructions: Model ko precise aur factual rehne ki hidayat di gayi hai.
# Input: Ek specific factual question.
# top_p (0.0): Yeh sabse kam top_p hai, matlab model sirf sabse
# probable word ko choose karega (similar to greedy decoding). Output bahut focused aur direct hoga.
# Purpose: Factual questions, summaries, code generation, jahan consistency zaruri ho.
agent_low_p = Agent(
    name="FactChecker",
    instructions="You are a highly accurate factual assistant. Provide concise and direct answers without embellishment.",
    model_settings=ModelSettings(
        top_p=0.0 # <--- Yahan top_p set kiya gaya hai.
    )
)

result_low_p = Runner.run_sync(
    starting_agent=agent_low_p,
    input="What is the capital of France?",
    run_config=config
)

print(f"Agent Output (Low Top_P): {result_low_p.final_output}")
print("\n" + "="*50 + "\n") # Separator for clarity

# --- EXAMPLE 2: HIGH TOP_P (Creative & Diverse) ---
print("--- Example 2: High top_p (0.9) ---")

# Agent definition for high top_p.
# Instructions: Model ko creative aur imaginative banane ki hidayat di gayi hai.
# Input: Ek open-ended creative prompt.
# top_p (0.9): Yeh high top_p hai. Model un words mein se choose karega jinki cumulative probability
# 0.9 tak pahunchti hai. Isse zyada diversity aur randomness allow hogi.
# Har baar run karne par output thoda mukhtalif ho sakta hai.
# Purpose: Creative writing, brainstorming ideas, story generation, poetry, jahan variability chahiye.
agent_high_p = Agent(
    name="Storyteller",
    instructions="You are a whimsical and imaginative storyteller. Craft vivid and original narratives.",
    model_settings=ModelSettings(
        top_p=0.9 # <--- Yahan top_p set kiya gaya hai.
    )
)

result_high_p = Runner.run_sync(
    starting_agent=agent_high_p,
    input="Write a short, fantastical tale about a talking teapot that grants wishes.",
    run_config=config
)

print(f"Agent Output (High Top_P): {result_high_p.final_output}")
print("\n" + "="*50 + "\n") # Separator for clarity

# --- EXAMPLE 3: MEDIUM TOP_P (Balanced Diversity) ---
print("--- Example 3: Medium top_p (0.7) ---")

# Agent definition for medium top_p.
# Instructions: Model ko helpful aur imaginative rehne ki hidayat di gayi hai.
# Input: Ek prompt jahan kai mukhtalif lekin munasib jawab ho sakte hain.
# top_p (0.7): Yeh ek intermediate top_p value hai. Model un words mein se agla word choose karega
# jinki cumulative probability 0.7 tak ho. Isse model ko kaafi saare achhe options milenge
# jinmein se woh chun sakta hai, jisse output mein munasib diversity aayegi
# jabke woh topic se bhatkega nahi.
# Purpose: Brainstorming related ideas, creating diverse lists, generating variations on a theme.
agent_medium_p = Agent(
    name="IdeaGenerator",
    instructions="You are a creative brainstorming assistant. Provide a variety of relevant and distinct ideas.",
    model_settings=ModelSettings(
        top_p=0.7 # <--- Yahan top_p set kiya gaya hai.
    )
)

result_medium_p = Runner.run_sync(
    starting_agent=agent_medium_p,
    input="Suggest 5 unique and eco-friendly ways to reuse old plastic bottles.",
    run_config=config
)

print(f"Agent Output (Medium Top_P): {result_medium_p.final_output}")
print("\n" + "="*50 + "\n") # Separator for clarity


# --- TOP_P AUR USKA PURPOSE (Comments mein Definition) ---

# Top_P (Nucleus Sampling):
# Machine Learning aur particularly Large Language Models (LLMs) mein 'top_p'
# (jise nucleus sampling bhi kehte hain) ek hyperparameter hai jo model ki output
# randomness (creativity) ko control karta hai.
# Yeh agle word ke chunav ke liye ek threshold set karta hai. Model sirf un words
# mein se choose karta hai jinki cumulative probability is 'top_p' value tak
# pahunchti hai. For example, agar top_p = 0.9, toh model sirf un top words mein
# se agla word choose karega jinki combined probability 90% tak ho.

# Purpose:
# 1. Kam Top_P (e.g., 0.0 - 0.2):
#    - Model zyada 'safe', predictable, aur deterministic output dega.
#    - Yeh sabse zyada probable words ko select karne ki taraf zyada jhukega,
#      kyunki kumulative probability bahut jaldi top_p value tak pahunch jaati hai.
#    - Hasilat: Factual questions, summarization, code generation jahan consistency
#      aur accuracy paramount ho. Output har run par lagbhag ek jaisa hoga.

# 2. Zyada Top_P (e.7 - 1.0):
#    - Model zyada creative, diverse, aur unexpected output dega.
#    - Yeh ek wide range of words ko consider karega, jisse kam probable words ko
#      bhi chunne ki flexibility milegi (jab tak unki cumulative probability top_p
#      ko cross na kare).
#    - Hasilat: Creative writing, brainstorming, poetry, story generation jahan naya-pan
#      aur alag-alag ideas ki zarurat ho. Output har run par mukhtalif ho sakta hai.

# 'top_p' bhi 'temperature' ki tarah predictability aur creativity ke darmiyan trade-off
# ko control karta hai, lekin ek mukhtalif tareeqe se. Jahan temperature probabilities
# ko 'sharpen' karta hai, top_p words ke ek 'subset' ko select karta hai.
