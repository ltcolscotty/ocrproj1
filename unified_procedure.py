"""
Module for putting all code together
"""

import os
from pathlib import Path
import shutil
import random

import sorter_settings

import cv2
import easyocr


def clear_folder(cwd, folder_directory):
    """
    Clears folder

    Args:
    - ``cwd``: Current Working Directory
    - ``folder_directory``: folder that you want to clear relative to ``cwd``
    """
    unsorted_files = os.listdir(f"{cwd}\\{folder_directory}\\")
    if len(unsorted_files) > 0:
        for filename in unsorted_files:
            file_path = os.path.join(f"{cwd}\\{folder_directory}\\", filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print("Failed to delete %s. Reason: %s" % (file_path, e))
        print("Successfully cleared folder 'unsorted files'")
    else:
        print("No files removed for unsorted files: Length = 0")


def setup_comp(cwd):
    """
    Sets up competition.

    Args:
        - cwd: Current Working Directory
    """
    # Number of competitors
    comp_num = 35
    comp_roster = list()
    file_list = os.listdir(f"{cwd}\{sorter_settings.library}\\")

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
    clear_folder(cwd, sorter_settings.unsorted)

    # Clear files from sorted folder
    clear_folder(cwd, sorter_settings.sorted_destination)

    # Clear files from unidentifiable folder
    clear_folder(cwd, sorter_settings.non_IDable)

    for team in comp_roster:
        Path(f"{cwd}/{sorter_settings.sorted_destination}/{str(team)}").mkdir(
            parents=True, exist_ok=True
        )
        # print(f"Created folder for {team}")

    # MANAGES SETTING UP AND MOVING IMAGES
    selected_file_list = list()

    for team in comp_roster:
        for file in file_list:
            if file.startswith(f"{str(team)}_"):
                selected_file_list.append(file)

    for file in selected_file_list:
        shutil.copy(
            f"{cwd}\{sorter_settings.library}\\{file}",
            f"{cwd}\\{sorter_settings.unsorted}\\",
        )

    print("Setup Complete!")


def sort_comp(reader: easyocr.Reader, cwd):
    """
    Sorts competition generated initially

    Args:
        reader: easyocr.Reader - easyocr reader object
        cwd: Current Working Directory
    """

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
                """else:
                    print(f"discarding: {result[index][1]}")"""

            if not sorted_status:
                shutil.copy(
                    f"{cwd}\\{sorter_settings.unsorted}\\{file}",
                    f"{cwd}\\{sorter_settings.non_IDable}\\{file}",
                )

    print("Finished sorting!")


def evaluate_test(cwd):
    """
    Evaluates test

    Args:
        cwd: Current Working Directory

    Returns:
        Tuple: Attempted Rate, Correct Attempted, Overall Rate
    """
    print("Starting evaluation")
    # Evaluate Correct
    sfll = os.listdir(f"{cwd}\\{sorter_settings.sorted_destination}\\")
    c_counter = 0
    for folder in sfll:
        ifile_list = os.listdir(
            f"{cwd}\\{sorter_settings.sorted_destination}\\{folder}"
        )
        for file in ifile_list:
            if len(ifile_list) > 0:
                if file.partition("_")[0] == folder:
                    c_counter += 1

    # Results
    unsorted_files = os.listdir(f"{cwd}\\{sorter_settings.unsorted}\\")
    correct = len(unsorted_files) - len(
        os.listdir(f"{cwd}\\{sorter_settings.non_IDable}\\")
    )
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

    return (atr, car, overall_acc)
