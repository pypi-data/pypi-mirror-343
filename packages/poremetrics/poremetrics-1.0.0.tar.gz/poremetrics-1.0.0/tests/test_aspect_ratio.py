from poremetrics import aspect_ratio
from . import shapes
from . import parameters
import numpy as np

def test_square():
    square = shapes.make_rectangle()
    assert aspect_ratio(square)==1
def test_circle(): 
    circle = shapes.make_circle()
    assert aspect_ratio(circle)==1
def test_oval(): 
    oval = shapes.make_oval()
    assert aspect_ratio(oval)>=2*parameters.LOWER_BOUND_SCALE
    assert aspect_ratio(oval)<=2*parameters.UPPER_BOUND_SCALE
def test_equilateral_triangle():
    equilateral_triangle = shapes.make_equilateral_triangle(height=100,base=200)
    assert aspect_ratio(equilateral_triangle)>=2*parameters.LOWER_BOUND_SCALE
    assert aspect_ratio(equilateral_triangle)<=2*parameters.UPPER_BOUND_SCALE