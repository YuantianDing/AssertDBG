import json
from typing import Iterator
from datasets import load_dataset
import re
import subprocess
from termcolor import colored
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter

from ..testcase import TestCase


def code_word_replace(code, id1, id2):
    result = "".join(id2 if word == id1 else word for word in re.split(r"(\w+)", code))
    return result

def load(data: dict):
    return TestCase(
        task_id=data['task_id'],
        prompt=data['complete_prompt'],
        solution=data['complete_prompt'] + "\n" + data['canonical_solution'],
        entry_point=data['entry_point'],
        test=data['test'] + "\n\nunittest.main()"
    )

def dataset() -> Iterator[TestCase]:
    for row in load_dataset("bigcode/bigcodebench-hard", cache_dir=".cache")["v0.1.4"]:
        # with open("/tmp/testing_python_program.py", "w") as f:
            # f.write(row['complete_prompt'] + "\n" + row['canonical_solution'])
        
        # p = subprocess.run(["python3", "/tmp/testing_python_program.py"], capture_output=True, timeout=60)
        # if p.returncode != 0:
        #     print(colored("Test Failed: ", "red", attrs=["bold"]) + p.stderr.decode())
        #     continue
            
        yield load(row)
        # yield row['libs']
