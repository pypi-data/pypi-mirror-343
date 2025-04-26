import cv2
import numpy as np
def centroid(array):
    x = np.sum(array,axis=0)
    y = np.sum(array,axis=1)
    return (x,y)
