from poremetrics import perimeter
import numpy as np
import math
from . import shapes
from . import parameters

def test_square():
    square = shapes.make_rectangle(x_length=100,y_length=200)
    assert perimeter(square)>=(100*2+200*2)*parameters.LOWER_BOUND_SCALE
    assert perimeter(square)<=(100*2+200*2)*parameters.UPPER_BOUND_SCALE
def test_circle():
    circle = shapes.make_circle(radius=100)
    assert perimeter(circle)>=2*math.pi*100*parameters.LOWER_BOUND_SCALE
    assert perimeter(circle)<=2*math.pi*100*parameters.UPPER_BOUND_SCALE
    