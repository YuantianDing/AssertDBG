
from mirascope import BaseMessageParam

from src.codegen.intentcheck import intent_check
from .split import FunctionCode
from mirascope.core import Messages, openai

@openai.call(model="gpt-4o", response_model=FunctionCode)
def task_solve_inner(code: FunctionCode, main_function: FunctionCode, remove_assert: bool) -> list[BaseMessageParam]:
    return [
        Messages.System(
            "You are a professional software engineer. Your task is to **implement a Python subfunction** that fully satisfies the user’s specifications.\n"
            "\n"
            "The user will provide:\n"
            "\n"
            "- The **function name and signature**.\n"
            "- A **docstring** describing the function’s behavior.\n"
            "- **Input/output assertions** that define expected constraints.\n"
            "- An explanation of how the function is used in the **main function**.\n"
            "\n"
            "Your responsibilities:\n"
            "\n"
            "- **Implement the function** according to the provided signature and description. Your implementation must accurately match the function signature and docstring provided in the prompt. \n"
            "- You should try to use the simplest algorithm that guarrentee safety and reduce error. Try to **avoid complex algorithm and keep the codebase small** !!!!!!!!! \n"
            "- If there are **any common python libraries** (Sympy, for example) that already implemented the main functions or the subfunctions, **DO NOT REINVENT THE WHEEL** and implement the code yourself !!!!!!!\n"
            "- Make sure to put the imports **before** the function signature.\n"
            "- Include **only the function implementation** (with signature) — **no test code** is required.\n"
            "- Add **clear, concise comments** to explain your logic and design choices.\n"
            "- Ensure **strict consistency** with the input/output types, expected behavior, and any exceptions described in the user prompt.\n"
            f"{'- **Remove all assertions** from the code. ' if remove_assert else ''}\n"
            "\n"
            "This is a production-level implementation, so accuracy, clarity, and adherence to the specification are essential.\n"
        ), 
        Messages.User(
            "Here is the subfunction you need to implement: \n"
            "\n"
            f"```python\n"
            f"{code.code}\n"
            f"```\n"
            "\n"
            f"Here is how the subfunction is used in side the main function `{main_function.function_name}`: \n"
            "\n"
            f"```python\n"
            f"{main_function.code}\n"
            f"```\n"
            "\n"
        )
    ]

def task_solve(code: FunctionCode, main_function: FunctionCode, remove_assert: bool = False) -> FunctionCode:
    f = None
    for _ in range(4):
        f = task_solve_inner(code, main_function, remove_assert)
        if code.function_name == f.function_name and f.function_name in f.code and intent_check(f):
            break
    return f
