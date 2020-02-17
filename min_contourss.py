# -*- coding: utf-8 -*-
from numpy import zeros

def min_contourss(extracted_foreground, minaa, maxaa, minab, maxab):

    # Extraction of the minimum value of the contour and its coords
    a = 255
    for i in range(minaa, maxaa):  
        for j in range(minab, maxab):
            if (extracted_foreground[i][j] < a) and (extracted_foreground[i][j]!=0) \
               and (extracted_foreground[i][j]!=255):
                   a = extracted_foreground[i][j] 
                   min_loc = (i, j)

    return a, min_loc
