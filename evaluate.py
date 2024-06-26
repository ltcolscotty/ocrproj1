"""
evaluation module
"""

import os
import sorter_settings

cwd = os.getcwd()
print("Starting evaluation")

# Evaluate Correct
sfll = os.listdir(f"{cwd}\\{sorter_settings.sorted_destination}\\")
c_counter = 0
for folder in sfll:
    ifile_list = os.listdir(f"{cwd}\\{sorter_settings.sorted_destination}\\{folder}")
    for file in ifile_list:
        if len(ifile_list) > 0:
            if file.partition("_")[0] == folder:
                c_counter += 1

# Results
unsorted_files = os.listdir(f"{cwd}\\{sorter_settings.unsorted}\\")
correct = len(unsorted_files) - len(os.listdir(f"{cwd}\\{sorter_settings.non_IDable}\\"))
atr = (correct) / len(unsorted_files)
overall_acc = c_counter / len(unsorted_files)
car = overall_acc / atr
print("---Summary Start---")
print(f"Attempted Rate: {atr}")
print(f"AR(Fraction): {correct}/{len(unsorted_files)}")
print("---")
print(f"Correct Attempted: {car}")
print(f"CA (Fraction): {c_counter}/{correct}")
print("---")
print(f"Overall Correct: {overall_acc}")
print(f"OC (Fraction): {c_counter}/{len(unsorted_files)}")
print("---Summary End---")
