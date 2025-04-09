


from .. import models
from .split import FunctionCode
from langchain_core.messages import SystemMessage, HumanMessage

def task_solve(code: FunctionCode):
    message = [
        SystemMessage(
            "You are a professional software engineer. Your task is to implement a python function that satifies the user prompts. "
            "User prompts includes a function name and signature, a docstring description, input/output assertions, and test cases. "
            "You only need to implement the function that satisfies the user prompts. "
            "Generate the function implementation as long as the signature. No testing needed. "
            "Be sure to add comments to the code to explain your implementation. ",
        ), HumanMessage(
            f"```python\n"
            f"{code.code}\n"
            f"```\n"
        )
    ]
    return models.MODELS["task"].with_structured_output(FunctionCode).invoke(message)


