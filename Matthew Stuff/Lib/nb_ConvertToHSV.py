
#################################################
### THIS FILE WAS AUTOGENERATED! DO NOT EDIT! ###
#################################################
# file to edit: dev_nb/ConvertToHSV.ipynb
import numpy as np
import matplotlib.pyplot as plt
import cv2

from Lib.nb_PixelManipulation import *
from Lib.nb_HistogramEqualisation import *

def showEachChannel(img, **kwargs):
    plt.figure(figsize=(20,10))
    plt.subplot(1,3,1);
    showImage(img[:, :, 0], **kwargs)
    plt.subplot(1,3,2);
    showImage(img[:, :, 1], **kwargs)
    plt.subplot(1,3,3);
    showImage(img[:, :, 2], **kwargs)

def getHueFromChroma(col_arr : np.array, chroma: np.float32, max_col : np.float32, min_col : np.float32):
    if chroma == 0:
        hue = 255
    elif max_col == 0:
        hue = (col_arr[1] - col_arr[2]) / chroma
        hue %= 6
    elif max_col == 1:
        hue = (col_arr[2] - col_arr[0]) / chroma
        hue += 2
    elif max_col == 2:
        hue = (col_arr[0] - col_arr[1]) / chroma
        hue += 4
    hue *= (255/6)
    return hue

def getSatuationFromChroma(col_arr : np.array, chroma : np.float32, value : np.float32):
    saturation = 0 if value == 0 else (chroma / value) * (255/2)
    return saturation

def convertRGBToHSVColor(colours : np.array):
    col_arr = np.float32(colours)
    min_col = colours.argmin()
    max_col = colours.argmax()
    chroma = col_arr[max_col] - col_arr[min_col]
    hue = getHueFromChroma(col_arr, chroma, max_col, min_col)
    value = np.mean(col_arr)
    saturation = getSatuationFromChroma(col_arr, chroma, value)
    return np.array([hue, saturation, value], dtype = np.uint8)

def convertToHSV(img : np.array):

    img, height, width, channels, im_size = getChannels(img)
    hsv_img = img.copy()
    current_colour = np.ndarray(3, dtype = np.uint8)
    last_channel = channels - 1

    i = 0; j = 0; k = 0
    for px in np.nditer(img):
        current_colour[k] = px
        if (k % channels) == last_channel:
            hsv_img[i, j, :] = convertRGBToHSVColor(current_colour)
        i, j, k = iterateImage(i, j, k, channels, width)
    return hsv_img