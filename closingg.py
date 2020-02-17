# -*- coding: utf-8 -*-
from numpy import zeros

def closingg(bin_frame):    # for a "3x3" kernel

    #Dilation kernel 3x3
    Dil_A = zeros(bin_frame.shape, 'uint8')
    for i in range(1,bin_frame.shape[0]-1): 
        for j in range(1,bin_frame.shape[1]-1):
            if (bin_frame[i][j] > 0):
                Dil_A[i][j]=255
                Dil_A[i-1][j-1]=255
                Dil_A[i-1][j]=255
                Dil_A[i-1][j+1]=255
                Dil_A[i][j-1]=255
                Dil_A[i][j+1]=255
                Dil_A[i+1][j-1]=255
                Dil_A[i+1][j]=255
                Dil_A[i+1][j+1]=255

    #Erosion kernel 3x3
    Eroded_A = zeros(bin_frame.shape, 'uint8')
    for i in range(1,bin_frame.shape[0]-1): 
        for j in range(1,bin_frame.shape[1]-1):
            if (Dil_A[i][j] != 0):
                if (Dil_A[i-1][j-1]>0) and (Dil_A[i+1][j-1]>0) and \
                   (Dil_A[i+1][j-1]> 0) and (Dil_A[i-1][j+1]> 0) \
                   and (Dil_A[i+1][j+1]> 0):
                    Eroded_A[i][j]=255

    return Eroded_A
