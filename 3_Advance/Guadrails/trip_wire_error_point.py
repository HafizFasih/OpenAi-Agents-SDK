from agents import input_guardrail, GuardrailFunctionOutput

@input_guardrail
def my_guardrail(ctx, agent, input):
    return GuardrailFunctionOutput(
        output_info=None,
        tripwire_triggered=True
    )


#! Yahan pr mene tripwire_triggered ko True set kia hua ha. 
#! To kia ye code crash hojayega ????
#! Ya nhi hoga?

#! Bilkul nhi hoga q ke code crash hona ya na hona iski logic guadrails ma nhi likhi hui ha.
#! just ek property ha named 'tripwire_triggered' jo ye decide krta ha k crash krna ha ya nhi (just True ua False) but guadrails ma kahin error generate nhi hota.


#! Sawal phr ye ha k error kahan aata h phr ??

#! Jab ham Runner.run chalaty hain to Runner.run() k andar ek method run hota ha jiska name ha '_run_input_guardrails' wahan pr sabhi input guadrails k tasks banaye jaty hain (parallell execution k liye) to wahan 'InputGuardrailTripwireTriggered' ko raise kia jata ha in case kisi bh guardrail ka tripwire_triggered=True ho

#! It Means k Runner.run ko chalany pr hi error ayega agar tripwire_triggered True ho wrna nhi ayega