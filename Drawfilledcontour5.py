# -*- coding: utf-8 -*-
  
from numpy import indices as indicess
from numpy import sign as signn
from numpy import zeros
from numpy import ones
from numpy import squeeze
from numpy import all as alll
from numpy import ndarray
from numpy import asarray
from numpy import concatenate
from numpy import rollaxis


def check(p1, p2, base_array):
    """
    Uses the line defined by p1 and p2 to check array of 
    input indices against interpolated value

    Returns boolean array, with True inside and False outside of shape
    """
    idxs = indicess(base_array.shape) # Create 3D array of indices

    p1 = p1.astype(float)
    p2 = p2.astype(float)

    # Calculate max column idx for each row idx based on interpolated line between two points
    if p2[1] == p1[1]:
        max_col_idx = (idxs[0] - p2[1]) * idxs.shape[1]
        sign = signn(p1[0] - p2[0])
    else:
        max_col_idx = (idxs[0] - p2[1]) / (p1[1] - p2[1]) * (p1[0] - p2[0]) + p2[0]
        sign = signn(p1[1] - p2[1])
    return idxs[1] * sign <= max_col_idx * sign



def Drawfilledcontour(zerosarray, vertices, centroid_x, centroid_y):
    """
    Creates np.array with dimensions defined by shape
    Fills polygon defined by vertices with ones, all other values zero"""
    vertices = squeeze(vertices, axis=1)

    centroid = asarray((centroid_x, centroid_y))

    base_array = zerosarray # zeros(shape, dtype=float)  # Initialize your array of zeros

    fill = ones(base_array.shape) * True  # Initialize boolean array defining shape fill

    # Create check array for each edge segment, combine into fill array
    for k in range(len(vertices)):
        base_array[vertices[k][1]][vertices[k][0]] = 1

    for k in range(len(vertices)):
        fill = alll([fill, check(vertices[k-1], vertices[k], base_array)], axis=0)

    # Set all values inside polygon to one
    base_array[fill] = 1

    return base_array







