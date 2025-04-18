
from datetime import timedelta
import subprocess
import traceback

from pydantic_cache import disk_cache
from termcolor import colored
from src.debug.debug import debug
from src.debug.testgen import test_gen
from ..codegen.split import FunctionCode, SplittedTask



def debug_loop(attempt: int, prompt: str, code: SplittedTask, use: str, with_assert: bool, test_count: int, debug_attempts: int = 10, verbose: int = 0) -> bool:
    test_funcs = [test_gen(i, prompt, add_error_msg=with_assert) for i in range(test_count)]
    timeout_limit = 3
    for testf in test_funcs:
        if verbose > 5:
            print(colored("Testing", "yellow", attrs=["bold"]))
            testf.pretty_print()
        for i in range(debug_attempts):
            with open("/tmp/assertdbg.py", "w") as f:
                f.write(use + "\n\n")
                f.write(code.combine())
                f.write("\n\n")
                f.write(testf.code)
                f.write(f"\n{testf.function_name}()\n")
            testing_proc = None

            try:
                testing_proc = subprocess.run(["python3", "/tmp/assertdbg.py"], capture_output=True, timeout=60)
                if testing_proc.returncode == 0:
                    if verbose > 1:
                        print(colored("Inner Testing Passed! ", 'green'))
                    break

                error = testing_proc.stderr.decode()
                timeout_limit = 3
            except subprocess.TimeoutExpired as e:
                error = traceback.format_exc()
                timeout_limit -= 1
                if timeout_limit == 0:
                    return True
            if verbose > 1:
                print(colored(f"Inner Testing Error: {i}", 'red'))
                print(error)
            action = debug(code, testf, error, verbose=verbose)
            print("A")
            if not action.perform(code, testf, verbose=verbose):
                return False
    return True
                
    

