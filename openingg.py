# -*- coding: utf-8 -*-
from numpy import zeros

def openingg(bin_frame):    # for a "3x3" kernel

    #Erosion
    Eroded_A = zeros(bin_frame.shape, 'uint8')
    for i in range(1,bin_frame.shape[0]-1): 
        for j in range(1,bin_frame.shape[1]-1):
            if (bin_frame[i][j] != 0):
                if (bin_frame[i-1][j-1]> 0) and (bin_frame[i+1][j-1]> 0) \
                   and (bin_frame[i+1][j-1]> 0) and (bin_frame[i-1][j+1]> 0) \
                   and (bin_frame[i+1][j+1]> 0):
                    Eroded_A[i][j]=255

    Dil_A=zeros(bin_frame.shape, 'uint8')
    #Dilation
    for i in range(1,Eroded_A.shape[0]-1): 
        for j in range(1,Eroded_A.shape[1]-1):
            if (Eroded_A[i][j] > 0):
                Dil_A[i][j]=255
                Dil_A[i-1][j-1]=255
                Dil_A[i-1][j]=255
                Dil_A[i-1][j+1]=255
                Dil_A[i][j-1]=255
                Dil_A[i][j+1]=255
                Dil_A[i+1][j-1]=255
                Dil_A[i+1][j]=255
                Dil_A[i+1][j+1]=255

    return Dil_A
