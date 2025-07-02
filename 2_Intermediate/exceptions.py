# type: ignore
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .guardrail import InputGuardrailResult, OutputGuardrailResult

#! Exceptions
#? AgentsException
#* Bases: Exception

#* Base class for all exceptions in the Agents SDK.

#* Source code in src/agents/exceptions.py

class AgentsException(Exception):
    """Base class for all exceptions in the Agents SDK."""


#? MaxTurnsExceeded
#* Bases: AgentsException

#* Exception raised when the maximum number of turns is exceeded.

#* Source code in src/agents/exceptions.py


class MaxTurnsExceeded(AgentsException):
    """Exception raised when the maximum number of turns is exceeded."""

    message: str

    def __init__(self, message: str):
        self.message = message


#? ModelBehaviorError
#* Bases: AgentsException

#* Exception raised when the model does something unexpected, e.g. calling a tool that doesn't exist, or providing malformed JSON.

#* Source code in src/agents/exceptions.py

class ModelBehaviorError(AgentsException):
    """Exception raised when the model does something unexpected, e.g. calling a tool that doesn't
    exist, or providing malformed JSON.
    """

    message: str

    def __init__(self, message: str):
        self.message = message


#? UserError
#* Bases: AgentsException

#* Exception raised when the user makes an error using the SDK.

#* Source code in src/agents/exceptions.py


class UserError(AgentsException):
    """Exception raised when the user makes an error using the SDK."""

    message: str

    def __init__(self, message: str):
        self.message = message

#? InputGuardrailTripwireTriggered
#* Bases: AgentsException

#* Exception raised when a guardrail tripwire is triggered.

#* Source code in src/agents/exceptions.py
#* guardrail_result instance-attribute

#* guardrail_result: InputGuardrailResult = guardrail_result
#* The result data of the guardrail that was triggered.


class InputGuardrailTripwireTriggered(AgentsException):
    """Exception raised when a guardrail tripwire is triggered."""

    guardrail_result: "InputGuardrailResult"
    """The result data of the guardrail that was triggered."""

    def __init__(self, guardrail_result: "InputGuardrailResult"):
        self.guardrail_result = guardrail_result
        super().__init__(
            f"Guardrail {guardrail_result.guardrail.__class__.__name__} triggered tripwire"
        )


#? OutputGuardrailTripwireTriggered
#* Bases: AgentsException

#* Exception raised when a guardrail tripwire is triggered.

#* Source code in src/agents/exceptions.py
#* guardrail_result instance-attribute

#* guardrail_result: OutputGuardrailResult = guardrail_result
#* The result data of the guardrail that was triggered.


class OutputGuardrailTripwireTriggered(AgentsException):
    """Exception raised when a guardrail tripwire is triggered."""

    guardrail_result: "OutputGuardrailResult"
    """The result data of the guardrail that was triggered."""

    def __init__(self, guardrail_result: "OutputGuardrailResult"):
        self.guardrail_result = guardrail_result
        super().__init__(
            f"Guardrail {guardrail_result.guardrail.__class__.__name__} triggered tripwire"
        )
