'''
evaluation module
'''

import os

import torch
import easyocr
import cv2
import numpy as np
from matplotlib import pyplot as plt
from pathlib import Path
import shutil


cwd = os.getcwd()
print("Starting evaluation")

# Evaluate Correct
sfll = os.listdir(f"{cwd}\\sorted_teams\\")
c_counter = 0
for folder in sfll:
    ifile_list = os.listdir(f"{cwd}\\sorted_teams\\{folder}")
    for file in ifile_list:
        if len(ifile_list) > 0:
            if file.partition('_')[0] == folder:
                c_counter += 1

# Results
unsorted_files = os.listdir(f"{cwd}\\unsorted_demo\\")
correct = len(unsorted_files)-len(os.listdir(f"{cwd}\\unidentifiable_demo\\"))
atr = (correct)/len(unsorted_files)
overall_acc = (c_counter/len(unsorted_files))
car = overall_acc/atr
print("---Summary Start---")
print(f"Attempted Rate: {atr}")
print (f"AR(Fraction): {correct}/{len(unsorted_files)}")
print("---")
print(f"Correct Attempted: {car}")
print(f"CA (Fraction): {correct}/{c_counter}")
print("---")
print(f"Overall Correct: {overall_acc}")
print(f"OC (Fraction): {c_counter}/{len(unsorted_files)}")
print("---Summary End---")