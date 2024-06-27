# ocrproj1

Demo of using easyocr to assist the automation of sorting photos for FRC

### Requirements:
- Files may have any suffix readable by matplotlib. Recommended usage of:
    - ``.webp``
    - ``.png``
    - ``.jpg``

### New required packages:
- ``torch`` - Pytorch - GPU Acceleration (Files may be modified if ONLY CPUs will be used)
- ``easyocr`` - EasyOCR - Vision Package
- ``cv2`` - OpenCV - image manipulation
- ``shutil`` - File management (Pathlib may also be used, current code uses shutil for file management)

### Demo Essentials:
- Image library
    - Images labelled with the format [team_number]_[extra info], eg. (```1318_1.png```)

### Essentials for an implementation:
- Unsorted dump folder
- Unidentifiable folder
- 'Sorted' folder containing subfolders with team numbers

## How to run a demo:
Be sure to read [demo essentials](#demo-essentials)

1. Modify the number of cycles you want to test in ``multitest.py``
2. Run ``multitest.py``

## How to configure for usage:
Be sure to read [implementation essentials](#essentials-for-an-implementation)

### Setup
- Create a dump folder for unsorted images
- Use the viewer to create image folders for competition inside a designated 'sorted' directory
- Create a folder for images the program can't identify
- Use ``Sort.py``'s code to create a program that sorts out images from the dump folder
- Update ``Sorter_settings.py`` to use appropriate folders/paths

### Final Result
- Dump folder
- Sorted folder
- Unidentifiable folder
- Designated sorter program/package command
- ``Sorter_settings.py`` is configured
- Review.py, setup.py, evaluate.py, easyocrdemo.py, and the image library are deleted

## Theoretical usage at competition:
After [configuring for usage](#how-to-configure-for-usage)
1. Pit scouting data is entered in
2. Viewer is used to create folders for team images
3. Sorter program is run (eg. ``viz25 sort``)
4. Remaining images are manually sorted out

### Ways to reduce mis-matches and non-identifiables:
- Bumpers MUST BE ON with numbers visible and non-separated
- Have clear text somewhere in the image containing the team number
    - whiteboard with team number written somewhat neatly if the font on the bumpers is confusing
- Other team numbers are blocked out
    - Take pictures in the pits
    - Minimal angle (robot shouldn't be diagonal, etc.)
    - Decent lighting (Not excessively dark)
- Gamepieces with year numbers shouldn't be in the photo

## How sorting works
1. Get image, run through EasyOCR
    - EasyOCR returns every piece of text it can identify with related bounding box of where it found said text
    - Included text AND numbers
2. Filter out text containing alphabetical characters, numbers with spaces inbetween them are okay
3. Remove spaces inbetween the numbers. At this point, all results should be numbers without spaces
4. In one image, go through the results. If a result matches a team in the team roster, copy the image to that team's image folder
5. If the results list is empty or contains number sequences not in the team roster, the team is unidentifiable by the program

    
