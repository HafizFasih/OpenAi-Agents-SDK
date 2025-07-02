from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled, input_guardrail, output_guardrail, GuardrailFunctionOutput, AgentOutputSchema, RunContextWrapper, TResponseInputItem, InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered, RunConfig
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Optional
from rich import print
import os, asyncio

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

class FieldMetrics(BaseModel):
    avg_salary_range: str 
    job_demand_index: float 
    growth_rate_projection: float 
    num_companies_hiring: int
    innovation_score: float
    local_talent_pool_size: int
    networking_events_per_month: int

class CitySpecificDetails(BaseModel):
    cost_of_living_index: float 
    average_commute_time_mins: Optional[int]
    major_universities_count: int
    supportive_regulatory_environment: bool

class BestTechnicalFieldFormat(BaseModel):
    name: str 
    city: str 
    country: str 
    field_metrics: FieldMetrics
    city_details: CitySpecificDetails
    overall_attractiveness_score: Optional[float] 
    sources_from_where_you_gather_info: List[str]

class RelevantQuery(BaseModel):
    is_fields_related: bool

@output_guardrail
async def run_guardrail(
    ctx: RunContextWrapper[None], 
    agent: Agent[None], 
    input: List[TResponseInputItem] | str
) -> GuardrailFunctionOutput:
    print("RunGuardrail has been triggered")
    return GuardrailFunctionOutput(
        output_info="Successfull",
        tripwire_triggered=False
    )

config=RunConfig(
    output_guardrails=[run_guardrail]
)

input_guard=Agent(
    name="Checker",
    instructions="Check wether the input is about any field related or not",
    model=model,
    output_type=AgentOutputSchema(RelevantQuery, True)
)

@input_guardrail(name="Checker")
async def filter_out_irrelevant_quries(
    ctx: RunContextWrapper[None], 
    agent: Agent[None],
    input: str | List[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result= await Runner.run(
        starting_agent=input_guard,
        input=input
    )
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_fields_related
    )
        
@output_guardrail
async def extract_karachi_fields(
    ctx: RunContextWrapper[None],
    agent: Agent[None],
    output_list: List[BestTechnicalFieldFormat],
) -> GuardrailFunctionOutput:

    print("AgentGuardrail has been triggered")
    is_all_karachi_fields=all(output.city.lower() == "karachi" for output in output_list)
    return GuardrailFunctionOutput(
        output_info=output_list, tripwire_triggered=not is_all_karachi_fields
    )
async def main():
    try:
        agent=Agent(
            name="Advisor Agent",
            instructions="You are the best advisor agent, you advise the best **TECHNICAL** fileds or occupations should be occupy according to the given country and city. Make sure that the AMOUNT OF FIELDS is right.",
            output_type=AgentOutputSchema(List[BestTechnicalFieldFormat], strict_json_schema=False),
            model=model,
            input_guardrails=[filter_out_irrelevant_quries],
            output_guardrails=[extract_karachi_fields]
        )
        user_input=input("Ask your Query -> ")
        result = await Runner.run(
            starting_agent=agent,
            input=user_input,
            run_config=config
        )
        print(result.final_output)
        
    except InputGuardrailTripwireTriggered as ig:
        print("Please ask fields reltaed questions")

    except OutputGuardrailTripwireTriggered as og:
        print("All fields should be from Karachi")

asyncio.run(main())

# print(result.input_guardrail_results)
#! InputGuardrailResult:
#?     guardrail=InputGuardrail:
#             *guardrail_function
#             *name
#?     output=GuardrailFunctionOutput:
#             *output_info
#             *tripwire_triggered


# print(result.output_guardrail_results)
#! InputGuardrailResult:
#?     guardrail=OutputGuardrail:
#             *guardrail_function
#             *name
#?     output=GuardrailFunctionOutput:
#             *output_info
#             *tripwire_triggered
#?     agent_output=result.final_output(same)
#?     agent=Agent()

