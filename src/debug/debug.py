from datetime import timedelta
from typing import Literal, Union
from mirascope import BaseMessageParam, BaseTool
from pydantic import BaseModel, Field, ValidationError
from pydantic_cache import disk_cache
from termcolor import colored

from src.my_cache import my_cache
from ..codegen.split import FunctionCode, SplittedTask
from mirascope.core import openai, Messages
from mirascope.core.openai.call_response import OpenAICallResponse

class FixCode(BaseModel):
    """Provide fix for a certain function in the codebase. """
    action: Literal["fix_code"]
    functions: list[FunctionCode]

class RequestRework(BaseModel):
    """Request to reimplement the entire codebase. """
    action: Literal["request_rework"]

class DebugAction(BaseModel):
    inner: Union[FixCode, RequestRework]

    def perform(self, code: SplittedTask, test: FunctionCode, verbose: int = 0) -> bool:
        functions = {}
        functions[test.function_name] = test
        functions[code.main_func.function_name] = code.main_func
        for i in range(len(code.subfunctions)):
            functions[code.subfunctions[i].function_name] = code.subfunctions[i]
            assert functions[code.subfunctions[i].function_name] is code.subfunctions[i]

        if self.inner.action == "request_rework":
            return False
        else:
            if verbose > 4:
                print(colored("Generated Fix: ", "green", attrs=["bold"]))
            
            for f in self.inner.functions:
                if f.function_name in functions:
                    functions[f.function_name].code = f.code
                    if verbose > 4:
                        functions[f.function_name].pretty_print("| ")
            return True

@my_cache(".cache/debug")
def debug(code: SplittedTask, test: FunctionCode, error: str, verbose: int = 0) -> DebugAction:
    if verbose > 1:
        print(colored("LLM Debuging...", "yellow", attrs=["bold"]))
    functions = {}
    functions[test.function_name] = test
    functions[code.main_func.function_name] = code.main_func
    for i in range(len(code.subfunctions)):
        functions[code.subfunctions[i].function_name] = code.subfunctions[i]
        assert functions[code.subfunctions[i].function_name] is code.subfunctions[i]

    class ViewFunc(BaseTool):
        """
        Request to view a function in the codebase.
        If the function is found in the codebase Return function code.
        Otherwise, return `None`.
        """
        function_name: str = Field(description="The name of the function requested.")
        
        def call(self)  -> Union[str, None]:
            if verbose > 2:
                print(colored("Model Viewing: ", "green") + self.function_name)
            if self.function_name in functions:
                return Messages.System(
                    f"[view_func] Viewing function {self.function_name}:\n"
                    "\n"
                    "```python\n"
                    f"{functions[self.function_name].code}\n"
                    "```\n"
                )
            else:
                return Messages.System(f"Viewing function {self.function_name}: Function not found.")
    messages = [
        Messages.System(
            "You are a professional Python developer tasked with diagnosing and fixing a bug revealed by a failing unit test.\n"
            "\n"
            "The user will provide you with an **error message** that contains valuable clues about the issue. Your job is to investigate the codebase, determine the root cause, and propose an appropriate fix.\n"
            "\n"
            "The codebase consists of the following functions:  \n"
            f"**{','.join(f'`{f}`' for f in functions.keys())}**\n"
            "\n"
            "To assist in your investigation, you have access to a tool called `ViewFunc`. This tool takes a function name as input and returns its full source code as a string, if it exists.\n"
            "\n"
            "Once you’ve identified the cause of the bug, choose one of the following actions:\n"
            "\n"
            "- **`fix_code`**: Propose a fix by rewriting any and all functions that should be modified. Include only the updated versions.\n"
            "- **`request_rework`**: Recommend a complete reimplementation of the codebase. \n"
            "    Use this when the code is poorly structured or contains errors that are too difficult to locate and resolve incrementally. \n"
            "    This is primarily useful for syntax errors and timeouts. \n"
            "\n"
            "Guidelines:\n"
            "\n"
            "- The issue may stem from function implementations **or** from the unit test itself (e.g. incorrect assertions or invalid assumptions).\n"
            "- **Avoid changing unrelated code**. Keep your changes minimal and focused.\n"
            "- If external packages are required, **import them before the function signature**.\n"
            "- Test cases are run with a **1-minute timeout**. If a test is timing out, consider fixing or simplifying it.\n"
            "- If the code already does a complete check on the output using assertions, the test case error is often caused by a wrong test case. In such cases, it is acceptable to **remove the faulty test case**.\n"
            "- When introducing new helper or subfunctions, ensure that **they are not already present** in the function list above.\n"
            "\n"
            "Be systematic, pragmatic, and concise in your debugging process.\n"
        ),
        Messages.User(error),
        ViewFunc(function_name=test.function_name).call(),
    ]

    @openai.call("gpt-4o", response_model=DebugAction, tools=[ViewFunc])
    def step():
        return messages
    
    while True:
        try:
            fix_resp = step()
        except ValidationError as e:
            print(colored(f"Validation Error: debug {e}", "red"))
            continue
        if isinstance(fix_resp, OpenAICallResponse):
            messages += [ fix_resp.tool.call() ]
        elif isinstance(fix_resp, DebugAction):
            if fix_resp.inner.action == "fix_code" and not all(f.function_name in f.code for f in fix_resp.inner.functions):
                continue
            return fix_resp
        else:
            raise ValueError(f"Unexpected response type: {type(fix_resp)}")
            

    