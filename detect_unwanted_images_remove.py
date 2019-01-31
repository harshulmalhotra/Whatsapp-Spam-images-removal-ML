import os
from PIL import Image, ImageFile
from pytesseract import image_to_string, image_to_boxes, image_to_data, Output
import numpy as np
import cv2
from copy import deepcopy

image_path = 'images\\'
ImageFile.LOAD_TRUNCATED_IMAGES = True
tessdata_dir = r'"C:\Users\MrJus\Documents\Whatsapp-Spam-images-removal-ML"'

for filename in os.listdir(image_path):  # listdir('.') = current directory
    print(os.path.join(image_path, filename))

    im_original = cv2.imread(os.path.join(image_path, filename))
    im_white_text = deepcopy(im_original)
    im_black_text = deepcopy(im_original)

    # Gather black text from image
    im_black_text[np.where((np.logical_and(im_black_text >= [0, 0, 0],
                                           im_black_text <= [20, 20, 20]))
                           .all(axis=2))] = [0, 33, 166]
    im_black_text[np.where((im_black_text > [20, 20, 20])
                           .all(axis=2))] = [255, 255, 255]
    im_black_text[np.where((im_black_text == [0, 33, 166])
                           .all(axis=2))] = [0, 0, 0]

    # Gather white text from image
    im_white_text[np.where((np.logical_and(im_white_text <= [255, 255, 255],
                                           im_white_text >= [240, 240, 240]))
                           .all(axis=2))] = [0, 0, 0]
    im_white_text[np.where((np.logical_and(im_white_text < [240, 240, 240],
                                           im_white_text >= [1, 1, 1]))
                           .all(axis=2))] = [255, 255, 255]

    # Get the area taken up by words
    # Pytesseract settings/configurations that will improve accuracy

    try:
        black_text_result = image_to_string(im_black_text, lang='eng',
                                            config=tessdata_dir + ' -c '
                                                                  "tessedit_char_whitelist=\\'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnozqrstuvwxyz,.")
        black_text_result_boxes = image_to_data(im_black_text, lang='eng',
                                                output_type=Output.DICT,
                                                config=tessdata_dir + ' -c '
                                                                      "tessedit_char_whitelist=\\'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnozqrstuvwxyz,.")
        white_text_result = image_to_string(im_white_text, lang='eng',
                                            config=tessdata_dir + ' -c '
                                                                  "tessedit_char_whitelist=\\'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnozqrstuvwxyz,.")

        # Still implementing area of text

        n_boxes = len(black_text_result_boxes['level'])
        for i in range(4, n_boxes):
            (x, y, w, h) = (
                black_text_result_boxes['left'][i],
                black_text_result_boxes['top'][i],
                black_text_result_boxes['width'][i],
                black_text_result_boxes['height'][i])
            cv2.rectangle(im_black_text, (x, y), (x + w, y + h), (0, 255, 0),
                          2)

        # if len(result) > 0:
        print(black_text_result)
        print(white_text_result)
        print(black_text_result_boxes)
    except IOError:
        print("Problem with file I/O")

    cv2.imshow('image_origin', im_original)
    cv2.imshow('image_white_text', im_white_text)
    cv2.imshow('image_black_text', im_black_text)
    cv2.waitKey(2500)
    cv2.destroyAllWindows()
