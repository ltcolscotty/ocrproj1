import os

import torch
import easyocr
import cv2
import numpy as np
from matplotlib import pyplot as plt
from pathlib import Path
import shutil

import random

cwd = os.getcwd()

if torch.cuda.is_available():
    reader = easyocr.Reader(['en'], gpu=True)
    print(f"GPU in use: {torch.cuda.get_device_name(0)}")

else:
    reader = easyocr.Reader(['en'], gpu=False)
    print("using CPU, CUDA not available")

#ROSTER GENERATOR & FOLDER RESETTER

#Number of competitors
comp_num = 35
comp_roster = list()
file_list = os.listdir(f"{cwd}\image_library\\")

for x in range(comp_num):
    valid_team = False
    while not valid_team:
        team = random.randint(1, 9785)
        if team in comp_roster:
            valid_team = False
        else:
            for file in file_list:
                if file.startswith(str(team) + "_"):
                    valid_team = True
                    comp_roster.append(team)
                    break
                else:
                    valid_team = False

print("Generated new roster!")

# Clear files in unsorted folder
unsorted_files = os.listdir(f"{cwd}\\unsorted_demo\\")
if len(unsorted_files) > 0:
    for filename in unsorted_files:
        file_path = os.path.join(f"{cwd}\\unsorted_demo\\", filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    print("Successfully cleared folder 'unsorted files'")
else:
    print("No files removed for unsorted files: Length = 0")

# Clear files from sorted folder
sorted_files = os.listdir(f"{cwd}\\sorted_teams\\")
if len(sorted_files) > 0:
    for filename in sorted_files:
        file_path = os.path.join(f"{cwd}\\sorted_teams\\", filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    print("Successfully cleared folder 'sorted files'")
else:
    print("No files removed for sorted folder: Length = 0")

# Clear files from unidentifiable folder
unidentifiable_files = os.listdir(f"{cwd}\\unidentifiable_demo\\")
if len(unidentifiable_files) > 0:
    for filename in unidentifiable_files:
        file_path = os.path.join(f"{cwd}\\unidentifiable_demo\\", filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    print("Successfully cleared folder 'unidentifiable'")
else:
    print("No files removed for unidentifiable folder: Length = 0")

for team in comp_roster:
    Path(f"{cwd}/sorted_teams/{str(team)}").mkdir(parents=True, exist_ok=True)
    print(f"Created folder for {team}")


# MANAGES SETTING UP AND MOVING IMAGES
selected_file_list = list()

for team in comp_roster:
    for file in file_list:
        if file.startswith(f"{str(team)}"):
            selected_file_list.append(file)

for file in selected_file_list:
    shutil.copy(f"{cwd}\image_library\\{file}", f"{cwd}\\unsorted_demo\\")


print("Setup Complete!")