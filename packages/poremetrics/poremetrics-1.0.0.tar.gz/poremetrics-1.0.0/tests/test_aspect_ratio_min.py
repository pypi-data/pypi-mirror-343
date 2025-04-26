# %%
from poremetrics import aspect_ratio_min
from . import shapes
from . import parameters
import numpy as np
import scipy.ndimage

def test_square():
    square = shapes.make_rectangle()
    assert aspect_ratio_min(square)==1
def test_circle():
    circle = shapes.make_circle()
    assert aspect_ratio_min(circle)==1

def test_oval():
    oval = shapes.make_oval()
    assert aspect_ratio_min(oval)>=2*parameters.LOWER_BOUND_SCALE
    assert aspect_ratio_min(oval)<=2*parameters.UPPER_BOUND_SCALE

def test_rotated_oval():
    oval = shapes.make_oval()
    oval_rotated = scipy.ndimage.rotate(oval,angle=30)
    assert aspect_ratio_min(oval_rotated)>=2*parameters.LOWER_BOUND_SCALE
    assert aspect_ratio_min(oval_rotated)<=2*parameters.UPPER_BOUND_SCALE

def test_rectangle_rotated():
    rectangle = shapes.make_rectangle(x_length=100,y_length=200)
    rectangle_rotated = scipy.ndimage.rotate(rectangle,angle=30)
    assert aspect_ratio_min(rectangle_rotated)>=2*parameters.LOWER_BOUND_SCALE
    assert aspect_ratio_min(rectangle_rotated)<=2*parameters.UPPER_BOUND_SCALE