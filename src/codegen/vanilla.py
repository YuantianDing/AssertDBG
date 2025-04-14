
from datetime import timedelta
from mirascope import BaseMessageParam
from pydantic_cache import disk_cache

from src.my_cache import my_cache
from src.codegen.intentcheck import intent_check
from .split import FunctionCode
from mirascope.core import Messages, openai

@my_cache(".cache/vanilla")
@openai.call(model="gpt-4o", response_model=FunctionCode)
def vanilla(prompt: str) -> FunctionCode:
    return [
        Messages.System(
            "You are a professional software engineer. Your task is to **implement a Python function** that fully satisfies the user’s specifications.\n"
            "\n"
            "The user will provide:\n"
            "\n"
            "- The **function name and signature**.\n"
            "- A **docstring** describing the function’s behavior.\n"
            "\n"
            "Your responsibilities:\n"
            "\n"
            "- **Implement the function** according to the provided signature and description. Your implementation must accurately match the function signature and docstring provided in the prompt. \n"
            "- You should try to use the simple implementation that guarrentee safety and reduce error. Try to avoid complex algorithm. \n"
            "- You may use any libraries needed. Make sure to put the imports **before** the function signature.\n"
            "- Include **only the function implementation** (with signature) — **no test code** is required.\n"
            "- Ensure **strict consistency** with the input/output types, expected behavior, and any exceptions described in the user prompt.\n"
            "\n"
            "This is a production-level implementation, so accuracy, clarity, and adherence to the specification are essential.\n"
        ), 
        Messages.User(
            f"```python\n"
            f"{prompt}\n"
            f"```\n"
        )
    ]
