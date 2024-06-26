import os

import torch
import easyocr
import cv2
from matplotlib import pyplot as plt

import sorter_settings

cwd = os.getcwd()

if torch.cuda.is_available():
    reader = easyocr.Reader(["en"], gpu=True)
    print(f"GPU in use: {torch.cuda.get_device_name(0)}")

else:
    reader = easyocr.Reader(["en"], gpu=False)
    print("using CPU, CUDA not available")

non_id_path = f"{cwd}//{sorter_settings.non_IDable}"
non_id_files = os.listdir(non_id_path)

if len(non_id_files) > 0:

    print(f"Reviewing: {len(non_id_files)} files")

    for file in non_id_files:
        
        print(f"File: {file}")

        result = reader.readtext(f"{cwd}//{sorter_settings.non_IDable}//{file}")

        # Initiate list for result collection
        bottom_right_list = list()
        top_left_list = list()
        index_list = list()
        answer_list = list()

        img = cv2.imread(f"{cwd}//{sorter_settings.non_IDable}//{file}")

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

        print("--- NEXT IMAGE ---")
    print("--- END OF REVIEW ---")

else:
    print("Folder seems empty")