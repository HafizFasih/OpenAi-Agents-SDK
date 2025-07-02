from agents import function_tool

@function_tool(name_override="addition")
def add(a: int, b: int) -> int:
    """Add two numbers
    Args:
        a: first number
        b: second number
        
    Returns:
        int: The sum of the two numbers.
    """
    return a + b


@function_tool
def subtract(a: int, b: int) -> int:
    """subtract two numbers
    Args:
        a: first number
        b: second number
        
    Returns:
        int: The difference of the two numbers.
    """
    return a + b

print(add.name) #! addition is the final name
print(subtract.name) #! subtract

#! Zahir si baat ha agar koi name override krdia jaye to final value uski wohi (override wali) hogi
#? IMPORTANT: description k liye bh same rule ha