# -*- coding: utf-8 -*-

from numpy import squeeze
from numpy import zeros
from numpy import zeros_like

def Drawfilledcontour(zeroes, polyCorner, minx, maxx, miny, maxy):

    polyCorner = squeeze(polyCorner, axis=1)
    polyCorners = zeros_like(polyCorner)
    nodeX = zeros(maxx-minx)  


#  Loop through the rows of the image.
    for pixelY in range(miny, maxy):
#  Build a list of nodes.
        nodes=-1 
        j=len(polyCorners)-1
        for i in range(len(polyCorners)):
            polyCorners[i][1] = polyCorner[i][0]
            polyCorners[i][0] = polyCorner[i][1]
            polyCorners[j][1] = polyCorner[j][0]
            polyCorners[j][0] = polyCorner[j][1]
            if (polyCorners[i][1]< float(pixelY) and polyCorners[j][1]>= float(pixelY) \
                or  polyCorners[j][1]< float(pixelY) and polyCorners[i][1]>= float(pixelY)):
                nodes = nodes+1
                nodeX[nodes]=int(polyCorners[i][0]+(pixelY-polyCorners[i][1])/(polyCorners[j][1] \
                                 -polyCorners[i][1]) *(polyCorners[j][0]-polyCorners[i][0]))
            j=i

#  //  Sort the nodes, via a simple “Bubble” sort
        i = 0
        while (i< nodes-1):
            if (nodeX[i]>nodeX[i+1]): 
                swap=nodeX[i]
                nodeX[i]=nodeX[i+1]
                nodeX[i+1]=swap
                if (i):
                    i = i-1
            else: 
                i=i+1

#  //  Fill the pixels between node pairs.
        for i in range(0, nodes, 2): 
            if (nodeX[i]>= nodeX[nodes]): break;
            if (nodeX[i+1]> nodeX[0]):
                if (nodeX[i]< nodeX[0]):
                    nodeX[i]=nodeX[0]
                if (nodeX[i+1]> nodeX[nodes]):
                    nodeX[i+1]=nodeX[nodes]
                for pixelX in range(int(nodeX[i]), int(nodeX[i+1])):
#                fillPixel(pixelX,pixelY)
                     zeroes[int(pixelX)][int(pixelY)]=1

    return zeroes

