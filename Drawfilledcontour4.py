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



def Drawfilledcontour(zerosarray, vertices, centroid_x, centroid_y):
    """
    Creates np.array with dimensions defined by shape
    Fills polygon defined by vertices with ones, all other values zero"""
    vertices = squeeze(vertices, axis=1)

#    vertices = ndarray.tolist(vertices)
#    t = []
#    for i in range(len(vertices)):
#        for j in vertices:
#            if j[0]<40 and j[1]<30:
#                t.append(j)
#                vertices.pop(vertices.index(j))
#                break
#        for j in vertices:
#            if j[0]<40 and j[1]>30:
#                t.append(j)
#                vertices.pop(vertices.index(j))
#                break
#        for j in vertices:
#            if j[0]>40 and j[1]>30:
#                t.append(j)
#                vertices.pop(vertices.index(j))
#                break
#        for j in vertices:
#            t.append(j)
#            vertices.pop(vertices.index(j))
#            break
#    vertices= array(t)
    centroid = asarray((centroid_x, centroid_y))

    base_array = zerosarray # zeros(shape, dtype=float)  # Initialize your array of zeros

    fill = ones(base_array.shape) * True  # Initialize boolean array defining shape fill

    # Create check array for each edge segment, combine into fill array
    for k in range(len(vertices)):
        base_array[vertices[k][1]][vertices[k][0]] = 1


 
    # Set all values inside polygon to one

    return base_array







