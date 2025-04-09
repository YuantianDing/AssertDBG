
from termcolor import colored
from .task import task_solve
from .assertgen import assertgen
from .split import split

def code_gen(prompt: str, verbose: int = 0) -> str:
    splitted_tasks = split(prompt)
    if verbose > 3:
        print(colored("Splitting Result: ", "yellow", attrs=["bold"]))
        splitted_tasks.pretty_print(indent="| ")
        print("\n")
    splitted_tasks.subfunctions = [task_solve(subfunction, splitted_tasks.task_func) for subfunction in splitted_tasks.subfunctions]

    if verbose > 3:
        print(colored("SubTask Result: ", "yellow", attrs=["bold"]))
        splitted_tasks.pretty_print(indent="| ")
        print("\n")

    splitted_tasks.task_func = assertgen(splitted_tasks.task_func)
    splitted_tasks.subfunctions = [assertgen(subfunction) for subfunction in splitted_tasks.subfunctions]

    return splitted_tasks.combine()


