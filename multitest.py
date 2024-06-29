import torch
import easyocr

import os
import statistics

import unified_procedure

cwd = os.getcwd()

if torch.cuda.is_available():
    reader = easyocr.Reader(["en"], gpu=True)
    print(f"GPU in use: {torch.cuda.get_device_name(0)}")

else:
    reader = easyocr.Reader(["en"], gpu=False)
    print("using CPU, CUDA not available")

cycles = 5

AR_data = list()
CA_data = list()
OR_data = list()


for run in range(cycles):
    print(f"-----|Testing Cycle {run}|-----")
    unified_procedure.setup_comp(cwd)
    unified_procedure.sort_comp(reader, cwd)
    test_result = unified_procedure.evaluate_test(cwd)
    AR_data.append(test_result[0])
    CA_data.append(test_result[1])
    OR_data.append(test_result[2])

print(f"Avg Attempted Rate: {statistics.mean(AR_data)} | StdDev: {statistics.stdev(AR_data)}")
print(f"Avg Correct Attempted Rate: {statistics.mean(CA_data)} | StdDev: {statistics.stdev(CA_data)}")
print(f"Avg Overall Correctness Rate: {statistics.mean(OR_data)} | StdDev: {statistics.stdev(OR_data)}")