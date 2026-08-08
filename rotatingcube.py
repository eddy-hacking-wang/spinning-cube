from manim import *
import math
from numpy import diagonal
from sympy import Symbol
from sympy.solvers import solve

from utillibrary import *

LARGE_VALUE = 50

class RotatingCube(Scene):
    def construct(self):
        #Set up everything we need to draw the cube at a given angle
        renderables, squareCenter, stationPoint, ellCenter, majorRadius, smallRadius= self.setUpRotation()
        horizon, centerAxis, enclosed, squareCenterDot, cvpdot, stationDot, lowerLine = renderables

        theta = ValueTracker(0.1)

        squareInfo = always_redraw(
            lambda: self.drawCube(
                    squareCenter,
                    theta.get_value(), 
                    stationPoint,
                    horizon,
                    ellCenter,
                    majorRadius,
                    smallRadius,
                    stationPoint
                )
        )

        self.add(renderables, squareInfo)
        self.wait(1)
        self.play(theta.animate.set_value(89.9), rate_func=smooth, run_time=2)
        self.wait(1)

    def setUpRotation(self):
        """Draws the ellipse responsible for maintaining the perspective of the cube at multiple angles by setting up the reference 45 degree perpendiculars, the reference diagonal, and the 45 degree square."""

        #Horizon and center axis
        horizon = Line(LEFT * LARGE_VALUE, RIGHT * LARGE_VALUE, color=BLUE, stroke_width=0.5)
        centerAxis = Line(UP*LARGE_VALUE, DOWN*LARGE_VALUE, stroke_width=0.5)

        #Central View Point
        cvp = self.intersectionTwoLines(horizon, centerAxis)
        cvpdot = Dot(point_to_3d_like(cvp), radius=0.04)

        #Station point
        lowerLine = horizon.copy().shift(3.5*DOWN)
        stationPoint = self.intersectionTwoLines(centerAxis, lowerLine)
        stationDot = Dot(point_to_3d_like(stationPoint), radius=0.04)

        enclosed, majorRadius, smallRadius, ellCenter, squareCenter, v1, v2 = self.drawReferenceEllipse(horizon, centerAxis, lowerLine)

        squareCenterDot = Dot(point_to_3d_like(squareCenter), radius=0.04)

        renderables = VGroup(horizon, centerAxis, enclosed[0], squareCenterDot, cvpdot, stationDot, lowerLine)

        return (renderables, squareCenter, stationPoint, ellCenter, majorRadius, smallRadius)
    
    def drawSquare(self, squareCenter, theta, station, horizon, origin, semiMajor, semiSmall):
        """Draws the square that is angled at a certain angle """
        if theta <= 0 or theta >= 90:
            pass

        v1line, v2line, bisector, angle = self.drawPerpendicular(station, theta)

        #Calculating horizon intersection points
        v1 = self.intersectionTwoLines(horizon, v1line) #Right vanishing point
        v2 = self.intersectionTwoLines(horizon, v2line) #Left vanishing point
        bisectorHorizon = self.intersectionTwoLines(horizon, bisector)

        #Finding diagonal of the rotated square
        bisectorHorizonX, bisectorHorizonY = get_x(bisectorHorizon), get_y(bisectorHorizon)
        squareCenterX, squareCenterY = get_x(squareCenter), get_y(squareCenter)
        rotatedDiagonal = Line(point_to_3d_like(bisectorHorizon), Point([bisectorHorizonX + LARGE_VALUE * (squareCenterX-bisectorHorizonX), bisectorHorizonY + LARGE_VALUE * (squareCenterY-bisectorHorizonY), 0]))

        # Intersection of rotated diagonal with ellipse
        q1, q2 = self.lineIntersectWithEllipse(rotatedDiagonal, squareCenter, origin, semiMajor, semiSmall)

        v1q1, v1q2, v2q1, v2q2 = self.drawVanishingLines(v1, v2, q1, q2)

        q3 = self.intersectionTwoLines(v1q1, v2q2)
        q4 = self.intersectionTwoLines(v2q1, v1q2)

        # Perpendiculars
        perpendiculars = VGroup(v1line, v2line, bisector, angle).set_stroke(opacity=0.3)

        return (Polygon(point_to_3d_like(q1), point_to_3d_like(q3), point_to_3d_like(q2), point_to_3d_like(q4), color=WHITE), perpendiculars, q1, q2, q3, q4, v1, v2)

    def drawCube(self, squareCenter, theta, station, horizon, origin, semiMajor, semiSmall, vertex):
        bottomSquareArt, perpendiculars, q1, q2, q3, q4, v1, v2 = self.drawSquare(squareCenter, theta, station, horizon, origin, semiMajor, semiSmall)
        extraLines = self.drawExtraLines(v1, v2, vertex, q1, q2, q3, q4)

        return VGroup(bottomSquareArt, perpendiculars, extraLines)

    def drawExtraLines(self, v1, v2, vertex, q1, q2, q3, q4):
        v2Tovertex = self.distance(v2, vertex)

        eqPoint = Point([get_x(v2) + v2Tovertex, get_y(v2), 0])
        oppositeCorner = q3 if self.distance(eqPoint, q3) > self.distance(eqPoint, q4) else q4

        eqOpposite = self.drawRay(eqPoint, oppositeCorner)
        bottomLine = self.drawRay(q2, Point([get_x(oppositeCorner), get_y(q2), 0]))

        heightPoint = self.intersectionTwoLines(eqOpposite, bottomLine)
        cubeHeight = self.distance(heightPoint, q2)

        topCube = Point([get_x(q2), get_y(q2) + cubeHeight, 0])
        cubeCornerLine = Line(q2, topCube)

        # Finding the remaining points of the cube
        v1Top = self.drawRay(v1, topCube)
        v2Top = self.drawRay(v2, topCube)

        q3Up = self.drawRay(q3, Point([get_x(q3), get_y(q3) + 1, 0]))
        q4Up = self.drawRay(q4, Point([get_x(q4), get_y(q4) + 1, 0]))

        q3Corner = self.intersectionTwoLines(v2Top, q3Up)
        q4Corner = self.intersectionTwoLines(v1Top, q4Up)

        v1q3corner = self.drawRay(v1, q3Corner)
        v2q4corner = self.drawRay(v2, q4Corner)
        q1Top = self.intersectionTwoLines(v1q3corner, v2q4corner)

        v1q3 = self.drawRay(v1, q3)
        v1q2 = self.drawRay(v1, q2)

        v2q4 = self.drawRay(v2, q4)
        v2q2 = self.drawRay(v2, q2)

        vanishingLines = VGroup(v1q3, v1q2, v2q4, v2q2, v1Top, v2Top, v1q3corner, v2q4corner).set_stroke(opacity=0.3)

        cubeTopLines = VGroup(cubeCornerLine, Line(q3Corner, topCube), Line(q4Corner, topCube), Line(q3Corner, q1Top), Line(q4Corner, q1Top), Line(q1, q1Top), Line(q3, q3Corner), Line(q4, q4Corner))

        return VGroup(cubeTopLines, vanishingLines)
        

    def distance(self, p1, p2):
        return math.sqrt((get_x(p1) - get_x(p2))**2 + (get_y(p1) - get_y(p2))**2)

    def drawVanishingLines(self, v1, v2, q1, q2):
        """Takes in the two vanishing points as well as the ends of the diagonal at which the vanishing lines should intersect.
        Returns the four lines created."""
        v1x, v1y = get_x(v1), get_y(v1)
        v2x, v2y = get_x(v2), get_y(v2)

        q1x, q1y = get_x(q1), get_y(q1)
        q2x, q2y = get_x(q2), get_y(q2)

        v1q1 = self.drawRay(v1, q1)
        v1q2 = self.drawRay(v1, q2)
        v2q1 = self.drawRay(v2, q1)
        v2q2 = self.drawRay(v2, q2)

        return (v1q1, v1q2, v2q1, v2q2)

    def lineIntersectWithEllipse(self, line, center, origin, semiMajor, semiSmall):
        """Takes the origin, major and minor axes of an ellipse (enough to form its equation) as well as a line, and
        calculates the intersection points of the line with the ellipse. Returns an array of points."""
        intercept = get_y(center)
        slope = self.calculateSlope(Point(line.get_start()), center)

        solution = None

        if not slope:
            # Vertical line
            y = Symbol("y")
            x = get_x(center)
            solution = solve((x-get_x(origin))**2/(semiMajor)**2 
                             +((y - get_y(origin))**2/(semiSmall)**2) - 1
                             )
            return sorted(list(map(lambda soln : Point([float(x), float(soln), 0]), solution)), key=lambda a: get_y(a), reverse=True)
        else:
            # Non-vertical line
            x = Symbol("x")
            solution = solve((x-get_x(origin))**2/(semiMajor)**2
                            +((slope * x + intercept - get_y(origin))**2/(semiSmall)**2) - 1
                            )

            return sorted(list(map(lambda soln : Point([float(soln), float(slope * soln + intercept), 0]), solution)), key=lambda a: get_y(a), reverse=True)

    def drawRay(self, vertex, intersection):
        xVertex, yVertex = get_x(vertex), get_y(vertex)
        xIntersection, yIntersection = get_x(intersection), get_y(intersection)

        return Line(vertex, Point([xVertex + LARGE_VALUE * (xIntersection - xVertex), yVertex + LARGE_VALUE * (yIntersection - yVertex), 0]))
        
    def calculateSlope(self, point1, point2):
        if get_x(point1) == get_x(point2):
            return None

        return (get_y(point1)-get_y(point2))/(get_x(point1)-get_x(point2))

    def drawPerpendicular(self, vertex, theta):
        """Draws a pair of perpendicular rays angled theta (degrees) from the positive x-axis at the given vertex, along with
        the angle bisector and the right angle marker. Returns a VGroup of the four objects."""

        rad = theta * math.pi/180

        v1line = Line(vertex, Point([get_x(vertex) + LARGE_VALUE * math.cos(rad), get_y(vertex) + LARGE_VALUE * math.sin(rad), 0]))
        v2line = Line(vertex, Point([get_x(vertex) - LARGE_VALUE * math.sin(rad), get_y(vertex) + LARGE_VALUE * math.cos(rad), 0]))
        bisector = Line(vertex, Point([get_x(vertex) + LARGE_VALUE * math.cos(rad + math.pi/4), get_y(vertex) + LARGE_VALUE * math.sin(rad + math.pi/4), 0]))
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

        #Reference diagonal for the bottom square
        diagonal = Line(Point([get_x(center), get_y(center) - 1, 0]), Point([get_x(center), get_y(center) - 2, 0])) #Diagonal of the bottom square
        q1 = Point(diagonal.get_start()) #Far edge of the 45 degree cube
        q2 = Point(diagonal.get_end())   #Near edge of the 45 degree cube

        #Lines from vanishing point to q1 and q2
        v1q1, v1q2, v2q1, v2q2 = self.drawVanishingLines(v1, v2, q1, q2)

        #q3 and q4 come from the intersections of the vanishing point lines
        q3 = self.intersectionTwoLines(v2q1, v1q2)
        q4 = self.intersectionTwoLines(v1q1, v2q2)

        oppDiagonal = Line(point_to_3d_like(q3), point_to_3d_like(q4))
        squareCenter = self.intersectionTwoLines(diagonal, oppDiagonal)
        ellCenter = Point(midpoint(point_to_3d_like(q1), point_to_3d_like(q2)))

        ellipse, majorRadius, smallRadius = self.drawEllipseAroundKite(q1, q2, q3, q4)
        enclosed = ellipse.move_to(ellCenter)

        return (enclosed, majorRadius, smallRadius, ellCenter, squareCenter, v1, v2)


    def intersectionTwoLines(self, l1, l2):
        toReturn =  find_intersection(
            [l1.get_start()], [l1.get_vector()],
            [l2.get_start()], [l2.get_vector()]
        )

        return Point(toReturn[0]);
    
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

        ellipse = Ellipse(2*majorRadius, 2*smallRadius, color="WHITE").set_stroke(opacity=0.3)

        return (ellipse, majorRadius, smallRadius)
