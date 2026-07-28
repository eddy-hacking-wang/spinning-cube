def access_contents(point):
    """Accesses the coordinates of the structure, which are in a wrapper array by default"""
    return point[0]

def get_x(point):
    """Accesses the x-coordinates of the point, which are in a wrapper array by default"""
    return access_contents(point)[0]

def get_y(point):
    """Accesses the y-coordinates of the point, which are in a wrapper array by default"""
    return access_contents(point)[1]