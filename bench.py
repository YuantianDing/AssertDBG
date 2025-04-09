

from src import ResultDB
from src.benchmark import bigcodebench

# Login using e.g. `huggingface-cli login` to access this dataset

def flatten(l):
	return [item for sublist in l for item in sublist]

db = ResultDB("results")
for c in set(b for a in bigcodebench.dataset() for b in eval(a)):
	print(c)
