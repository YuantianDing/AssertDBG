

from .. import models
from .split import FunctionCode
from langchain_core.messages import SystemMessage, HumanMessage

def assertgen(code: FunctionCode):
    message = [
        SystemMessage(
            "You are a professional software engineer. Your task is to add assertions to the function implemented by yourself that already satisfies the user prompts. "
            "You need to add assertions to report potential bugs of the function, including input/output correctness check and loop invariants: \n"
            "\n"
            "* For each assertion, provide an error message that captures the useful variables in the scope. \n"
            "* Be sure to add an assertion at the end of the function to check if the output is desired. You may define helper functions if needed. \n"
            "* Try to use the function signature and the comments to guide your assertions. \n"
            "* Do not change the functionality of the function. \n"
            "\n"
            "Respond with code as well as the function name. Remove all comments in the code except the docstring. \n"
        ), HumanMessage(
            f"```python\n"
            f"{code.code}\n"
            f"\n"
            f"{code.testing_code}\n"
            f"```\n"
        )
    ]
    return models.MODELS["assert"].with_structured_output(FunctionCode).invoke(message)