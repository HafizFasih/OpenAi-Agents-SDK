from agents.handoffs import handoff
from agents import Agent
from agents.util import _transforms

agent_name = "AI Expert"

#! default tool_name = lower(transfer_to_[agent ka name])
handoff_agent_with_default_name=handoff(
    agent=Agent(name=agent_name)
)
#! Backend pr ye function use ho raha hota ha
#? Output transfer_to_ai_expert
_transforms.transform_string_function_style(f"transfer_to_{agent_name}") 

print(handoff_agent_with_default_name.tool_name)
#? Output: transfer_to_ai_expert

#! Agent ka naam kuch bhi ho tool_nam_override se override krdia jayega
handoff_agent_with_name=handoff(
    agent=Agent(name=agent_name),
    tool_name_override="ai_expert"
)
print(handoff_agent_with_name.tool_name)

#! Invalid name
handoff_agent_invalid_name=handoff(
    agent=Agent(name=agent_name),
    tool_name_override="name with spaces"
)
print(handoff_agent_invalid_name.tool_name)

#! tool_name ek valid function name hona chahye wrna error ayega
#! or ye error tab ata ha jab LLM k paas request jati ha or LLM response krta ha (OpenAIChatCompletionModel)
#? IMPORTANT: Same case description k liye bh ha 'tool_description_override'. lekin yahan error ka koi scene nhi ha
