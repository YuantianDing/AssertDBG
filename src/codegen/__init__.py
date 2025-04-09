
from .task import task_solve
from .assertgen import assertgen
from .split import split

def code_gen(prompt: str):
    splitted_tasks = split(prompt)
    splitted_tasks.task_func = assertgen(splitted_tasks.task_func)
    splitted_tasks.subfunctions = [assertgen(task_solve(subfunction)) for subfunction in splitted_tasks.subfunctions]

    return "\n\n".join(f.code for f in [splitted_tasks.task_func] + splitted_tasks.subfunctions)


