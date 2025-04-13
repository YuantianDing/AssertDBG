
from datetime import timedelta
import subprocess
import traceback

from pydantic_cache import disk_cache
from termcolor import colored
from src.debug.debug import debug
from src.debug.testgen import test_gen
from ..codegen.split import FunctionCode, SplittedTask

@disk_cache(".cache/debug_loop", ttl=timedelta(days=2000))
def debug_loop(attempt: int, prompt: str, code: SplittedTask, use: str, test_count: int = 8, debug_attempts: int = 20, verbose: int = 0) -> bool:
    test_funcs = test_gen(prompt, test_count)
    
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
            except subprocess.TimeoutExpired as e:
                error = traceback.format_exc()
            
            if verbose > 1:
                print(colored(f"Inner Testing Error: {i}", 'red'))
                print(error)
            if not debug(code, testf, error, verbose=verbose):
                return False
    return True
                
    

