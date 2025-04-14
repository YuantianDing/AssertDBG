
from datetime import timedelta
from mirascope import Messages
from termcolor import colored

from src.my_cache import my_cache
from ..codegen.split import FunctionCode
from mirascope.core import openai

@my_cache(".cache/test_gen")
@openai.call(model="gpt-4o", response_model=FunctionCode)
def test_gen(id: int, prompt: str, add_error_msg: bool = True) -> FunctionCode:
    print(colored("LLM Generating Test...", "yellow", attrs=["bold"]))
    return [
            Messages.System(
                    "You are a professional software tester. Your job is to generate standalone a test function, to test a the function given by the user.\n"
                    "User will provide only the function's description and signature, without the definition of the function. \n"
                    "\n"
                    "The test function should:\n"
                    "\n"
                    "- Have **no arguments**.\n"
                    "- Use **assertions or raise errors** to indicate test failures.\n"
                    "- **Not be wrapped** in `unittest.TestCase` or any testing framework classes.\n"
                    "- Your job is to define the test function only. Do not generate other functions\n"
                    f"{'- **Do not provide any error messages** in any of the assertions/exceptions. ' if not add_error_msg else '' }\n"
                    "\n"
                    "You may use any standard or third-party libraries to assist with the testing logic.\n"
                    "\n"
                    "In your response, provide:\n"
                    "\n"
                    "- A **descriptive function name** for this specific test.\n"
                    "- The **full code** of the test function.\n"
                    "- In the test function, you should first provide code to generate thousands of random test cases. \n"
                    "- Then, you should also generate some individual test cases to check different edge cases, expected behavior, and potential failure points based on the task description. \n"
                    f"{'- **Do not provide any error messages** in any of the assertions/exceptions. ' if not add_error_msg else '' }\n"
                    "\n"
                    "Hint: for problems with encode/decode patterns, make sure always to use two functions in pair. \n"
            ), Messages.User(
                f"```python\n"
                f"{prompt}\n"
                f"```\n"
            )
        ]


