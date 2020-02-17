# -*- coding: utf-8 -*-
from numpy import zeros_like  
# Define Infinite (Using INT_MAX caused overflow problems) 
INF = 10000 
  
# Given three colinear points p, q, r, the function checks if 
# point q lies on line segment 'pr' 
def onSegment(p, q, r): 
    if (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1])): 
        return True 
    else: 
        return False 
 
  
# To find orientation of ordered triplet (p, q, r). 
# The function returns following values 
# 0 --> p, q and r are colinear 
# 1 --> Clockwise 
# 2 --> Counterclockwise 
def orientation(p, q, r): 
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1]) 
    if (val == 0):
        return 0  # colinear 
    elif (val>0):
        return 1
    else:
        return 2# clock or counterclock wise 
 
  
# The function that returns true if line segment 'p1q1' 
# and 'p2q2' intersect. 
def doIntersect(p1, q1, p2, q2): 
 
    # Find the four orientations needed for general and 
    # special cases 
    o1 = orientation(p1, q1, p2) 
    o2 = orientation(p1, q1, q2) 
    o3 = orientation(p2, q2, p1) 
    o4 = orientation(p2, q2, q1) 
      
    # General case 
    if (o1!= o2 and o3!=o4): 
        return True 
  
    # Special Cases 
    # p1, q1 and p2 are colinear and p2 lies on segment p1q1 
    if (o1 == 0 and onSegment(p1, p2, q1)): 
        return True 
  
    # p1, q1 and p2 are colinear and q2 lies on segment p1q1 
    if (o2 == 0 and onSegment(p1, q2, q1)): 
        return True 
  
    # p2, q2 and p1 are colinear and p1 lies on segment p2q2 
    if (o3 == 0 and onSegment(p2, p1, q2)): 
        return True 
  
     # p2, q2 and q1 are colinear and q1 lies on segment p2q2 
    if (o4 == 0 and onSegment(p2, q1, q2)): 
        return True 

    else:
        return False # Doesn't fall in any of the above cases 

   
# Returns true if the point p lies inside the polygon[] with n vertices 
def isInside(polygon, n, p):  
    # There must be at least 3 vertices in polygon[] 
    polygonn = zeros_like(polygon)
    if (n < 3):  
        return False 
  
    # Create a point for line segment from p to infinite 
    extreme = (INF, p[1]) 
  
    # Count intersections of the above line with sides of polygon 
    count = 0
    i = 0 
    next = 1
#        do
    while (next != 0):
        next = (i+1)%n 
        polygonn[i][0][0] = polygon[i][0][1]
        polygonn[i][0][1] = polygon[i][0][0]
        polygonn[next][0][0] = polygon[next][0][1]
        polygonn[next][0][1] = polygon[next][0][0]
        # Check if the line segment from 'p' to 'extreme' intersects 
        # with the line segment from 'polygon[i]' to 'polygon[next]' 
        
        if (doIntersect(polygonn[i][0][:], polygonn[next][0][:], p, extreme)): 
         
            # If the point 'p' is colinear with line segment 'i-next', 
            # then check if it lies on segment. If it lies, return true, 
            # otherwise false 
            if (orientation(polygonn[i][0][:], p, polygonn[next][0][:]) == 0): 
               return onSegment(polygonn[i][0][:], p, polygonn[next][0][:]) 
  
            count += 1 
         
        i = next 
#        while (i != 0) 
  
    # Return true if count is odd, false otherwise 
#    return count&1;  # Same as (count%2 == 1)
    return (count%2 == 1)  
 
  
# Driver program to test above functions 
def Polygontestpoint2(contourses, minima): 
    polygon = contourses 
    n = len(polygon)
    p = minima 
    testing = isInside(polygon, n, p)
    if testing == True: 
        return 1.0 
    if testing == False: 
        return -1.0 
