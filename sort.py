"""File sorting module"""

import os

cwd = os.getcwd()

import easyocr
import cv2
import shutil

import sorter_settings

def sort_comp(reader: easyocr.Reader):
    '''
    Sorts competition generated initially

    Args:
        reader: easyocr.Reader - easyocr reader object
    '''

    comp_roster = os.listdir(f"{cwd}\\{sorter_settings.sorted_destination}\\")

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
                '''else:
                    print(f"discarding: {result[index][1]}")'''

            if not sorted_status:
                shutil.copy(
                    f"{cwd}\\{sorter_settings.unsorted}\\{file}",
                    f"{cwd}\\{sorter_settings.non_IDable}\\{file}",
                )

    print("Finished sorting!")

