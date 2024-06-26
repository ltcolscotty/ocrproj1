import os
import torch
import easyocr

import sorter_settings

cwd = os.getcwd()

if torch.cuda.is_available():
    reader = easyocr.Reader(["en"], gpu=True)
    print(f"GPU in use: {torch.cuda.get_device_name(0)}")

else:
    reader = easyocr.Reader(["en"], gpu=False)
    print("using CPU, CUDA not available")

non_id_path = f"{cwd}//unidentifiable_demo"
non_id_files = os.listdir(non_id_path)

if len(non_id_files) > 0:
    for file in non_id_files:

else:
    print("Folder seems empty")