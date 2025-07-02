# type: ignore
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
from dotenv import load_dotenv
import os

set_tracing_disabled(True)
API_KEY = os.environ.get("GEMINI_API_KEY")

model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai"
    ),
)

@function_tool

def add_two_numbers(a: int, b: int) -> int:
    """Add the two numbers
    
    Args:
        a: the first number
        b: the second number
    """
    return a+b

math_expert_agent = Agent(
    name="Mathematician", 
    instructions="You are good at maths",
    model=model,
    tools=[add_two_numbers]    
)

physics_expert_agent = Agent(
    name="Physician", 
    instructions="You are good at physics",
    model=model,
)

confidentional_agent = Agent(
    name="General Knowledge Assistant",
    instructions=(
        "You are a highly intelligent, confident assistant capable of answering questions "
        "across all domains including science, technology, history, philosophy, math, health, and more. "
        "Respond clearly and accurately, and if you're unsure about something, state that honestly."
    ),
    model=model
)

triage_agent = Agent(
    name="Triage agent",
    instructions=(
        "Help the user with their questions."
        "If they ask about maths, handoff to the maths agent."
        "If they ask about physics, handoff to the physics agent."
    ),
    handoffs=[math_expert_agent, physics_expert_agent, confidentional_agent],
    model=model
)

result = Runner.run_sync(starting_agent=triage_agent, input="What is the sum of 425 and 252")
print(result.final_output)
print(result.new_items)

#! OUTPUT EXPLANATION:

#* 1. A user prompt was received by the Triage agent.
#* 2. The Triage agent has three sub-agents (handoffs): Mathematician, Physician, and General Knowledge Assistant.
#* 3. Based on the user query, the Triage agent decided the question was related to **math**.
#* 4. It triggered a handoff to the **Mathematician** agent using a function call: `transfer_to_mathematician`.
#* 5. This handoff is represented as a `HandoffCallItem`, signaling that the triage is handing over the query.
#* 6. Next, a `HandoffOutputItem` was created, confirming that the system successfully switched from Triage to the Mathematician agent.
#* 7. Finally, a `ToolCallItem` would likely follow (cut off in your message), where the Mathematician might execute the `add_two_numbers` tool.
#* 
#* → Output: The system correctly routed the math question from the Triage agent to the Mathematician agent.
#* → Result: The Mathematician agent is now responsible for handling the query and potentially invoking a math-related tool.


#! OUTPUT EXAMPLE:

[
  HandoffCallItem(
    agent=Agent(
      name='Triage agent',
      instructions=(
        "Help the user with their questions."
        "If they ask about maths, handoff to the maths agent."
        "If they ask about physics, handoff to the physics agent."
      ),
      handoff_description=None,
      handoffs=[
        Agent(
          name='Mathematician',
          instructions='You are good at maths',
          handoff_description=None,
          handoffs=[],
          model=<OpenAIChatCompletionsModel ...>,
          model_settings=ModelSettings(
            temperature=None, top_p=None, frequency_penalty=None,
            presence_penalty=None, tool_choice=None, parallel_tool_calls=None,
            truncation=None, max_tokens=None, reasoning=None, metadata=None,
            store=None, include_usage=None, extra_query=None,
            extra_body=None, extra_headers=None
          ),
          tools=[
            FunctionTool(
              name='add_two_numbers',
              description='Add the two numbers',
              params_json_schema={
                'properties': {
                  'a': {'description': 'the first number', 'title': 'A', 'type': 'integer'},
                  'b': {'description': 'the second number', 'title': 'B', 'type': 'integer'}
                },
                'required': ['a', 'b'],
                'title': 'add_two_numbers_args',
                'type': 'object',
                'additionalProperties': False
              },
              on_invoke_tool=<function _on_invoke_tool ...>,
              strict_json_schema=True
            )
          ],
          mcp_servers=[],
          mcp_config={},
          input_guardrails=[],
          output_guardrails=[],
          output_type=None,
          hooks=None,
          tool_use_behavior='run_llm_again',
          reset_tool_choice=True
        ),
        Agent(
          name='Physician',
          instructions='You are good at physics',
          handoff_description=None,
          handoffs=[],
          model=<OpenAIChatCompletionsModel ...>,
          model_settings=ModelSettings(...),
          tools=[],
          mcp_servers=[],
          mcp_config={},
          input_guardrails=[],
          output_guardrails=[],
          output_type=None,
          hooks=None,
          tool_use_behavior='run_llm_again',
          reset_tool_choice=True
        ),
        Agent(
          name='General Knowledge Assistant',
          instructions=(
            "You are a highly intelligent, confident assistant capable of answering questions across all domains "
            "including science, technology, history, philosophy, math, health, and more. Respond clearly and "
            "accurately, and if you're unsure about something, state that honestly."
          ),
          handoff_description=None,
          handoffs=[],
          model=<OpenAIChatCompletionsModel ...>,
          model_settings=ModelSettings(...),
          tools=[],
          mcp_servers=[],
          mcp_config={},
          input_guardrails=[],
          output_guardrails=[],
          output_type=None,
          hooks=None,
          tool_use_behavior='run_llm_again',
          reset_tool_choice=True
        )
      ],
      model=<OpenAIChatCompletionsModel ...>,
      model_settings=ModelSettings(...),
      tools=[],
      mcp_servers=[],
      mcp_config={},
      input_guardrails=[],
      output_guardrails=[],
      output_type=None,
      hooks=None,
      tool_use_behavior='run_llm_again',
      reset_tool_choice=True
    ),
    raw_item=ResponseFunctionToolCall(
      arguments='{}',
      call_id='',
      name='transfer_to_mathematician',
      type='function_call',
      id='__fake_id__',
      status=None
    ),
    type='handoff_call_item'
  ),
  
  HandoffOutputItem(
    agent=Agent(
      name='Triage agent',
      instructions=(
        "Help the user with their questions."
        "If they ask about maths, handoff to the maths agent."
        "If they ask about physics, handoff to the physics agent."
      ),
      handoff_description=None,
      handoffs=[ ... same handoffs as above ... ],
      model=<OpenAIChatCompletionsModel ...>,
      model_settings=ModelSettings(...),
      tools=[],
      mcp_servers=[],
      mcp_config={},
      input_guardrails=[],
      output_guardrails=[],
      output_type=None,
      hooks=None,
      tool_use_behavior='run_llm_again',
      reset_tool_choice=True
    ),
    raw_item={
      'call_id': '',
      'output': "{'assistant': 'Mathematician'}",
      'type': 'function_call_output'
    },
    source_agent=Agent( ... same as above ... ),
    target_agent=Agent( ... Mathematician ... ),
    type='handoff_output_item'
  ),

  ToolCallItem(
    agent=Agent(
      name='Mathematician',
      instructions='You are good at maths',
      handoff_description=None,
      handoffs=[],
      model=<OpenAIChatCompletionsModel ...>,
      model_settings=ModelSettings(...),
      tools=[
        FunctionTool(
          name='add_two_numbers',
          description='Add the two numbers',
          params_json_schema={ ... },
          on_invoke_tool=<function _on_invoke_tool ...>,
          strict_json_schema=True
        )
      ],
      mcp_servers=[],
      mcp_config={},
      input_guardrails=[],
      output_guardrails=[],
      output_type=None,
      hooks=None,
      tool_use_behavior='run_llm_again',
      reset_tool_choice=True
    ),
    raw_item=ResponseFunctionToolCall(
      arguments='{"b":252,"a":425}',
      call_id='',
      name='add_two_numbers',
      type='function_call',
      id='__fake_id__',
      status=None
    ),
    type='tool_call_item'
  ),

  ToolCallOutputItem(
    agent=Agent(
      name='Mathematician',
      instructions='You are good at maths',
      handoff_description=None,
      handoffs=[],
      model=<OpenAIChatCompletionsModel ...>,
      model_settings=ModelSettings(...),
      tools=[ ... ],
      mcp_servers=[],
      mcp_config={},
      input_guardrails=[],
      output_guardrails=[],
      output_type=None,
      hooks=None,
      tool_use_behavior='run_llm_again',
      reset_tool_choice=True
    ),
    raw_item={
      'call_id': '',
      'output': '677',
      'type': 'function_call_output'
    },
    output=677,
    type='tool_call_output_item'
  ),

  MessageOutputItem(
    agent=Agent(
      name='Mathematician',
      instructions='You are good at maths',
      handoff_description=None,
      handoffs=[],
      model=<OpenAIChatCompletionsModel ...>,
      model_settings=ModelSettings(...),
      tools=[ ... ],
      mcp_servers=[],
      mcp_config={},
      input_guardrails=[],
      output_guardrails=[],
      output_type=None,
      hooks=None,
      tool_use_behavior='run_llm_again',
      reset_tool_choice=True
    ),
    raw_item={
      'id': '',
      'object': 'chat.completion',
      'created': 1234567890,
      'model': 'gpt-4o-mini',
      'choices': [
        {
          'message': {
            'role': 'assistant',
            'content': 'The sum of 425 and 252 is 677.'
          },
          'finish_reason': 'stop',
          'index': 0
        }
      ]
    },
    output='The sum of 425 and 252 is 677.',
    type='message_output_item'
  )
]
