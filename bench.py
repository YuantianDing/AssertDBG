

import json
import os
import random
import subprocess
import traceback

from termcolor import colored
from tinydb import Query
from src import Config, ResultDB, TestResult
from src.benchmark import bigcodebench, humaneval
from pathlib import Path


for directory in [".cache/code_gen", ".cache/debug", ".cache/test_gen", ".cache/vanilla", ".bench", ".test"]:
	Path(directory).mkdir(parents=True, exist_ok=True)

dbs = [
    ResultDB("results", Config(True)),
	# ResultDB("results", Config(False)),
	# ResultDB("results", Config(False, vanilla=True)),
]

ds = list(humaneval.dataset())
for ts in ds:
	if os.path.exists(f'.bench/{ts.task_id.replace("/", "_")}.py'):
		continue
	with open(f'.bench/{ts.task_id.replace("/", "_")}.py', "w") as f:
		f.write(ts.solution + "\n\n")
		f.write(ts.test + "\n\n")
	print(colored("Testing packages: ", "yellow", attrs=["bold"]), ts.task_id)
	proc = subprocess.run(["python3", f".bench/{ts.task_id.replace('/', '_')}.py"], capture_output=True)
	if proc.returncode != 0:
		print(colored("Test Failed: ", "red", attrs=["bold"]))
		print(proc.stderr.decode())
		os.remove(f'.bench/{ts.task_id.replace("/", "_")}.py')

for testcase in ds:
	for db in dbs:
		try:
			db.run(testcase, verbose=2)
		except KeyboardInterrupt as e:
			print("KeyboardInterrupt")
			exit(0)
		except Exception as e:
			print(traceback.format_exc())
