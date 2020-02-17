# -*- coding: utf-8 -*-

from numpy import zeros_like
from numpy import flip
from numpy import zeros
from numpy import all as alll
from Union import Union
from numpy import max as maxx
from numpy import rot90

def FindContourss(binary_image):

    binary_image = flip(binary_image, axis=1)
    binary_image = rot90(binary_image, 1)
    Erode_A = zeros_like(binary_image)

    for i in range(1, binary_image.shape[0]-1):
        for j in range(1, binary_image.shape[1]-1):
            if (binary_image[i][j] != 0):
                if (binary_image[i-1][j-1]> 0) \
                   and (binary_image[i+1][j-1]> 0) \
                   and (binary_image[i-1][j+1]> 0) \
                   and (binary_image[i+1][j+1]> 0):
                    Erode_A[i][j]=1

    #Eroded image subtracted to the original image to get the boundaries
    Contourses =  binary_image - Erode_A

    #Labeling of each boundary
    labeler = Union()
    Labeled_image = labeler.labelComponents(Contourses)

    num_contours = int(maxx(Labeled_image))

    # Contours (vertices) for each boundary
    for i in range(num_contours):
        vars()['contour'+str(i+1)] = zeros((len(Labeled_image[Labeled_image == (i+1)]), 1, 2), dtype='int32')
        vars()['contador'+str(i+1)] = -1
    

    for i in range(binary_image.shape[0]):
        for j in range(binary_image.shape[1]):
            for k in range(num_contours):
                if Labeled_image[i][j]==(k+1):
                    vars()['contador'+str(k+1)] = (vars()['contador'+str(k+1)])+1
                    vars()['contour'+str(k+1)][(vars()['contador'+str(k+1)])][0][0]=int(i)
                    vars()['contour'+str(k+1)][(vars()['contador'+str(k+1)])][0][1]=int(j)
     
    contourseses = [] 

    for i in range(num_contours):
        contourseses.append(vars()['contour'+str(i+1)]) 

    return contourseses

