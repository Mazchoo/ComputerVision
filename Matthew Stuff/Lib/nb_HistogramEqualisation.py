
#################################################
### THIS FILE WAS AUTOGENERATED! DO NOT EDIT! ###
#################################################
# file to edit: dev_nb/HistogramEqualisation.ipynb
import numpy as np
import matplotlib.pyplot as plt
import cv2

from dataclasses import dataclass

from Lib.nb_PixelManipulation import *


@dataclass
class ChannelRange:
    c_range: np.array = np.array([], dtype = np.uint8)

    def __len__(self):
        return len(self.c_range) // 2

    def __getitem__(self, idx):
        return self.c_range[idx*2:idx*2 + 2]

    def checkLength(self):
        if self.c_range % 2 != 0: print('Length is not even!')


def getScalars(c_range : ChannelRange, channels : int):
    scalars = np.ndarray(channels, dtype = np.uint8)
    for k in range(channels): scalars[k] = 255 // (c_range[k][1] - c_range[k][0])
    return scalars

def putPixelInRange(px : int, channel_range: np.array, scalar : int):
    lower, upper = channel_range
    if px < lower: return np.uint8(0)
    if px > upper: return np.uint8(255)
    return np.uint8((px - lower)*scalar)

def enhanceContrast(img : np.array, channel_range : ChannelRange):
    img, height, width, channels, im_size = getChannels(img)
    scalars = getScalars(channel_range, channels)

    i = 0; j = 0; k = 0;
    for px in np.nditer(img):
        img[i, j, k] = putPixelInRange(px, channel_range[k], scalars[k])
        i, j, k = iterateImage(i, j, k, channels, width)
    return img

def compareTwoImages(im_x, im_y):
    plt.figure(figsize=(20,10))
    plt.subplot(1,2,1);
    showImage(im_x)
    plt.subplot(1,2,2);
    showImage(im_y)