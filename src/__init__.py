from dataclasses import dataclass
import dataclasses
import os
from pydantic import BaseModel
from termcolor import colored
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter
from tinydb import TinyDB, Query

from src.codegen import vanilla
from src.codegen.intentcheck import FunctionCode
from src.codegen.task import task_solve
from src.debug import debug_loop

from . import codegen
from .testcase import TestCase, code_word_replace
import glob

@dataclass
class TestResult:
    task_id: str = None
    function_name: str = None
    code: str = None
    testing: bool = None
    error_message: str = None
    internal_test: str = None
    inner_test_count: str = None

    def set_task_id(self, task_id, show=False):
        self.questions_and_answers = []
        self.task_id = task_id
        if show:
            print(colored("-" * 60 + f" {self.task_id} " + "-" * 60, "yellow"))
    
    
    def set_code(self, function_name, code, show=False):
        self.code = code
        self.function_name = function_name
        if show:
            print(colored(f"Function `{self.function_name}` : ", "green", attrs=["bold"]))
            print(highlight(self.code, PythonLexer(), TerminalFormatter()))

    def set_testing(self, testing, error_message,  show=False):
        # self.testing = testing_count
        self.testing = testing
        self.error_message = error_message
        if show:
            if self.testing:
                print(colored("Test Passed", "green", attrs=["bold"]))
            else:
                print(colored("Test Failed: ", "red", attrs=["bold"]) + self.error_message)

    def show_result(self):
        result = TestResult()
        result.set_task_id(self.task_id, show=True)
        result.set_code(self.function_name, self.code)
        result.set_testing(self.testing, self.error_message, show=True)

@dataclass
class Config:
    with_assert: bool
    vanilla: bool = False
    
    def __str__(self):
        if self.vanilla:
            return 'vanilla'
        return 'with_assert' if self.with_assert else 'no_assert'

class ResultDB:
    def __init__(self, db_path: str, config: Config):
        if not os.path.exists(db_path):
            os.makedirs(db_path)
        self.config = config
        self.db = TinyDB(os.path.join(db_path, str(config) + ".json", ))

    def run(self, testcase: TestCase, verbose: int = 0, rerun: bool=False) -> TestResult:
        result = self.db.get(Query().task_id == testcase.task_id)
        if result and rerun:
            self.db.remove(Query().task_id == testcase.task_id)
        elif result:
            return TestResult(**result)

        result = TestResult()
        result.set_task_id(testcase.task_id, show=verbose > 1)
        code = None
        testing, stderr = None, None
        for attempt in range(3):
            print(colored(f"Attempt {attempt}", attrs=["bold"]))
            test_count = 0
            if self.config.vanilla:
                code = vanilla.vanilla(testcase.prompt)
            else:
                for test_count in range(2):
                    code = solve(testcase, self.config.with_assert, test_count, verbose=verbose)
                    if testcase.run_test(code.code, code.function_name)[0]:
                        break
            testing, stderr = testcase.run_test(code.code, code.function_name)
            result.set_code(code.function_name, code.code, show = verbose > 2)
            result.set_testing(testing, stderr, show=verbose > 1)
            if testing:
                break
            testcase.prompt += " "

        
        self.db.insert(dataclasses.asdict(result))
        return result

def solve(testcase: TestCase, with_assert: bool, internal_test_count: int, verbose: int = 0) -> FunctionCode:
    code = codegen.code_gen(-1, testcase.prompt, with_assert=with_assert, verbose=verbose)
    for i in range(3):
        if debug_loop(i, testcase.prompt, code, testcase.use, with_assert=with_assert, test_count=internal_test_count, verbose=verbose):
            break
        code = codegen.code_gen(i, testcase.prompt, with_assert=with_assert, verbose=verbose)
    
    return FunctionCode(function_name=code.main_func.function_name,
                        code=code_word_replace(code.combine(), "assert", "assert True or ")
                            .replace("raise AssertionError", "assert True or ")
                            .replace("raise ValueError", "assert True or ")
                            .replace("raise Exception", "assert True or "))