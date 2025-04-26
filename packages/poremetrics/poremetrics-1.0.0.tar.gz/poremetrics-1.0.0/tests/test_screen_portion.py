from poremetrics import screen_portion
import numpy as np
from . import shapes
from . import parameters

def test_square():
    square = shapes.make_rectangle(x_length=100,y_length=100)
    assert screen_portion(square)>=(1024**2/100**2)*parameters.UPPER_BOUND_SCALE
    assert screen_portion(square)>=(1024**2/100**2)*parameters.LOWER_BOUND_SCALE