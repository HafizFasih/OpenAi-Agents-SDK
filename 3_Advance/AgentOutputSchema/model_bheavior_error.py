# type: ignore
from agents import AgentOutputSchema
from rich import print
from pydantic import BaseModel
import json

class UserInfo(BaseModel):
    name: str
    age: int

agent_output = AgentOutputSchema(UserInfo)
print(agent_output)

json_obj={"name": "Muhammad Fasih", "age": 10}
json_obj_str=json.dumps(json_obj)
final_obj=agent_output.validate_json(json_obj_str)
print(final_obj)

#! Yahan error ajayega q k name attribute missing ha hamari dict ma
json_error_obj={"name": "Ahmed"}
json_error_obj_str=json.dumps(json_error_obj)
final_error_obj=agent_output.validate_json(json_error_obj)
print(final_error_obj)

#! Two cases or hain ModelBehaviorError any ke

#! Jesa k hamy pata ha agar output_type inmy se koi ho (tuple, set, int, bool, float etc) to direct is format ma response nhi aata hamary paas. Hamary paas 2 hi format ma response ata ha. Ya plain str ya phr JSON object. 

#? To iska mtlb ye ha k agar in me se koi type ho (tuple, set, int, bool, float etc) to isko ek dict ma wrap krlia jayega or ek key banayegi with named 'response' and then us key ki value ma hamara main output ayega.

#* NOTE: Ye 'response' wali key ki agent_output file ma ek constant variabel ma set ha 
#* e.g _WRAPPER_DICT_KEY = "response"

#! 1. To ab agar LLM dict k format ma na den response to ModelBehaviorError trigger hoga.
#! 2. Agar LLM dict k format ma de answer but usmy 'response' wali key mojood nhi ho to tab bhi ModelBehaviorError ayega.

