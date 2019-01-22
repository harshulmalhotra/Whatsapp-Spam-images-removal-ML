import os
from PIL import Image, ImageFile
from pytesseract import image_to_string

image_path = 'images\\'
ImageFile.LOAD_TRUNCATED_IMAGES = True

for filename in os.listdir(image_path):  # listdir('.') = current directory
    print(os.path.join(image_path, filename))
    img = Image.open(os.path.join(image_path, filename))
    img.load()
    try:
        result = image_to_string(img, lang='eng',
                                 config='-c '
                                        'tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnozqrstuvwxyz,.')
        if len(result) > 0:
            print(result)
    except IOError:
        print("Problem with file I/O")



    # if "morning" in result.lower():  # detecting good morning images
    #     os.remove(filename)
    # elif len(result) == 0:  # most memes,unwanted images have no text which can extracted..so this!!
    #     os.remove(filename)
