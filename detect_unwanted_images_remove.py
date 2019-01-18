import os
from PIL import Image
from pytesseract import image_to_string

for index, filename in  enumerate(os.listdir('.')):  #listdir('.') = current directory
        if filename.endswith(".py"):
            continue
        img=Image.open(filename)
        result=image_to_string(img,lang="eng")
    
        if "morning" in result.lower():
            os.remove(filename)
        elif len(result)==0:
            os.remove(filename)