from agents import input_guardrail, GuardrailFunctionOutput, InputGuardrail
from rich import print

#! ye hamara simple sa guardrail function ha jo ke instance (object) return krta ha
@input_guardrail
def my_guardrail(ctx, agent, input):
    return GuardrailFunctionOutput(
        output_info="test",
        tripwire_triggered=False
    )

#! Yahan pr simple ek object print hoga jiski class InputGuardrail ha
print(my_guardrail)

#! InputGuardrail ki 2 properties ha:
#? 1. guardrail_function 
#* guardrail function ma hamara wo function rkha hota ha jisky uper hamny decorator lagaya ha
#* is case ma guardrail function k value hamara ye wala function hoga 'my_guardrail'
#? 2. name
#* ismy guardrail ka name ata ha, by default None

#! To asan lafzon ma @input_guardrail ka kaam ha ke ek object return krna jiski type InputGuardrail ho or usme jo property ha named 'guardrail_function' usmy hamary function ko rkhna.


#! Iska answer True ayega q ke hamy pata ha k 'my_guardrail' ek object ha jo InputGuardrail ka instance ha
print(isinstance(my_guardrail, InputGuardrail))
#! Output: True

#! Name of the guardrail (ye None hota ha by default)
print(my_guardrail.name)

#! Ye hamara wohi function ha jo hamny line 6 pr banaaya ha
print(my_guardrail.guardrail_function)

#? To hamy samajh ma aya ke '@input guardrail' jo decorator ha wo basically ek object return krta ha jismy 2 properties hoti ha 'name' and 'guardrail_function'


#! IMPORTANT: In sab ko dekh kr aapko lag rha hoga ke Agent jo ha wo InputGuardrail k instance ma se just directly guardrail_function ko call krdeta hoga parameters k saath like e.g [my_guardrail.guardrail_function(ctx, agent, input)] but esa nhi ha. 

#! InputGuardrail ma 2 properties k sath sath 2 methods bh hain first one is get_name() and second is run().

#! Agent jo ha wo run ka method chalata ha naa ke [my_guardrail.guardrail_function(ctx, agent, input)]
#! Ye run method phr InputGuardrailResult ka instance return krta ha jismy 2 keys hain first guardrail itself and second output.

#! 'Output' (property of InputGuardrailResult) ki type GuardrailFunctionOutput ha. Ek bat ghor krni ki ye ha k jo hamny yahan function banaya ha line 6 ma named 'my_guardrail' wo bh to same GuardrailFunctionOutput ka instance return kr raha ha. 

#! G aap bilkul thk smjhy issi function (user ka banaya hua) jo GuardrailFunctionOutput ka instance return kr rha ha issi instance ko 'InputGuardrail.run' ke ma get kia jata ha or phr InputGuardrailResult.output ma assign krdia jata.

#? SAME PATTERN OUTPUT GUADRAIL K LIYE BH FOLLOW HOTA HA BAS THORA SA FARK HA K OutputGuardrailResult MA 2 CHEEZIEN EXTRA RETURN HOTI HA FIRST 'agent_output' (LAST AGENT KA OUTPUT) AND 'agent' (LAST AGENT ITSELF)