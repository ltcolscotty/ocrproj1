'''File sorting module'''

import os
cwd = os.getcwd()

import torch
import easyocr
import cv2
import numpy as np
from matplotlib import pyplot as plt
from pathlib import Path
import shutil

comp_roster = os.listdir(f"{cwd}\\sorted_teams\\")

if torch.cuda.is_available():
    reader = easyocr.Reader(['en'], gpu=True)
    print(f"GPU in use: {torch.cuda.get_device_name(0)}")

else:
    reader = easyocr.Reader(['en'], gpu=False)
    print("using CPU, CUDA not available")

unsorted_files_list = os.listdir(f"{cwd}\\unsorted_demo\\")
for file in unsorted_files_list:

    WORKING_IMAGE_PATH = (f"{cwd}\\unsorted_demo\\{file}")
    result = reader.readtext(WORKING_IMAGE_PATH)
    
    #Initiate list for result collection
    answer_list = list()
    
    img = cv2.imread(WORKING_IMAGE_PATH)
    
    #Print results
    if not result:
        print("Empty Results List")
        shutil.copy(f"{cwd}\\unsorted_demo\\{file}", f"{cwd}\\unidentifiable_demo\\{file}")
    else:
        sorted_status = False
        for index, item in enumerate(result):
            if result[index][1].isdigit() and int(result[index][1]) in comp_roster:
                answer_list.append(result[index][1])
                shutil.copy(f"{cwd}\\unsorted_demo\\{file}", f"{cwd}\\sorted_teams\\{int(result[index][1])}\\{file}")
                sorted_status = True
            else:
                print(f"discarding: {result[index][1]}")

        if not sorted_status:
            shutil.copy(f"{cwd}\\unsorted_demo\\{file}", f"{cwd}\\unidentifiable_demo\\{file}")

print("Finished sorting!")

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