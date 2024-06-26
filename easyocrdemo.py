"""demo module"""

import os

cwd = os.getcwd()

import sorter_settings

import torch
import easyocr
import cv2
import numpy as np
from matplotlib import pyplot as plt
from pathlib import Path

import time

file = input("Input file name relative to image_library: ")

library = os.listdir(f"{cwd}\{sorter_settings.library}\\")

if torch.cuda.is_available():
    reader = easyocr.Reader(["en"], gpu=True)
    print(f"GPU in use: {torch.cuda.get_device_name(0)}")

else:
    reader = easyocr.Reader(["en"], gpu=False)
    print("using CPU, CUDA not available")

# Set image here
if file in library:
    IMAGE_PATH = f"{cwd}\{sorter_settings.library}\\{file}"
else:
    print("File not recognized, using default image. Remeber to include file suffix.")
    IMAGE_PATH = f"{cwd}\{sorter_settings.library}\\1_0.webp"
result = reader.readtext(IMAGE_PATH)

# Initiate list for result collection
bottom_right_list = list()
top_left_list = list()
index_list = list()
answer_list = list()

img = cv2.imread(IMAGE_PATH)

# Print results
if not result:
    print("Empty Results List")
else:
    for index, item in enumerate(result):
        if str(result[index][1]).replace(' ', '').isdigit():
            bottom_right_list.append(tuple(result[index][0][2]))
            top_left_list.append(tuple(result[index][0][0]))
            answer_list.append(result[index][1])
        else:
            print(f"discarding: {result[index][1]}")

        # Display Settings
        font = cv2.FONT_HERSHEY_SIMPLEX

        # Add labels
        for idx, answer in enumerate(answer_list):
            img = cv2.rectangle(
                img,
                tuple(map(int, top_left_list[idx])),
                tuple(map(int, bottom_right_list[idx])),
                (0, 225, 0),
                5,
            )
            img = cv2.putText(
                img,
                answer_list[idx],
                tuple(map(int, top_left_list[idx])),
                font,
                1.5,
                (255, 255, 255),
                3,
            )

plt.imshow(img)
plt.show()