from dataclasses import dataclass
import json
import re
import subprocess
from typing import Iterator
from termcolor import colored
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter
import os

def code_word_replace(code, id1, id2):
    result = "".join(id2 if word == id1 else word for word in re.split(r"(\w+)", code))
    return result

@dataclass
class TestCase:
    task_id : str
    prompt: str
    solution: str
    entry_point: str
    test: str
    use: str


    def show(self):
        print(colored("-" * 60 + f" {self.task_id} " + "-" * 60, "yellow"))
        print(colored("Task: ", "blue", attrs=["bold"]) + self.description)
        print(highlight(self.solution, PythonLexer(), TerminalFormatter()))

    def testing_code(self, code: str, function_name: str):
        result = "__name__ = '__test__'\n"
        result += code_word_replace(self.solution, self.entry_point, "reference_solution")
        result += "\n" * 3
        result += code
        result += "\n" * 3
        result += code_word_replace(self.test, self.entry_point, function_name)
        result += "\n" * 3
        return result
        
    def run_test(self, code: str, function_name: str) -> tuple[bool, str] | None:
        assert function_name in code, f"Function `{function_name}` not found in code"
        file_name = f".test/{self.task_id.split('/')[1]}_{hex(hash(code))[2:]}.py"
        with open(file_name, "w") as f:
            f.write(self.testing_code(code, function_name))
        try:
            testing_proc = subprocess.run(["python3",  file_name], capture_output=True, timeout=60)
        except subprocess.TimeoutExpired as e:
            return False, f"{e}"
        return testing_proc.returncode == 0, testing_proc.stderr.decode() if testing_proc.returncode != 0 else None
