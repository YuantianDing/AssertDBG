

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
	ResultDB("results", Config(False)),
	ResultDB("results", Config(False, vanilla=True)),
]

print([db.db.count(Query().testing == False) for db in dbs])
print([len(db.db) for db in dbs])