import json
import re
import subprocess
from typing import Iterator
from datasets import load_dataset
from ..testcase import TestCase

def load(data: dict):
    return TestCase(
        task_id=data['task_id'],
        prompt=data['prompt'],
        solution=data['prompt'] + "\n" + data["canonical_solution"],
        entry_point=data['entry_point'],
        test=data['test'] + f"\ncheck({data['entry_point']})",
        use=data['prompt'] + "\n    pass\n\n"
    )

def dataset() -> Iterator[TestCase]:
    for row in load_dataset("evalplus/humanevalplus", cache_dir=".cache")['test']:
        testcase = load(row)
        if testcase.task_id == "HumanEval/32":
            testcase.test = testcase.test.replace("_poly(*candidate(*inp), inp)", "_poly(*inp, candidate(*inp))")
        yield testcase

def extract_description(data: dict):
    with open(f"/tmp/print_prompt.py", "w") as f:
        f.write(data['prompt'] + "\n")
        f.write(data['canonical_solution'])
        f.write("\n" * 3)
        f.write(f"print({data['entry_point']}.__doc__)")
        
    proc = subprocess.run(["python3", "/tmp/print_prompt.py"], capture_output=True)
    description = proc.stdout.decode()    
    description = re.sub(r'\n\s*\n', '\n\n', description)
    return description.strip().split("\n\n")[0].split(">>>")[0].split("Example")[0]
