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

# --- EXAMPLE 1: LOW PRESENCE_PENALTY (Allows Repetition, Detailed Exploration) ---
print("--- Example 1: Low presence_penalty (0.0) ---")

# Agent definition for low presence_penalty.
# Instructions: Model ko kisi ek topic par tafseeli aur gehrai se baat karne ki hidayat.
# Input: Ek scientific ya complex concept ko detail mein samjhane ka prompt.
# presence_penalty (0.0): Yeh sabse kam penalty hai, matlab model ko woh alfaaz ya
# concepts dohrane ki azadi hogi jo usne pehle hi mention kar diye hain.
# Yeh tab behtar hai jab aapko kisi topic par mukammal aur tafseeli jawab chahiye,
# jahan key terms ka dohrana zaruri ho.
# Purpose: Deep dives, comprehensive explanations, where natural repetition of terms is needed.
agent_low_pp = Agent(
    name="DeepExplainer",
    instructions="You are an expert who provides thorough and detailed explanations on any given topic. Do not shy away from re-emphasizing key concepts for clarity.",
    model_settings=ModelSettings(
        presence_penalty=0.0 # <--- Yahan presence_penalty set kiya gaya hai.
    )
)

result_low_pp = Runner.run_sync(
    starting_agent=agent_low_pp,
    input="Explain the carbon cycle in detail, including its main components and processes.",
    run_config=config
)

print(f"Agent Output (Low Presence Penalty): {result_low_pp.final_output}")
print("\n" + "="*50 + "\n") # Separator for clarity

# --- EXAMPLE 2: HIGH PRESENCE_PENALTY (Discourages Repetition, Encourages Diversity) ---
print("--- Example 2: High presence_penalty (2.0) ---")

# Agent definition for high presence_penalty.
# Instructions: Model ko mukhtalif alfaaz aur concepts istemal karne ki hidayat.
# Input: Ek aisa prompt jo mukhtalif ya mutabadil tareeqon se jawab mangta hai.
# presence_penalty (2.0): Yeh highest penalty hai. Model sakhti se koshish karega
# ke jo alfaaz ya concepts usne pehle hi istemal kar liye hain, unko dobara na dohraye.
# Isse output mein vocabulary diversity aur naye ideas shamil honge.
# Purpose: Brainstorming unique ideas, creative writing with varied vocabulary, avoiding jargon.
agent_high_pp = Agent(
    name="InnovativeThinker",
    instructions="You are a highly creative and original thinker. Express ideas using diverse vocabulary and avoid reiterating previously mentioned concepts.",
    model_settings=ModelSettings(
        presence_penalty=2.0 # <--- Yahan presence_penalty set kiya gaya hai.
    )
)

result_high_pp = Runner.run_sync(
    starting_agent=agent_high_pp,
    input="Describe the feeling of joy without using the words 'happy', 'glee', 'elation', or 'delight'.",
    run_config=config
)

print(f"Agent Output (High Presence Penalty): {result_high_pp.final_output}")
print("\n" + "="*50 + "\n") # Separator for clarity

# --- EXAMPLE 3: MEDIUM PRESENCE_PENALTY (Balanced Approach) ---
print("--- Example 3: Medium presence_penalty (0.7) ---")

# Agent definition for medium presence_penalty.
# Instructions: Model ko ek topic par baat karne ki hidayat, lekin munasib diversity ke saath.
# Input: Ek prompt jo thodi si creativity aur variation expect karta hai.
# presence_penalty (0.7): Yeh ek darmiyani penalty hai. Model thodi bohot repetition ko
# tolerate karega, lekin zyada dohrane se gurez karega. Natija balanced hoga, jahan
# relevant ideas dohrae bhi ja sakte hain lekin naya-pan bhi maujood hoga.
# Purpose: Summaries with varied phrasing, discussions that require balanced repetition and novelty.
agent_medium_pp = Agent(
    name="BalancedCommunicator",
    instructions="You are a clear and concise communicator. Explain topics thoroughly while maintaining diverse phrasing.",
    model_settings=ModelSettings(
        presence_penalty=0.7 # <--- Yahan presence_penalty set kiya gaya hai.
    )
)

result_medium_pp = Runner.run_sync(
    starting_agent=agent_medium_pp,
    input="Discuss three key benefits of outdoor exercise, focusing on distinct aspects for each.",
    run_config=config
)

print(f"Agent Output (Medium Presence Penalty): {result_medium_pp.final_output}")
print("\n" + "="*50 + "\n") # Separator for clarity


# --- PRESENCE_PENALTY AUR USKA PURPOSE (Comments mein Definition) ---

# Presence_Penalty:
# Large Language Models (LLMs) mein 'presence_penalty' ek parameter hai jo model ko
# un tokens (words ya word parts) ko dohrane se rokta hai jo output mein pehle hi
# aa chuke hain. Iska maqsad output mein naya-pan (novelty) aur diversity lana hai.
# Yeh parameter -2.0 se 2.0 tak hota hai.

# Purpose:
# 1. Kam Presence_Penalty (e.g., 0.0, ya negative values):
#    - Model ko pehle se maujood topics ya alfaaz ko dohrane se kam roka jaata hai.
#    - Negative values (jaise -2.0) repetition ko encourage kar sakti hain.
#    - Hasilat: Tafseeli aur gehre jawab jahan ek hi concept ya key term ko baar baar
#      samjhana zaruri ho. Isse cohesive aur thorough explanations mil sakti hain,
#      lekin kuch redundancy bhi aa sakti hai.
#    - Misal: Scientific explanations, technical documentation, detailed summaries.

# 2. Zyada Presence_Penalty (e.g., 1.0 - 2.0):
#    - Model ko pehle se maujood topics ya alfaaz ko dohrane par sakhti se saza (penalty) milti hai.
#    - Iska matlab hai ke model koshish karega ke har baar naye alfaaz aur concepts
#      istemal kare.
#    - Hasilat: Zyada diverse, original, aur kam redundant output. Yeh model ko
#      "out-of-the-box" sochne par majboor karta hai.
#    - Misal: Creative writing (jahan variation chahiye), brainstorming unique ideas,
#      list generation (jahan items distinct hon), essay writing (jahan repetition
#      avoid karni ho).

# Presence_Penalty ka istemal output ki redundancy ko control karne aur usmein
# diversity badhane ke liye kiya jaata hai. Yeh 'frequency_penalty' se mukhtalif hai
# kyunki 'frequency_penalty' sirf token ki frequency ko dekhta hai, jabke
# 'presence_penalty' yeh dekhta hai ke woh token output mein maujood hai ya nahi,
# bhale hi woh ek hi baar kyun na aaya ho.
