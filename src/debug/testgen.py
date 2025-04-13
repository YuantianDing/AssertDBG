
from datetime import timedelta
from pydantic_cache import disk_cache
from ..codegen.split import FunctionCode
from openai import OpenAI

client = OpenAI()

@disk_cache(".cache/test_gen", ttl=timedelta(days=2000))
def test_gen(prompt: str, test_count: int = 8) -> list[FunctionCode]:
    result =  client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            { 
                "role": "system",
                "content":
                    "You are a professional software tester. Your job is to generate standalone a test function, to test a the function given by the user.\n"
                    "User will provide only the function's description and signature, without the definition of the function. \n"
                    "\n"
                    "The test function should:\n"
                    "\n"
                    "- Have **no arguments**.\n"
                    "- Use **assertions or raise errors** to indicate test failures.\n"
                    "- **Not be wrapped** in `unittest.TestCase` or any testing framework classes.\n"
                    "- Your job is to define the test function only. Do not generate other functions\n"
                    "\n"
                    "You may use any standard or third-party libraries to assist with the testing logic.\n"
                    "\n"
                    "In your response, provide:\n"
                    "\n"
                    "- A **descriptive function name** for this specific test.\n"
                    "- The **full code** of the test function.\n"
                    "- In the test function, you should first provide code to generate some random test cases. \n"
                    "- Then, you should also generate some individual test cases to check different edge cases, expected behavior, and potential failure points based on the task description. \n"
                    "\n"
                    "Hint: for problems with encode/decode patterns, make sure always to use two functions in pair. \n"
            }, { 
                "role": "system",
                "content": prompt
            }
        ],
        response_format=FunctionCode,
        n=test_count,
    )
    assert len(result.choices) == test_count
    return [c.message.parsed for c in result.choices]


