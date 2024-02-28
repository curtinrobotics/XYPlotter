"""
pointList.py
Classes and enums for creating a list of points
"""

import math
import numpy as np
from enum import Enum
import constants as const

"""PointType - for whether the point is a position or and action"""
class PointType(Enum):
    Up = 1
    Down = 2
    Point = 3

"""PointCategory - for whether the point is inside or outside the plotter size"""
class PointCategory(Enum):
    Unknown = 1
    Inside = 2
    Border = 3
    Outside = 4
    Command = 5

"""Point - a single point/action"""
class Point:
    def __init__(self, pointType, x=None, y=None):
        self.type = pointType
        self.x = x
        self.y = y
        self.cat = PointCategory.Unknown

"""PointsList - a list of Points"""
class PointList:
    def __init__(self):
        self.list = []

    """Appends pen up command"""
    def penUp(self):
        newPoint = Point(PointType.Up)
        newPoint.cat = PointCategory.Command
        self.list.append(newPoint)

    """Appends pen down command"""
    def penDown(self):
        newPoint = Point(PointType.Down)
        newPoint.cat = PointCategory.Command
        self.list.append(newPoint)

    """Appends x and y to point list"""
    def addPoint(self, x, y):
        newPoint = Point(PointType.Point, x, y)
        self.list.append(newPoint)

    """Adds x and y to point list at index"""
    def addPointIndex(self, x, y, index):
        newPoint = Point(PointType.Point, x, y)
        self.list.insert(index, newPoint)

    """Appends list of points onto current list"""
    def extend(self, pList):
        self.list.extend(pList.list)

    """Removes last point from point list"""
    def removePoint(self):
        self.list.pop()

    """Appends list of points to create arc"""
    def drawArc(self, xPos, yPos, rx, ry, startDegree=None, arcDegree=None, res=100):
        
        if startDegree != None and arcDegree != None:
            sRad = startDegree * math.pi/180  # Start pos
            rad = arcDegree * math.pi/180  # Move amount
            for step in range(res+1):
                x = xPos + rx * math.cos((rad/res)*step + sRad)
                y = yPos + ry * math.sin((rad/res)*step + sRad)
                self.addPoint(x, y)

    """Appends list of points to create path arc"""
    def drawPathArc(self, xPos1, yPos1, rx, ry, rot, large, sweep, xPos2, yPos2):
        """
        *Note, all inputs are given by svg data

        xPos1 (int) - X-Position of the first point on the path arc
        yPos1 (int) - Y-Position of the first point on the path arc
        rx (int) - The radius along the x-axis of the ellipse created by the path
        ry (int) - The radius along the y-axis of the ellipse created by the path
        rot (int) - The rotation of the ellipse created by the path in degrees
        large (int) - Either 0 or 1 - Whether the desired path is the minor or major arc of the ellipse
        sweep (int) - Either 0 or 1 - Whether the desired path moves at anticlockwise or clockwise angles from (xPos1, yPos1), respectively
        xPos2 (int) - X-Position of the second point on the path arc
        yPos2 (int) - Y-Position of the second point on the path arc


        For more info, refer to: 
            https://www.desmos.com/calculator/sslfp6keyu
            https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths#arcs
        """

        """Function to return the maximum and minimum x values for the ellipse"""
        def xValueList(centre, LR, L):
            """
            centre (list) - the centre of the ellipse in question (x, y)
            LR (int) - whether the required point is to be on the left or on the right. LR is either -1 or 1, respectively
            L (int / float) - the scale factor of the ellipse (often is 1)
                            - for more information refer to Rotated Ellipse (r < d) on the above desmos url.
            """


            if P > 0 and Q > 0: inv = 1
            elif P > 0 and Q <= 0: inv = -1
            elif P <= 0 and Q > 0: inv = -1
            elif P <= 0 and Q <= 0: inv = 1

            xc1 = centre[0]

            if P == 0: xval = xc1 + LR* (L / math.sqrt(L*p))
            else: xval = LR * (LR* xc1*p + (L * P**3 * Q**3) / math.sqrt(L * P**2 * q * Q**2 * -ce3) + inv * math.sqrt(L * ( p - (P**2 * Q**2)/q ) ) )/p
            
            # Mathematical formulae as calculated by using wolfram mathematica.
            # Calculated by taking the formula for a rotated ellipse:
            # (LaTeX)
            # L=2 P Q (x-c) (y-d)+p (x-c)^2+q (y-d)^2
            # Where p, q, P, Q are designated constants as defined below and (c,d) are the coordinates of the centre of the ellipse
            # This formula was solved for x
            # \left\{x\to \frac{c p-\sqrt{L p-(d-y)^2 \left(p q-P^2 Q^2\right)}+P Q (d-y)}{p}\right\},\left\{x\to \frac{c p+\sqrt{L p-(d-y)^2 \left(p q-P^2 Q^2\right)}+P Q (d-y)}{p}\right\}
            # Of which the derivative d/dy was taken to create the derivative function:
            # \frac{\partial \frac{c p-\sqrt{L p-(d-y)^2 \left(p q-P^2 Q^2\right)}+P Q (d-y)}{p}}{\partial y}
            # -\frac{\frac{(d-y) \left(p q-P^2 Q^2\right)}{\sqrt{L p-(d-y)^2 \left(p q-P^2 Q^2\right)}}+P Q}{p}
            # The derivative was set to 0 and solved for y, resulting in the y value of the min and max x values:
            # \text{Solve}\left[0=-\frac{\frac{(d-y) \left(p q-P^2 Q^2\right)}{\sqrt{L p-(d-y)^2 \left(p q-P^2 Q^2\right)}}+P Q}{p},y\right]
            # \left\{y\to d-\frac{L P^2 Q^2}{\sqrt{L P^2 q Q^2 \left(p q-P^2 Q^2\right)}}\right\},\left\{y\to d+\frac{L P^2 Q^2}{\sqrt{L P^2 q Q^2 \left(p q-P^2 Q^2\right)}}\right\}
            # This y value was then substituted into the already calulated formula for x, resulting in:
            # -\frac{-c p+\sqrt{L \left(p-\frac{P^2 Q^2}{q}\right)}+\frac{L P^3 Q^3}{\sqrt{L P^2 q Q^2 \left(p q-P^2 Q^2\right)}}}{p}
            # Which was generalised to include both x values, as seen above

            return xval

        """Function to return the y values on an ellipse specified by its centre, according to the specified xList"""
        def yValueList(centre, L, xList):
            tempYList1 = []
            tempYList2 = []
            tempXList = []

            # Calculations involve solving the rotated ellipse equation:
            # (LaTeX)
            # L=2 P Q (x-c) (y-d)+p (x-c)^2+q (y-d)^2
            # with respect to y and substituting the x values
            # LaTeX code is given below:

            for i in range(len(xList)):
                x = xList[i]

                if L*q + ce3 * (centre[0] - x)**2 < 0: 
                    # If the discriminant is less than 0

                    if x == xList[-1]:
                        # If the x value is the end value, add it regardless

                        tempYList1.append(centre[1] - (L * P**2 * Q**2) / math.sqrt(L * P**2 * q * Q**2 * -ce3) )
                        tempYList2.append(centre[1] - (L * P**2 * Q**2) / math.sqrt(L * P**2 * q * Q**2 * -ce3) )
                        tempXList.append(x)
                        # y\to d-\frac{L P^2 Q^2}{\sqrt{L P^2 q Q^2 \left(p q-P^2 Q^2\right)}}

                    elif x == xList[0]:
                        # If the x value is the start value, add it regardless

                        tempYList1.append(centre[1] + (L * P**2 * Q**2) / math.sqrt(L * P**2 * q * Q**2 * -ce3) )
                        tempYList2.append(centre[1] + (L * P**2 * Q**2) / math.sqrt(L * P**2 * q * Q**2 * -ce3) )
                        tempXList.append(x)
                        # y\to d+\frac{L P^2 Q^2}{\sqrt{L P^2 q Q^2 \left(p q-P^2 Q^2\right)}}

                    print("xValue that was rejected is: " + str(x))
                    continue
                    # Reject any values that would otherwise result in a complex number calculation
                
                tempYList1.append((centre[1] * q - math.sqrt(L*q + ce3 * (centre[0] - x)**2 ) + P*Q * (centre[0] - x) ) / q)
                tempYList2.append((centre[1] * q + math.sqrt(L*q + ce3 * (centre[0] - x)**2 ) + P*Q * (centre[0] - x) ) / q)
                tempXList.append(x)
                # Calculate the y values for the given x value and add them to separate lists
                # \left\{y\to \frac{-\sqrt{L q-(c-x)^2 \left(p q-P^2 Q^2\right)}+P Q (c-x)+d q}{q}\right\},\left\{y\to \frac{\sqrt{L q-(c-x)^2 \left(p q-P^2 Q^2\right)}+P Q (c-x)+d q}{q}\right\}

            return tempXList, tempYList1, tempYList2


        if rot == 0: rot = 360 # Cannot handle rotation = 0 (divide by 0 error)
        rot = rot * -np.pi/180 # Convert to radians
        
        mid = [(xPos1 + xPos2)/2, (yPos1 + yPos2)/2] # Mid point between the two given points
        centre1 = [0, 0] # placeholder for the centre
        centre2 = [0, 0] # placeholder for the centre

        """-------------------------Constant Definitions-------------------------------"""
        # Refer to Placeholder Variables in the above desmos url

        p = math.cos(rot)**2/(rx**2) + math.sin(rot)**2/(ry**2)
        q = math.sin(rot)**2/(rx**2) + math.cos(rot)**2/(ry**2)

        P = 1/(rx**2) - 1/(ry**2)
        Q = math.cos(rot)*math.sin(rot)

        ce1 = (yPos1-yPos2)**2*q+(xPos1-xPos2)*((xPos1-xPos2)*p+2*(yPos1-yPos2)*P*Q)
        ce2 = xPos1*p-xPos2*p+(yPos1-yPos2)*P*Q
        ce3 = -p*q+P**2*Q**2
        ce4 = (ce2**2)*(ce3)*(-4+ce1)*(ce1)
        """----------------------------------------------------------------------------"""

        if ( -( (xPos1-xPos2)*p+(yPos1-yPos2)*P*Q)**2*(-ce3)*(-4+ce1)*(ce1) >= 0 or (ce2)**2*(ce3)*(-4+ce1)*(ce1) >= 0 ) and yPos2 - yPos1 == 0:
            # Rotated Ellipse where r > d and yPos2 - yPos1 = 0 
            # This is a special case as the other equations do not work for dy = 0

            centre1[0] = 0.5*(xPos1+xPos2+ (P*Q*math.sqrt(p*(-4+(xPos1-xPos2)**2*p)*(ce3))) / (p*(-ce3)) )
            # x\to \frac{1}{2} \left(\frac{P Q \sqrt{p \left(p (c-n)^2-4\right) \left(P^2 Q^2-p q\right)}}{p \left(p q-P^2 Q^2\right)}+c+n\right)
            centre1[1] = yPos1- (math.sqrt(-p*(-4+(xPos1-xPos2)**2*p)*(-ce3))) / (2*(-ce3))
            # y\to d-\frac{\sqrt{-p \left(p (c-n)^2-4\right) \left(p q-P^2 Q^2\right)}}{2 p q-2 P^2 Q^2}

            centre2[0] = 0.5*(xPos1+xPos2- (P*Q*math.sqrt(p*(-4+(xPos1-xPos2)**2*p)*(ce3))) / (p*(-ce3)) )
            # x\to \frac{1}{2} \left(-\frac{P Q \sqrt{p \left(p (c-n)^2-4\right) \left(P^2 Q^2-p q\right)}}{p \left(p q-P^2 Q^2\right)}+c+n\right)
            centre2[1] = yPos1+ (math.sqrt(-p*(-4+(xPos1-xPos2)**2*p)*(-ce3))) / (2*(-ce3))
            # y\to \frac{\sqrt{-p \left(p (c-n)^2-4\right) \left(p q-P^2 Q^2\right)}}{2 p q-2 P^2 Q^2}+d
            

            # Equations are calculated from finding the intersection of two ellipses where the y value on both is the same
            # c = xPos1, d = yPos1, n = xPos2
            # \text{Solve}\left[\left\{1=2 P Q (c-x) (d-y)+p (c-x)^2+q (d-y)^2,1=2 P Q (d-y) (n-x)+q (d-y)^2+p (n-x)^2\right\},\{y,x\}\right]
            # Refer to MDN web docs for path arcs for more information: https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths#arcs 
            # The above version is an extension of the unrotated example.

            xList1 = np.linspace(xValueList(centre1, -1, 1), xValueList(centre1, 1, 1), const.CURVE_SAMPLE_POINTS)
            xList2 = np.linspace(xValueList(centre2, -1, 1), xValueList(centre2, 1, 1), const.CURVE_SAMPLE_POINTS)
            # Create evenly spaced lists

            CentralPoints = [centre1, centre2]

            xList1, yList1, yList2 = yValueList(centre1, 1, xList1)
            xList2, yList3, yList4 = yValueList(centre2, 1, xList2)
            # Return the xLists and yLists of each ellipse

            print("dy = 0")

        elif -((xPos1-xPos2)*p+(yPos1-yPos2)*P*Q)**2*(-ce3)*(-4+ce1)*(ce1) >= 0 or (ce2)**2*(ce3)*(-4+ce1)*(ce1) >= 0:
            # Rotated Ellipse where r > d
            
            centre1[0] = 0.5*(xPos1+xPos2+ ((math.sqrt(ce4))) / (((yPos1-yPos2)*(ce2)*(-ce3))) - ((xPos1*math.sqrt(ce4))) / (((yPos1-yPos2)*(-ce3)*(ce1))) + ((xPos2*math.sqrt(ce4))) / (((yPos1-yPos2)*(-ce3)*(ce1))) )
            # x\to \frac{1}{2} \left(\frac{\sqrt{\left(P^2 Q^2-p q\right) (c p+P Q (d-m)-n p)^2 \left((c-n) (c p+2 P Q (d-m)-n p)+q (d-m)^2-4\right) \left((c-n) (c p+2 P Q (d-m)-n p)+q (d-m)^2\right)}}{(d-m) \left(p q-P^2 Q^2\right) (c p+P Q (d-m)-n p)}+\frac{n \sqrt{\left(P^2 Q^2-p q\right) (c p+P Q (d-m)-n p)^2 \left((c-n) (c p+2 P Q (d-m)-n p)+q (d-m)^2-4\right) \left((c-n) (c p+2 P Q (d-m)-n p)+q (d-m)^2\right)}}{(d-m) \left(p q-P^2 Q^2\right) \left((c-n) (c p+2 P Q (d-m)-n p)+q (d-m)^2\right)}-\frac{c \sqrt{\left(P^2 Q^2-p q\right) (c p+P Q (d-m)-n p)^2 \left((c-n) (c p+2 P Q (d-m)-n p)+q (d-m)^2-4\right) \left((c-n) (c p+2 P Q (d-m)-n p)+q (d-m)^2\right)}}{(d-m) \left(p q-P^2 Q^2\right) \left((c-n) (c p+2 P Q (d-m)-n p)+q (d-m)^2\right)}+c+n\right)
            centre1[1] = 0.5*(yPos1+yPos2- (math.sqrt( -(ce2**2)*(-ce3)*(-4+ce1)*(ce1) )) / ((-ce3)*(ce1)) )
            # y\to \frac{1}{2} \left(-\frac{\sqrt{\left(p q-P^2 Q^2\right) \left(-(p (c-n)+P Q (d-m))^2\right) \left((c-n) (p (c-n)+2 P Q (d-m))+q (d-m)^2-4\right) \left((c-n) (p (c-n)+2 P Q (d-m))+q (d-m)^2\right)}}{\left(p q-P^2 Q^2\right) \left((c-n) (p (c-n)+2 P Q (d-m))+q (d-m)^2\right)}+d+m\right)

            centre2[0] = 0.5*(xPos1+xPos2+ ((math.sqrt(ce4))) / (((yPos1-yPos2)*(ce2)*(ce3))) + ((xPos1*math.sqrt(ce4))) / (((yPos1-yPos2)*(-ce3)*(ce1))) - ((xPos2*math.sqrt(ce4))) / (((yPos1-yPos2)*(-ce3)*(ce1))) )
            # x\to \frac{1}{2} \left(\frac{\sqrt{\left(P^2 Q^2-p q\right) (c p+P Q (d-m)-n p)^2 \left((c-n) (c p+2 P Q (d-m)-n p)+q (d-m)^2-4\right) \left((c-n) (c p+2 P Q (d-m)-n p)+q (d-m)^2\right)}}{(d-m) \left(P^2 Q^2-p q\right) (c p+P Q (d-m)-n p)}+\frac{c \sqrt{\left(P^2 Q^2-p q\right) (c p+P Q (d-m)-n p)^2 \left((c-n) (c p+2 P Q (d-m)-n p)+q (d-m)^2-4\right) \left((c-n) (c p+2 P Q (d-m)-n p)+q (d-m)^2\right)}}{(d-m) \left(p q-P^2 Q^2\right) \left((c-n) (c p+2 P Q (d-m)-n p)+q (d-m)^2\right)}-\frac{n \sqrt{\left(P^2 Q^2-p q\right) (c p+P Q (d-m)-n p)^2 \left((c-n) (c p+2 P Q (d-m)-n p)+q (d-m)^2-4\right) \left((c-n) (c p+2 P Q (d-m)-n p)+q (d-m)^2\right)}}{(d-m) \left(p q-P^2 Q^2\right) \left((c-n) (c p+2 P Q (d-m)-n p)+q (d-m)^2\right)}+c+n\right)
            centre2[1] = 0.5*(yPos1+yPos2+ (math.sqrt( -(ce2**2)*(-ce3)*(-4+ce1)*(ce1) )) / ((-ce3)*(ce1)) )
            # y\to \frac{1}{2} \left(\frac{\sqrt{\left(p q-P^2 Q^2\right) \left(-(p (c-n)+P Q (d-m))^2\right) \left((c-n) (p (c-n)+2 P Q (d-m))+q (d-m)^2-4\right) \left((c-n) (p (c-n)+2 P Q (d-m))+q (d-m)^2\right)}}{\left(p q-P^2 Q^2\right) \left((c-n) (p (c-n)+2 P Q (d-m))+q (d-m)^2\right)}+d+m\right)


            # Equations are calculated from finding the intersection of two ellipses
            # c = xPos1, d = yPos1, n = xPos2, m = yPos2
            # \text{Solve}\left[\left\{1=2 P Q (c-x) (d-y)+p (c-x)^2+q (d-y)^2,1=2 P Q (m-y) (n-x)+q (m-y)^2+p (n-x)^2\right\},\{y,x\}\right]
            # Refer to MDN web docs for path arcs for more information: https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths#arcs 
            # The above version is an extension of the unrotated example.

            xList1 = np.linspace(xValueList(centre1, -1, 1), xValueList(centre1, 1, 1), const.CURVE_SAMPLE_POINTS)
            xList2 = np.linspace(xValueList(centre2, -1, 1), xValueList(centre2, 1, 1), const.CURVE_SAMPLE_POINTS)
            # Create evenly spaced lists

            CentralPoints = [centre1, centre2]

            xList1, yList1, yList2 = yValueList(centre1, 1, xList1)
            xList2, yList3, yList4 = yValueList(centre2, 1, xList2)
            # Return the xLists and yLists of each ellipse

            print("dy != 0")

        elif -((xPos1-xPos2)*p+(yPos1-yPos2)*P*Q)**2*(-ce3)*(-4+ce1)*(ce1) < 0 or (ce2)**2*(ce3)*(-4+ce1)*(ce1) < 0:
            # Rotated Ellipse where r < d
            
            # Notice no centre calculation
            # The centre is the midpoint between the start and end

            L = (p)*(xPos2-mid[0])**2+2*Q*(P)*(xPos2-mid[0])*(yPos2-mid[1])+(q)*(yPos2-mid[1])**2
            # Scale factor for the ellipse 
            # Calculated using the equation for a rotated ellipse:
            # L=2 P Q (x-c) (y-d)+p (x-c)^2+q (y-d)^2
            # where c is the x-value for the ellipse centre and d is the y-value
            # Refer to MDN web docs for path arcs for more information: https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths#arcs 

            xList1 = np.linspace(xValueList(mid, -1, L), xValueList(mid, 1, L), const.CURVE_SAMPLE_POINTS)

            CentralPoints = [mid, mid]

            xList1, yList1, yList2 = yValueList(mid, L, xList1)
            xList2, yList3, yList4 = xList1, yList1, yList2
            # Return the xLists and yLists of the ellipse (xList2, yList3 and yList4 are irrelevant but the variables must exist)
            # As opposed to the other calculations, only one ellipse is returned


        endPoints = [Vec2D(xPos1, yPos1, 'rec'), Vec2D(xPos2, yPos2, 'rec')]
        # Create the end points as position vectors

        ellipseDirectionVector = endPoints[1] - endPoints[0]
        # Points from start to end
        if ellipseDirectionVector.vec.x < 0: chooser = not abs(large - sweep)
        else: chooser = abs(large - sweep)
        # Chooser decides which ellipse is required for the path arc


        Cx, Cy = CentralPoints[chooser]
        # Chooses the required centre

        ChosenCentre = Vec2D(Cx, Cy, 'rec')
        # Creates a vector object for the centre

        relativeEnds = [-1*ChosenCentre + endPoints[0], -1*ChosenCentre + endPoints[1]]
        # Creates relative position vectors for the end points
        
        """Function to convert the reference angle depending on the quadrant the vector lies in"""
        def referenceAngleConverter(sweep, theta):
            if sweep and theta < 0: theta = 2*math.pi + theta
            elif not sweep and theta > 0: theta = theta - 2*math.pi
            
            return theta



        startAngle = 0 # The angles will be measured from the start position (relativeEnds[0])
        endAngle = referenceAngleConverter(sweep, relativeEnds[0].convert().angle(relativeEnds[1]))
            # Make the start angle 0 and the end angle transformed wrt to the start angle.
            #   ie. the angles start to measure cw or acw from the start point depending on sweep



        #Chosen Centre decided by chooser ie. 0 for centre1 and 1 for centre2
        #Centre 1 - [xList1, yList1, yList2]
        #Centre 1 - [[xList1, yList1], [xList1, yList2]]
        #Centre 2 - [xList2, yList3, yList4]
        #Centre 2 - [[xList2, yList3], [xList2, yList4]]

        PointLists = [ [ [xList1, yList1], [xList1, yList2] ], [ [xList2, yList3], [xList2, yList4] ] ]

        ellipseList = PointLists[chooser]

        xList = ellipseList[0][0] + ellipseList[1][0]
        yList = ellipseList[0][1] + ellipseList[1][1]
        # Combining the xLists and yLists, but ensuring that they remain in the same order.


        vecList = [Vec2D(xList[i], yList[i], 'rec') for i in range(len(xList))]
        # Convert all points in xList and yList to position vectors

        relativeVecList = [-1*ChosenCentre + vec for vec in vecList]
        # Convert all position vectors to relative position vectors with respect to the ellipse centre

        thetaList = [referenceAngleConverter(sweep, relativeEnds[0].convert().angle(vec)) for vec in relativeVecList]
        # Creates a list of angles in the direction of sweep with respect to the start position from all of the vectors


        """----------Useful for debugging----------------
        print('\nThetaList\n', thetaList, '\n')
        print(relativeEnds[0].angle(relativeVecList[4]))
        print(relativeVecList[4].angle(relativeEnds[0]))
        print(startAngle)
        print(endAngle * 180/math.pi)
        print(Cx, Cy)
        """

        
        filteredVecList = []
        filteredThetaList = []

        for i in range(len(thetaList)):
            theta = thetaList[i]
            # For each angle in thetaList
            
            if sweep:
                if startAngle <= theta and theta <= endAngle:
                    # If sweep is clockwise, accept only angles between the start and end angles, but moving clockwise
                    
                    filteredVecList.append(vecList[i])
                    filteredThetaList.append(theta)
            else:
                if startAngle >= theta and theta >= endAngle:
                    # If sweep is anticlockwise (default), accept only angles between the start and end angles, but moving anticlockwise

                    filteredVecList.append(vecList[i])
                    filteredThetaList.append(theta)

                """------------Useful for debugging---------------------------------
                    print('ACCEPTED:\t', str(vecList[i]), '\t', theta * 180/math.pi)
                else: 
                    print('REJECTED:\t', str(vecList[i]), '\t', theta * 180/math.pi)
                """


        #print([str(vec) for vec in filteredVecList])
        #print([a*180/math.pi for a in filteredThetaList])
        # Prints the vectors and the angles that have been filtered (used for debugging)


        if sweep: sortedVecList = Sort(True, filteredThetaList, filteredVecList)[1][0]
        else: sortedVecList = Sort(False, filteredThetaList, filteredVecList)[1][0]
        # If sweep is clockwise, angles are positive so sorting must occur from smallest to largest
        # If sweep is anticlockwise, angles are negative so sorting must occur from largest to smallest


        sortedVecListX = [vec.vec.x for vec in sortedVecList]
        sortedVecListY = [vec.vec.y for vec in sortedVecList]

        for i in range(len(sortedVecListX)):
            self.addPoint(sortedVecListX[i], sortedVecListY[i])
            # Adds the points as part of the pointlist

        return sortedVecListX, sortedVecListY 
        # Returns sorted vector lists in component forms (may remove later)


    """Returns length of the point list"""
    def length(self):
        return len(self.list)


    """Gets maximum and minimum points from"""
    def getMaxPoints(self):
        minMax = PointMinMax()

        for curPoint in self.list:
            if curPoint.type == PointType.Point:
                if curPoint.x > minMax.maxX:
                    minMax.maxX = curPoint.x
                if curPoint.y > minMax.maxY:
                    minMax.maxY = curPoint.y
                if curPoint.x < minMax.minX:
                    minMax.minX = curPoint.x
                if curPoint.y < minMax.minY:
                    minMax.minY = curPoint.y

        return minMax

"""PointMinMax - data structure for holding minimum and maximum points"""
class PointMinMax:
    def __init__(self):
        self.maxX = -9999
        self.maxY = -9999
        self.minX = 9999
        self.minY = 9999


"""Class to act as a 2D Vector"""
class Vec2D:
            
    """Subclass for the rectangular version of a 2D Vector"""
    class Rec:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.type = 'rec'

        """Converts the class to a readable string"""
        def __str__(self):
            return f'[{self.x}, {self.y}]'
        
        """Converts the class to a usable iterable object"""
        def __iter__(self):
            return iter([self.x, self.y])

        """Allows for addition of classes"""
        def __add__(self, vec):
            if vec.type == 'polar': vec = vec.convert()
            return Vec2D(self.x + vec.vec.x, self.y + vec.vec.y, 'rec')
        
        """Allosw for addition of classes"""
        def __radd__(self, vec):
            return self.__add__(vec)
        
        """Allows for subtraction of classes"""
        def __sub__(self, vec):
            if vec.type == 'polar': vec = vec.convert()
            return Vec2D(self.x - vec.vec.x, self.y - vec.vec.y, 'rec')
        
        """Allows for subtraction of classes"""
        def __rsub__(self, vec):
            if vec.type == 'polar': vec = vec.convert()
            return Vec2D(-self.x + vec.vec.x, -self.y + vec.vec.y, 'rec')
        
        """Allows for multiplication of a number with the vector"""
        def __mul__(self, int):
            return Vec2D(self.x * int, self.y * int, 'rec')

        """Allows for multiplication of a number with the vector"""
        def __rmul__(self, int):
            return self.__mul__(int)

        """Allows for division of a number with the vector"""
        def __truediv__(self, int):
            return Vec2D(self.x / int, self.y / int, 'rec')

        """Allows for the division of a number with the vector"""
        def __rtruediv__(self, int):
            return Vec2D(int / self.x, int / self.y, 'rec')

        """Calculates the dot product of two vectors"""
        def dot(self, vec):
            if vec.type == 'polar': vec = vec.convert()
            return self.x * vec.vec.x + self.y * vec.vec.y

        """Calculates the magnitude of the vector"""
        def norm(self):
            return math.sqrt(self.x**2 + self.y**2)

        """Calculates the angle between two vectors (Not relative)"""
        def angle(self, vec):
            if vec.type == 'polar': vec = vec.convert()
            return math.acos( self.dot(vec) / (self.norm() * vec.norm()) )

        """Converts the rectangular form to a polar form vector"""
        def convert(self):
            r = math.sqrt(self.x**2 + self.y**2)
            if self.x != 0: theta = math.atan(self.y/self.x)
            else: theta = self.y/abs(self.y) * math.pi/2

            if self.x < 0 and self.y >= 0:
                theta += math.pi
            elif self.x < 0 and self.y < 0:
                theta -= math.pi

            return Vec2D(r, theta, 'polar')
    

    """Subclass for the polar version of a 2D Vector"""
    class Polar:
        def __init__(self, r, theta):
            self.r = r
            self.theta = theta
            self.type = 'polar'

        """Converts the class to a readable string"""
        def __str__(self):
            return f'[{self.r}, {self.theta}]'
        
        """Converts the class to a usable iterable object"""
        def __iter__(self):
            return iter([self.r, self.theta])

        """Allows for addition of classes"""
        def __add__(self, vec):
            """Converts to rectangular then adds according to rectangular form"""
            return self.convert().__add__(vec).convert()

        """Allows for addition of classes"""
        def __radd__(self, vec):
            """Converts to rectangular then adds according to rectangular form"""
            return self.__add__(vec)
        
        """Allows for subtraction of classes"""
        def __sub__(self, vec):
            """Converts to rectangular then subtracts according to rectangular form"""
            return self.convert().__sub__(vec).convert()

        """Allows for subtraction of classes"""
        def __rsub__(self, vec):
            """Converts to rectangular then subtracts according to rectangular form"""
            return self.__sub__(vec)
        
        """Allows for multiplication of a number with the vector"""
        def __mul__(self, int):
            """Converts to rectangular then multiplies according to rectangular form"""
            converted = self.convert()
            return Vec2D(converted.vec.x * int, converted.vec.y * int, 'rec').convert()

        """Allows for multiplication of a number with the vector"""
        def __rmul__(self, int):
            """Converts to rectangular then multiplies according to rectangular form"""
            return self.__mul__(int)
        
        """Allows for division of a number with the vector"""        
        def __truediv__(self, int):
            """Converts to rectangular then divides according to rectangular form"""
            converted = self.convert()
            return Vec2D(converted.vec.x / int, converted.vec.y / int, 'rec').convert()

        """Allows for division of a number with the vector"""
        def __rtruediv__(self, int):
            """Converts to rectangular then divides according to rectangular form"""
            converted = self.convert()
            return Vec2D(int / converted.vec.x, int / converted.vec.y, 'rec').convert()

        """Calculates the dot product of two vectors"""
        def dot(self, vec):
            if vec.type == 'rec': vec = vec.convert()
            return self.r * vec.vec.r * math.cos(self.angle(vec))

        """Returns the magnitude of the vector"""
        def norm(self):
            return self.r

        """Calculates the angle between two vectors (Relative)"""
        def angle(self, vec):
            """
            Note: the angle that is returned is positive for the clockwise direction and negative for the anticlockwise direction.
            """
            
            if vec.type == 'rec': vec = vec.convert()
            
            angle = vec.vec.theta - self.theta
            if angle > math.pi or angle < -math.pi: 
                if angle > 0: angle = angle - 2*math.pi
                else: angle = 2*math.pi + angle

            return angle

        """Converts the polar form to a rectangular form vector"""
        def convert(self):
            x = self.r * math.cos(self.theta)
            y = self.r * math.sin(self.theta)
            
            return Vec2D(x, y, 'rec')

    def __init__(self, arg1, arg2, type='rec'):
        self.type = type

        if type.lower() == 'rec':
            self.vec = self.Rec(arg1, arg2)

        elif type.lower() == 'polar':
            self.vec = self.Polar(arg1, arg2)

        else:
            raise AttributeError

    """Converts the class to a readable string"""    
    def __str__(self):
        return str(self.vec)

    """Converts the class to a usable iterable object"""    
    def __iter__(self):
        return iter(self.vec)

    """Allows for addition of classes"""
    def __add__(self, vec):
        return self.vec.__add__(vec)

    """Allosw for addition of classes"""    
    def __radd__(self, vec):
        return self.vec.__radd__(vec)

    """Allows for subtraction of classes"""    
    def __sub__(self, vec):
        return self.vec.__sub__(vec)

    """Allows for subtraction of classes"""    
    def __rsub__(self, vec):
        return self.vec.__rsub__(vec)

    """Allows for multiplication of a number with the vector"""    
    def __mul__(self, int):
        return self.vec.__mul__(int)

    """Allows for multiplication of a number with the vector"""    
    def __rmul__(self, int):
        return self.vec.__rmul__(int)

    """Allows for division of a number with the vector"""    
    def __truediv__(self, int):
        return self.vec.__truediv__(int)

    """Allows for the division of a number with the vector"""    
    def __rtruediv__(self, int):
        return self.vec.__rtruediv__(int)

    """Calculates the dot product of two vectors"""    
    def dot(self, vec):
        return self.vec.dot(vec)

    """Calculates the magnitude of the vector"""
    def norm(self):
        return self.vec.norm()

    """Calculates the angle between two vectors"""
    def angle(self, vec):
        """
        Note: not relative for rectangular, relative for polar.
        """
        return self.vec.angle(vec)

    """Converts one type of vector into the other form"""
    def convert(self):
        return self.vec.convert()
    

    
"""Sorts lists with respect to a reference list"""
def Sort(forward:bool, ref:list, *others:list):
    """
    forward (bool) - whether the sorting should occur in ascending order or not
    ref (list) - the reference list by which to sort the other lists
    others (list) - any other lists that would be sorted according to the reference list
    
    * Note
    organisedArrays is returned as an array of the others
    ie. if the function is passed as: Sort(True, [3, 2, 1], [4, 5, 6], [7, 8, 9])
        then organisedArrays returns: [ [6, 5, 4], [9, 8, 7] ]
    """
    
    sorter = {}
    ref2 = list(ref)
    others = np.array(others)

    for i in range(len(ref)):
        sorter[ref2[i]] = list(others[:,i])
        # Create a key-value pair where all of the values from the others list are paired to their respective keys in the reference list

    ref2.sort(reverse= not forward)
    # sort the reference array

    organiser = np.array([sorter[i] for i in ref2])
    # creates arrays where each value is mapped to the respective reference value

    organisedArrays = np.array([organiser[:,i] for i in range(len(organiser[0]))])
    # combines the sorted values from the different lists into the sorted lists
    # ie. [1, 4], [2, 5], [3, 6] becomes [1, 2, 3], [4, 5, 6]

    return np.array(ref2), organisedArrays



if __name__ == '__main__':
    pl = PointList()

    #xLists, yLists = pl.drawPathArc(10, 30, 20, 20, 0, 0, 1, 50, 30)
    #xLists, yLists = pl.drawPathArc(50, 50, 30, 60, 45, 0, 1, 20, 20)
    #xLists, yLists = pl.drawPathArc(50, 50, 30, 60, 20, 0, 0, 110, 70)
    #xLists, yLists = pl.drawPathArc(50, 50, 20, 30, -45, 1, 0, 60, 60)
    #xLists, yLists = pl.drawPathArc(0, 30, 10, 20, -90, 0, 0, 0, 90)
    #xLists, yLists = pl.drawPathArc(20, 20, 20, 30, 0, 1, 1, 50, 50)
    #xLists, yLists = pl.drawPathArc(50, 50, 10, 15, 30, 0, 1, 110, 90)
    #xLists, yLists = pl.drawPathArc(110, 90, 10, 15, 30, 0, 1, 20, 20)
    #xLists, yLists = pl.drawPathArc(60, 60, 10, 5, -20, 1, 0, 90, 90)
    xLists, yLists = pl.drawPathArc(60, 60, 10, 5, -135, 1, 0, 90, 90)

    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = fig.add_subplot()

    plt.plot(xLists, yLists)

    def gradientLine(x):
            m = ( 40 - 60 ) / ( 100 - 60 )
            
            y = m*(x-60) + 60
            
            return y


    plt.plot(xLists, [gradientLine(x) for x in xLists])
    

    ax.set_aspect('equal')

    plt.axis()
    plt.show()