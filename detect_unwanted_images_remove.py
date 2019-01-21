import os
from PIL import Image
from pytesseract import image_to_string

for index, filename in enumerate(os.listdir('.')):  #listdir('.') = current directory
    if filename.endswith(".py"):     #some python files can also be in directory..so to ignore that
        continue
    img = Image.open(filename)
    result = image_to_string(img,lang="eng")

    if "morning" in result.lower():      #detecting good morning images
        os.remove(filename)
    elif len(result) == 0:            #most memes,unwanted images have no text which can extracted..so this!!
        os.remove(filename)
