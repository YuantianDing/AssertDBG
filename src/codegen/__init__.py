
from datetime import timedelta
from pydantic_cache import disk_cache
from termcolor import colored

from src.my_cache import my_cache
from .task import task_solve
from .assertgen import assertgen
from .split import SplittedTask, split

@my_cache(".cache/code_gen")
def code_gen(attempt: int, prompt: str, with_assert: bool = True, verbose: int = 0) -> SplittedTask:
    if verbose > 1:
        print(colored("LLM Generating Code... ", "yellow", attrs=["bold"]))
    splitted_tasks = split(prompt)
    assert splitted_tasks is not None, "Splitting failed"
    if verbose > 3:
        print(colored("Splitting Result: ", "yellow", attrs=["bold"]))
        splitted_tasks.pretty_print(indent="| ")
        print("\n")
    splitted_tasks.subfunctions = [task_solve(subfunction, splitted_tasks.main_func, remove_assert=not with_assert) for subfunction in splitted_tasks.subfunctions]


    if with_assert:
        splitted_tasks.main_func = assertgen(splitted_tasks.main_func)
        splitted_tasks.subfunctions = [assertgen(subfunction) for subfunction in splitted_tasks.subfunctions]
        
    if verbose > 3:
        print(colored("SubTask Result: ", "yellow", attrs=["bold"]))
        splitted_tasks.pretty_print(indent="| ")
        print("\n")

    fnames = set([splitted_tasks.main_func.function_name] + [f.function_name for f in splitted_tasks.subfunctions])
    assert len(fnames) == len(splitted_tasks.subfunctions) + 1, [splitted_tasks.main_func.function_name] + [f.function_name for f in splitted_tasks.subfunctions]
    return splitted_tasks


