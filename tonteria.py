import numpy as np

def check(p1, p2, base_array):
    """
    Uses the line defined by p1 and p2 to check array of 
    input indices against interpolated value

    Returns boolean array, with True inside and False outside of shape
    """
    idxs = np.indices(base_array.shape) # Create 3D array of indices

    p1 = p1.astype(float)
    p2 = p2.astype(float)

    # Calculate max column idx for each row idx based on interpolated line between two points
    if p1[0] == p2[0]:
        max_col_idx = (idxs[0] - p1[0]) * idxs.shape[1]
        sign = np.sign(p2[1] - p1[1])
    else:
        max_col_idx = (idxs[0] - p1[0]) / (p2[0] - p1[0]) * (p2[1] - p1[1]) + p1[1]
        sign = np.sign(p2[0] - p1[0])
    return idxs[1] * sign <= max_col_idx * sign

def create_polygon(base_array, vertices):
    """
    Creates np.array with dimensions defined by shape
    Fills polygon defined by vertices with ones, all other values zero"""
#    base_array = np.zeros([40,20], dtype=float)  # Initialize your array of zeros

    fill = np.ones(base_array.shape) * True  # Initialize boolean array defining shape fill

    # Create check array for each edge segment, combine into fill array
    for k in range(vertices.shape[0]-1):
        fill = np.all([fill, check(vertices[k], vertices[k+1], base_array)], axis=0)

    # Set all values inside polygon to one
    base_array[fill] = 1

    return base_array


# (Row, Col) Vertices of Polygon (Defined Clockwise)
#vertices = np.array([    [5,12],    [8,16],    [13,14],    [11,6],    [4,6]])
#vertices = np.array([    [25,12],    [28,16],    [33,14],    [31,6],    [24,6]])


#polygon_array = create_polygon(base_array, vertices)



