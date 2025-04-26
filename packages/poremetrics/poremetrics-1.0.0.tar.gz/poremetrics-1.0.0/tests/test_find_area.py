from poremetrics import pixel_area
import numpy as np
from . import shapes

def test_square():
    square = shapes.make_rectangle(x_length=100,y_length=100)
    assert pixel_area(square)==100*100
