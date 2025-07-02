import asyncio, os
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
from dotenv import load_dotenv
from rich import print
from openai.types.responses import ResponseTextDeltaEvent


#? StreamEvent: TypeAlias = Union[
#?     RawResponsesStreamEvent,
#?     RunItemStreamEvent,
#?     AgentUpdatedStreamEvent,
#? ]

#! RawResponsesStreamEvent{
#!     data: TResponseStreamEvent,
#!     type: 'raw_response_event'
#! }

#! RunItemStreamEvent{
#!     name: Literal[
#!         "message_output_created",
#!         "handoff_requested",
#!         "handoff_occured",
#!         "tool_called",
#!         "tool_output",
#!         "reasoning_item_created",
#!         "mcp_approval_requested",
#!         "mcp_list_tools",
#!     ],
#!     item:RunItem
#! }


#! AgentUpdatedStreamEvent{
#!     new_agent: Agent[Any]
#! }


#* RunItem: TypeAlias = Union[
#*     MessageOutputItem,
#*     HandoffCallItem,
#*     HandoffOutputItem,
#*     ToolCallItem,
#*     ToolCallOutputItem,
#*     ReasoningItem,
#*     MCPListToolsItem,
#*     MCPApprovalRequestItem,
#*     MCPApprovalResponseItem,
#* ]


load_dotenv()
set_tracing_disabled(disabled=True)

API_KEY=os.environ.get("GEMINI_API_KEY")

model=OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=AsyncOpenAI(
        api_key=API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai"
    )
)

async def main():
    agent = Agent(
        name="Joker",
        instructions="You are a helpful assistant.",
        model=model
    )

    result = Runner.run_streamed(agent, input="Please tell me 5 jokes.")
    async for event in result.stream_events():
        print(event.type)

if __name__ == "__main__":
    asyncio.run(main())