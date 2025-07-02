from agents import input_guardrail, GuardrailFunctionOutput

#! 1. First method to make a guardrial
@input_guardrail
def guardrail_without_name(ctx, agent, input):
    return GuardrailFunctionOutput(
        output_info=None,
        tripwire_triggered=False
    )

#! Default None hoga lekin agar None hua to function ka name consider kia jayega
print(guardrail_without_name.get_name())
#! Output: guardrail_without_name

#! Intersting thing iska output None ayega q ke @input_guardrail decorator name ko jab hi assign kr raha ha jab ham ussy as a parameter pass kren
print(guardrail_without_name.name)
#! Output: None


#? Hona ye chahye tha k default ma func.__name__ lia jaye or agar override kren ham to us waqt phr override wala name assign hojaye.


#! 2. Second method to make a guardrail
@input_guardrail(name="new_name") #! Yahan pr hamny name ko override krdia ha 
def guardrail_with_name(ctx, agent, input):
    return GuardrailFunctionOutput(
        output_info=None,
        tripwire_triggered=False
    )

#! Default None hoga lekin agar None hua to function ka name consider kia jayega
#! But hamny jese ke decorator ma new_name define krdia ha to wohi name consider hoga
print(guardrail_with_name.get_name())
#! Output: new_name

#! Output new_name ayega q ke hamny decorator ma define krdia ha
print(guardrail_with_name.name)
#! Output: new_name