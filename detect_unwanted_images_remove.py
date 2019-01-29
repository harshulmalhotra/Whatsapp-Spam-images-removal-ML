import os
from PIL import Image, ImageFile
from pytesseract import image_to_string, image_to_data
import numpy as np
import cv2


image_path = 'images\\'
ImageFile.LOAD_TRUNCATED_IMAGES = True
tessdata_dir = r'"C:\Users\MrJus\Documents\Whatsapp-Spam-images-removal-ML"'

for filename in os.listdir(image_path):  # listdir('.') = current directory
    print(os.path.join(image_path, filename))

    im = cv2.imread(os.path.join(image_path, filename))

    im[np.where((np.logical_and(im >= [0, 0, 0], im <= [20, 20, 20]))
                .all(axis=2))] = [0, 33, 166]
    im[np.where((im > [20, 20, 20])
                .all(axis=2))] = [255, 255, 255]
    im[np.where((im == [0, 33, 166])
                .all(axis=2))] = [0, 0, 0]

    try:
        result = image_to_string(im, lang='eng',
                                 config=tessdata_dir + ' -c '
                                        "tessedit_char_whitelist=\\'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnozqrstuvwxyz,.")
        if len(result) > 0:
             print(result)
    except IOError:
        print("Problem with file I/O")

    cv2.imshow('image', im)
    cv2.waitKey(5000)
    cv2.destroyAllWindows()