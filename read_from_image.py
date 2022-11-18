import cv2
import re
from PIL import Image
import pytesseract
import io
import requests
from PIL import Image, ImageEnhance

from IPython.display import display
import PIL.ImageOps
import os
import glob
import concurrent.futures
import time
import numpy as np
Image.LOAD_TRUNCATED_IMAGES = True
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
os.environ['OMP_THREAD_LIMIT'] = '1'
out_dir = "ocr_results//"


# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# noise removal
def remove_noise(image):
    return cv2.medianBlur(image, 5)


# thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


# dilation
def dilate(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)


# erosion
def erode(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(image, kernel, iterations=1)


# opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


# canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)


# skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)

    else:
        angle = -angle
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return rotated


def readImage(imagePath):
    imgText = ""
    """

    :rtype: str
    """
    # url = requests.get(imagePath)
    # img = Image.open(imagePath)
    # i = 0
    # try:
    #     i = img.n_frames
    # except:
    #     i = 1

    # imgText = ""
    
    try:

                #---------------------------------------------------
        image = cv2.imread(imagePath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = 255 - thresholding(gray)

        # Blur and perform text extraction
        thresh = cv2.GaussianBlur(thresh, (3,3), 0)
        imgText = pytesseract.image_to_string(thresh, lang='eng', config='--psm 6')

        #---------------------------------------------------

        # for frame in range(0, i):  # img.n_frames):
        #     img.seek(frame)

        #     # convert to RGB
        #     imgrgb = img.convert('RGB')

        #     # Invert Image
        #     imgrgb = PIL.ImageOps.invert(imgrgb)

        #     # Enhance Brightness
        #     enhancer = ImageEnhance.Brightness(imgrgb)
        #     imgrgb = enhancer.enhance(1.8)

        #     # Enhance Contrast
        #     enhancer = ImageEnhance.Contrast(imgrgb)
        #     imgrgb = enhancer.enhance(4.0)

        #     imgrgb = imgrgb.convert('1')
        #     print(imgrgb)
        #     # display(imgrgb)
            
        #     text = pytesseract.image_to_string(imgrgb)

        #     imgText += text
        #     imgText += "\n"

    except:
        print ("Issue in conversion image - " + imagePath)

    out_file1 = imagePath.split("\\")[-1]
    out_file_name = out_file1.split(".")[0] + ".txt"
    out_path = out_dir + out_file_name
    fd = open(out_path, "w")
    fd.write("%s" % imgText)
    fd.close()

    # print(imgText)
    return imgText


# def main1(img_path):
#     with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
#         executor.submit(readImage(img_path))


def main(path):
    global img_path
    if os.path.isdir(path) == 1:

        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        with concurrent.futures.ProcessPoolExecutor(max_workers=1) as executor:
            image_list = glob.glob(path + "\\*")

            for img_path, text in zip(image_list, executor.map(readImage, image_list)):

                print(img_path.split("\\")[-1], ', processed')


if __name__ == '__main__':
    start = time.time()
    main(path=r"C:\Users\anjali\Desktop\Covert_Image_to_Text\Anjali\1_5DT0111")
    
    end = time.time()
    print(end - start)
