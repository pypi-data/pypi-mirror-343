from poremetrics import validate
import numpy as np
import cv2
from . import shapes

def test_color_channels():
    path = shapes.get_file_path("filled.png")
    color_img = cv2.imread(path)
    grayscale_img = cv2.imread(path,cv2.IMREAD_GRAYSCALE)
    assert not validate(color_img)
    assert validate(grayscale_img)
def test_wrong_type():
    incorrect = np.zeros((1024,1024),np.int8)
    correct = np.zeros((1024,1024),np.uint8)
    assert not validate(incorrect)
    assert validate(correct)
def test_other_values():
    zeros = np.zeros((1024,1024),np.uint8)
    ons = np.full(shape=(1024,1024),fill_value=255,dtype=np.uint8)
    others = np.zeros((1024,1024),np.uint8)
    others[0:100,0:100]=100
    others[101:200,101:200]=200
    others[400:500,400:500]=255
    zeros_and_ons = zeros
    zeros_and_ons[500:600,500:600]=255
    assert validate(zeros)
    assert validate(ons)
    assert validate(zeros_and_ons)
    assert not validate(others)
