"""File sorting module"""

import os

cwd = os.getcwd()

import torch
import easyocr
import cv2
import shutil

import sorter_settings

comp_roster = os.listdir(f"{cwd}\\{sorter_settings.sorted_destination}\\")

if torch.cuda.is_available():
    reader = easyocr.Reader(["en"], gpu=True)
    print(f"GPU in use: {torch.cuda.get_device_name(0)}")

else:
    reader = easyocr.Reader(["en"], gpu=False)
    print("using CPU, CUDA not available")

unsorted_files_list = os.listdir(f"{cwd}\\{sorter_settings.unsorted}\\")
for file in unsorted_files_list:

    WORKING_IMAGE_PATH = f"{cwd}\\{sorter_settings.unsorted}\\{file}"
    result = reader.readtext(WORKING_IMAGE_PATH)

    # Initiate list for result collection
    answer_list = list()

    img = cv2.imread(WORKING_IMAGE_PATH)

    # Print results
    if not result:
        print("Empty Results List")
        shutil.copy(
            f"{cwd}\\{sorter_settings.unsorted}\\{file}",
            f"{cwd}\\{sorter_settings.non_IDable}\\{file}",
        )
    else:
        sorted_status = False
        for index, item in enumerate(result):
            result[index][1]
            if (
                str(result[index][1]).replace(" ", "").isdigit()
                and str(result[index][1]).replace(" ", "") in comp_roster
            ):
                answer_list.append(str(result[index][1]).replace(" ", ""))
                shutil.copy(
                    f"{cwd}\\{sorter_settings.unsorted}\\{file}",
                    f"{cwd}\\{sorter_settings.sorted_destination}\\{str(result[index][1]).replace(' ','')}\\{file}",
                )
                sorted_status = True
            else:
                print(f"discarding: {result[index][1]}")

        if not sorted_status:
            shutil.copy(
                f"{cwd}\\{sorter_settings.unsorted}\\{file}",
                f"{cwd}\\{sorter_settings.non_IDable}\\{file}",
            )

print("Finished sorting!")
