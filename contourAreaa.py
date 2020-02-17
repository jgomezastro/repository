# -*- coding: utf-8 -*-

def contourAreaa(contourses):

    vertexCount = len(contourses) 
    signedArea = 0.0
    x0 = 0.0 # Current vertex X
    y0 = 0.0 # Current vertex Y
    x1 = 0.0 # Next vertex X
    y1 = 0.0 # Next vertex Y
    a = 0.0  # Partial signed area


        # For all vertices except last
    for i in range (vertexCount-1):
        x0 = contourses[i][0][0]
        y0 = contourses[i][0][1]
        x1 = contourses[i+1][0][0]
        y1 = contourses[i+1][0][1]
        a = x0*y1 - x1*y0
        signedArea += a

        # Do last vertex separately to avoid performing an expensive
        # modulus operation in each iteration.

    x0 = contourses[vertexCount-1][0][0]
    y0 = contourses[vertexCount-1][0][1]
    x1 = contourses[0][0][0]
    y1 = contourses[0][0][1]
    a = x0*y1 - x1*y0
    signedArea += a


    signedArea *= 0.5

    return float(abs(signedArea))
