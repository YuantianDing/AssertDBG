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
