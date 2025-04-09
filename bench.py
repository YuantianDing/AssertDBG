

from src import ResultDB
from src.benchmark import bigcodebench

# Login using e.g. `huggingface-cli login` to access this dataset


db = ResultDB("results")
for testcase in bigcodebench.dataset():
	db.run(testcase, verbose=4)