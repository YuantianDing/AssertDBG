from dataclasses import dataclass
import dataclasses
import os
from termcolor import colored
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter
from tinydb import TinyDB, Query

from . import codegen
from .testcase import TestCase

@dataclass
class TestResult:
    task_id: str = None
    function_name: str = None
    code: str = None
    testing: bool = None
    error_message: str = None

    def set_task_id(self, task_id):
        self.questions_and_answers = []
        self.task_id = task_id
        print(colored("-" * 60 + f" {self.task_id} " + "-" * 60, "yellow"))
    
    
    def set_code(self, function_name, code):
        self.code = code
        self.function_name = function_name
        print(colored(f"Function `{self.function_name}` : ", "green", attrs=["bold"]))
        print(highlight(self.code, PythonLexer(), TerminalFormatter()))

    def set_testing(self, testing, error_message=None):
        self.testing = testing
        self.error_message = error_message
        if self.testing:
            print(colored("Test Passed", "green", attrs=["bold"]))
        else:
            print(colored("Test Failed: ", "red", attrs=["bold"]) + self.error_message)

    def show_result(self):
        result = TestResult()
        result.set_task_id(self.task_id, self.code_model, self.question_limit)
        for q, a in self.questions_and_answers:
            result.add_questions_and_answers(q, a)
        result.set_code(self.function_name, self.code)
        result.set_testing(self.testing, self.error_message)


class ResultDB:
    def __init__(self, db_path: str, config: str = 'default'):
        if not os.path.exists(db_path):
            os.makedirs(db_path)
        self.db = TinyDB(os.path.join(db_path, config + ".json", ))

    def run(self, testcase: TestCase):
        result = self.db.get(Query().task_id == testcase.task_id)
        if result:
            return TestResult(**result[0])

        result = TestResult()
        result.set_task_id(testcase.task_id)
        code = codegen.code_gen(testcase.prompt)
        result.set_code(testcase.entry_point, code)

        result.set_testing(*testcase.run_test(code, testcase.entry_point))
        self.db.insert(dataclasses.asdict(result))
        return result

