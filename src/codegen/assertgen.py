

from pydantic import ValidationError
from .split import FunctionCode
from openai import OpenAI

client = OpenAI()

def system(content: str) -> dict:
    return {"role": "system", "content": content}

def user(content: str) -> dict:
    return {"role": "user", "content": content}

def assertgen_inner(code: FunctionCode) -> FunctionCode:
    return client.beta.chat.completions.parse(
        model="gpt-4o",
        messages = [
            system(
                "You are a professional software engineer. Your task is to **add runtime assertions** to a function you have implemented, which already satisfies the user’s prompt.\n"
                "\n"
                "Your goal is to catch potential bugs by validating assumptions during execution, including:\n"
                "\n"
                "- **Input and output correctness**.\n"
                "- **Loop invariants and intermediate state checks**, where applicable.\n"
                "\n"
                "Guidelines:\n"
                "\n"
                "- Each assertion must include an **informative error message** that references relevant variables in scope.\n"
                "- **Always generate an assertion checking the exact logic specification of the output** to validate that the output is corrent. You may define helper functions to support this check.\n"
                "- Use the **function signature and docstring** (if present) as guidance for the expected behavior and constraints.\n"
                "- **Do not modify the core logic** of the function.\n"
                # "- Mock testing will be used in the code. **Do not add any assertions to check types.** Also remove all the existing type checking assertions.  \n"
                "- Remove all comments from the code **except for the docstring**.\n"
                "- **Say it again, keep the doc string!**\n"
                "\n"
                "In your response, include:\n"
                "\n"
                "- The **function name**.\n"
                "- The **full function code** with assertions added.\n"
            ),
            user(
                f"```python\n"
                f"{code.code}\n"
                f"```\n"
            )
        ],
        response_format=FunctionCode,
    ).choices[0].message.parsed

def assertgen(code: FunctionCode) -> FunctionCode:
    f = None
    for _ in range(4):
        try:
            f = assertgen_inner(code)            
            break
        except ValidationError as e:
            continue
    return f
