





from .. import models
from .split import FunctionCode
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.chain import LLMChain

def task_solve(code: FunctionCode, main_function: FunctionCode):
    message = [
        SystemMessage(
            "You are a professional software tester. Your task is to implement a single test case for a python programming task "
            "User prompts includes a function name and signature, a docstring description, input/output assertions, test cases, and how the function is used in the main function. "
            "You only need to implement the function that satisfies the user prompts. "
            "Generate the function implementation as long as the signature. No testing needed. "
            "Be sure to add comments to the code to explain your implementation. "
            "Please make sure that the inputs, output and exceptions are strictly consistent with the user prompts. ",
        ), HumanMessage(
            "Here is the subfunction you need to implement: \n"
            "\n"
            f"```python\n"
            f"{code.code}\n"
            f"\n"
            f"{code.testing_code}\n"
            f"```\n"
            "\n"
            "Here is the main function that uses the subfunction: \n"
            "\n"
            f"```python\n"
            f"{main_function.code}\n"
            f"```\n"
            "\n"
        )
    ]
    return LLMChain(models.MODELS["test"].with_structured_output(FunctionCode), message)


