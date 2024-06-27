import torch
import easyocr

import setup
import sort
import evaluate

import statistics

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
    setup.setup_comp()
    sort.sort_comp(reader)
    test_result = evaluate.evaluate_test()
    AR_data.append(test_result[0])
    CA_data.append(test_result[1])
    OR_data.append(test_result[2])

print(f"Avg Attempted Rate: {statistics.mean(AR_data)}")
print(f"Avg Correct Attempted Rate: {statistics.mean(CA_data)}")
print(f"Avg Overall Correctness Rate: {statistics.mean(OR_data)}")