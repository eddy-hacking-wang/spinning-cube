from manim import *
import math
from numpy import diagonal
from sympy import Symbol
from sympy.solvers import solve

from utillibrary import *

class RotatingCube(Scene):
    def construct(self):
        #Set up everything we need to draw the cube at a given angle
        renderables, squareCenter, stationPoint, ellCenter, majorRadius, smallRadius = self.setUpRotation()
        horizon, centerAxis, enclosed, squareCenterDot, cvpdot, stationDot, lowerLine = renderables
        #print(setup)


        squareInfo = self.drawSquare(squareCenter, 30, stationPoint, horizon,  ellCenter, majorRadius, smallRadius)

        self.add(renderables, squareInfo[0], squareInfo[1])

    def setUpRotation(self):
        """Draws the ellipse responsible for maintaining the perspective of the cube at multiple angles by setting up the reference 45 degree perpendiculars, the reference diagonal, and the 45 degree square."""

        #Horizon and center axis
        horizon = Line(LEFT * 8, RIGHT * 8, color=BLUE, stroke_width=0.5)
        centerAxis = Line(UP*4, DOWN*4, stroke_width=0.5)

        #Central View Point
        cvp = self.intersectionTwoLines(horizon, centerAxis)
        cvpdot = Dot(cvp, radius=0.04)

        #Station point
        lowerLine = horizon.copy().shift(3.5*DOWN)
        stationPoint = self.intersectionTwoLines(centerAxis, lowerLine)
        stationDot = Dot(stationPoint, radius=0.04)

        enclosed, majorRadius, smallRadius, ellCenter, squareCenter = self.drawReferenceEllipse(horizon, centerAxis, lowerLine)

        squareCenterDot = Dot(access_contents(squareCenter), radius=0.04)

        renderables = VGroup(horizon, centerAxis, enclosed[0], squareCenterDot, cvpdot, stationDot, lowerLine)

        return (renderables, squareCenter, stationPoint, ellCenter, majorRadius, smallRadius)
    
    def drawSquare(self, squareCenter, theta, station, horizon, origin, semiMajor, semiSmall):
        """Draws the square that is angled at a certain angle """
        if theta <= 0 or theta >= 90:
            pass

        v1line, v2line, bisector, angle = self.drawPerpendicular(station, theta)

        #Calculating horizon intersection points
        v1 = self.intersectionTwoLines(horizon, v1line)
        v2 = self.intersectionTwoLines(horizon, v2line)
        bisectorHorizon = self.intersectionTwoLines(horizon, bisector)

        #Finding diagonal of the rotated square
        bisectorHorizonX, bisectorHorizonY = get_x(bisectorHorizon), get_y(bisectorHorizon)
        squareCenterX, squareCenterY = get_x(squareCenter), get_y(squareCenter)
        rotatedDiagonal = Line(access_contents(bisectorHorizon), Point([bisectorHorizonX + 500 * (squareCenterX-bisectorHorizonX), bisectorHorizonY + 500 * (squareCenterY-bisectorHorizonY), 0]))

        # Intersection of rotated diagonal with ellipse
        q1, q2 = self.lineIntersectWithEllipse(rotatedDiagonal, squareCenter, origin, semiMajor, semiSmall)

        v1q1, v1q2, v2q1, v2q2 = self.drawVanishingLines(v1, v2, q1, q2)

        q3 = self.intersectionTwoLines(v2q1, v1q2)
        q4 = self.intersectionTwoLines(v1q1, v2q2)

        return (Polygon(q1, q3, q2, q4), v1line, v2line, bisector, angle)

    def drawVanishingLines(self, v1, v2, q1, q2):
        """Takes in the two vanishing points as well as the ends of the diagonal at which the vanishing lines should intersect.
        Returns the four lines created."""
        v1Contents, v1x, v1y = access_contents(v1), get_x(v1), get_y(v1)
        v2Contents, v2x, v2y = access_contents(v2), get_x(v2), get_y(v2)

        q1x, q1y = get_x(q1), get_y(q1)
        q2x, q2y = get_x(q2), get_y(q2)

        v1q1 = Line(v1Contents, Point([v1x + 500 * (q1x-v1x), v1y + 500 * (q1y-v1y), 0]))
        v1q2 = Line(v1Contents, Point([v1x + 500 * (q2x-v1x), v1y + 500 * (q2y-v1y), 0]))
        v2q1 = Line(v2Contents, Point([v2x - 500 * (q1x-v2x), v2y + 500 * (q1y-v2y), 0]))
        v2q2 = Line(v2Contents, Point([v2x - 500 * (q2x-v2x), v2y + 500 * (q2y-v2y), 0]))

        return (v1q1, v1q2, v2q1, v2q2)

    def lineIntersectWithEllipse(self, line, center, origin, semiMajor, semiSmall):
        """Takes the origin, major and minor axes of an ellipse (enough to form its equation) as well as a line, and
        calculates the intersection points of the line with the ellipse. Returns an array of points."""
        intercept = center[1]
        slope = self.calculateSlope(line.get_start(), center)
        print(slope)

        print(origin)
        print(semiMajor)
        print(semiSmall)

        x = Symbol("x")
        solution = solve((x-origin[0])**2/(semiMajor)**2
                        +((slope * x + intercept - origin[1])**2/(semiSmall)**2) - 1
                         )
        
        print(solution)

        return list(map(lambda soln : Point(float(soln), float(slope * soln + intercept), 0), solution))


        
    def calculateSlope(self, point1, point2):
        return (get_y(point1)-get_y(point2))/(get_x(point1)-get_x(point2))

    def drawPerpendicular(self, vertex, theta):
        """Draws a pair of perpendicular rays angled theta (degrees) from the positive x-axis at the given vertex, along with
        the angle bisector and the right angle marker. Returns a VGroup of the four objects."""

        rad = theta * math.pi/180

        print("vertex is:")
        print(vertex)

        print(get_y(vertex))

        v1line = Line(vertex, Point([get_x(vertex) + 500 * math.cos(rad), get_y(vertex) + 500 * math.sin(rad), 0]))
        v2line = Line(vertex, Point([get_x(vertex) - 500 * math.sin(rad), get_y(vertex) + 500 * math.cos(rad), 0]))
        bisector = Line(vertex, Point([get_x(vertex) + 500 * math.cos(rad + math.pi/4), get_y(vertex) + 500 * math.sin(rad + math.pi/4), 0]))
        angle = RightAngle(v1line, v2line)

        return VGroup(v1line, v2line, bisector, angle)

    def drawReferenceEllipse(self, horizon, centerAxis, lowerLine):
        """Draws the reference ellipse that is used to maintain the perspective of the cube at multiple angles. Takes in the horizon line, center axis, and lower line that the perpendiculars rest on.
        Returns the ellipse, the major radius, the minor radius, the center of the ellipse, and the center of the square."""
        stationPoint = self.intersectionTwoLines(centerAxis, lowerLine) 
        v1line, v2line, bisector, angle = self.drawPerpendicular(stationPoint, 45)

        #Vanishing points, v for vanishing points
        v1 = self.intersectionTwoLines(horizon, v1line)
        v2 = self.intersectionTwoLines(horizon, v2line)

        center = self.intersectionTwoLines(horizon, centerAxis)

        print("The center is:")
        print(center)

        #Reference diagonal for the bottom square
        diagonal = Line(Point([get_x(center), get_y(center) - 1, 0]), Point([get_x(center), get_y(center) - 2, 0]), color=RED) #Diagonal of the bottom square
        q1 = diagonal.get_start() #Far edge of the 45 degree cube
        q2 = diagonal.get_end()   #Near edge of the 45 degree cube

        #Lines from vanishing point to q1 and q2
        v1q1, v1q2, v2q1, v2q2 = self.drawVanishingLines(v1, v2, q1, q2)

        #q3 and q4 come from the intersections of the vanishing point lines
        q3 = self.intersectionTwoLines(v2q1, v1q2)
        q4 = self.intersectionTwoLines(v1q1, v2q2)

        oppDiagonal = Line(access_contents(q3), access_contents(q4))
        squareCenter = self.intersectionTwoLines(diagonal, oppDiagonal)
        ellCenter = midpoint(q1, q2)

        ellipse, majorRadius, smallRadius = self.drawEllipseAroundKite(q1, q2, q3, q4)
        enclosed = ellipse.move_to(ellCenter)

        print("Enclosed ellipse is:")
        print(enclosed)

        return (enclosed, majorRadius, smallRadius, ellCenter, squareCenter)


    def intersectionTwoLines(self, l1, l2):
        toReturn =  find_intersection(
            [l1.get_start()], [l1.get_vector()],
            [l2.get_start()], [l2.get_vector()]
        )
        return toReturn;
    
    def drawEllipseAroundKite(self, q1, q2, q3, q4):
        """Draws an ellipse around the kite formed by the points q1, q2, q3, and q4, where q1q2 and q3q4 are the diagonals of the kite, and the ellipse's axes are parallel to these
        lines. Returns the ellipse, the major radius, and the minor radius of the ellipse.
                 q1
        
             q3       q4
        
                 q2     
        """
        halfKiteHorizontal =  (get_x(q4) - get_x(q3)) / 2 #a
        distanceAboveAxis = get_y(q1) - get_y(q4) #b
        distanceBelowAxis = get_y(q1) - distanceAboveAxis - get_y(q2) #c
        smallRadius = (distanceBelowAxis + distanceAboveAxis) / 2 #(b+c)/2

        #Find distance from the center to the focus
        f = Symbol("f")
        solution = solve(2*(smallRadius**2 + f**2)**0.5 
                         - ((distanceBelowAxis-smallRadius)**2 + (halfKiteHorizontal - f)**2)**0.5
                         - ((distanceBelowAxis-smallRadius)**2 + (halfKiteHorizontal + f)**2)**0.5
                                     )
        
        majorRadius = math.sqrt(smallRadius**2 + solution[0]**2)

        ellipse = Ellipse(2*majorRadius, 2*smallRadius)

        return (ellipse, majorRadius, smallRadius)
