from manim import *

def point_to_3d_like(point):
    return point.get_center()

def get_x(point):
    """Accesses the x-coordinates of the point, which are in a wrapper array by default"""
    return point_to_3d_like(point)[0]

def get_y(point):
    """Accesses the y-coordinates of the point, which are in a wrapper array by default"""
    return point_to_3d_like(point)[1]