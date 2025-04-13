

import json
import traceback

from tinydb import Query
from src import Config, ResultDB, TestResult
from src.benchmark import bigcodebench, humaneval
from pathlib import Path

for directory in [".cache/code_gen", ".cache/debug_loop", ".cache/test_gen"]:
	Path(directory).mkdir(parents=True, exist_ok=True)

dbs = [
    ResultDB("results", Config(True, internal_test_count=2)),
	ResultDB("results", Config(False, internal_test_count=2)),
	ResultDB("results", Config(False, vanilla=True)),
]

for testcase in humaneval.dataset():
	for db in dbs:
		try:
			db.run(testcase, verbose=2)
		except KeyboardInterrupt as e:
			print("KeyboardInterrupt")
			exit(0)
		except Exception as e:
			print(traceback.format_exc())
