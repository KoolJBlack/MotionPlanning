import numpy as np
import math

MAX_DISTANCE = 100 #TODO clean
# =============================================================================
# Map Primitives
# =============================================================================
class Point:
    ''' 2D class representaiton of a point '''
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.items = [x,y]
        self.polygonal = False
        self.numpyRep = np.array([self.x, self.y])
    def __getitem__(self, index):
        return self.items[index]
    def dist_to_point(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
    def __len__(self):
        return 2
    def __str__(self):
        return str(self.x) + ', ' + str(self.y) 
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    def setPreSuc (self, pre, suc, ccw):
        self.pre = pre
        toPre = self.pre.numpyRep - self.numpyRep
        self.preAngle = math.atan2(toPre[1],toPre[0])
        self.suc = suc
        toSuc = self.suc.numpyRep - self.numpyRep
        self.sucAngle = math.atan2(toSuc[1],toSuc[0])
        self.ccw = ccw
        self.polygonal = True
    def angleOutside(self, angle):
        if not self.polygonal:
            return True
        insideCCW = False
        if self.preAngle > 0:
            if self.sucAngle > 0:
                if self.sucAngle > self.preAngle:
                    insideCCW = angle <= self.sucAngle and angle >= self.preAngle
                else: 
                    insideCCW = angle <= self.sucAngle or angle >= self.preAngle
            else:
                insideCCW = angle <= self.sucAngle or angle >= self.preAngle
        else:
            if self.sucAngle < 0:
                if self.sucAngle > self.preAngle:
                    insideCCW = angle <= self.sucAngle and angle >= self.preAngle
                else:
                    insideCCW = angle <= self.sucAngle or angle >= self.preAngle
            else:
                insideCCW = angle <= self.sucAngle and angle >= self.preAngle
        return insideCCW if self.ccw else not insideCCW
                    
class Poly:
    ''' A poly is a list of points '''
    def __init__(self):
        self.points = []
    def computeWinding(self):
        signedArea = 0
        for i in range(len(self.points)-1, -1, -1):
            pi = self.points[i - 1]
            pip1 = self.points[i] #i + 1
            signedArea += .5 * (pi.x*pip1.y - pip1.x*pi.y)
        self.ccw = signedArea > 0
        for i in range(len(self.points)):
            self.points[i].setPreSuc(self.points[i - 1], self.points[(i + 1) % len(self.points)], self.ccw)


def p2p_dist(p1, p2):
    ''' Returns euclidian distance between two points'''
    return p1.dist_to_point(p2) 

def compute_adjacency_list(p_origin, other_points, grid):
    ''' Creates adjacency list for a point in the form: 
    '{'u' : 10, 'x' : 5}
    '''
    adjacent = dict()
    for point in other_points:
        unobstructed = True
        pathSeg = LineSegment(p_origin.numpyRep, point.numpyRep)
        toPoint = point.numpyRep - p_origin.numpyRep
        if np.linalg.norm(toPoint) > MAX_DISTANCE:
            continue
        originAngle = math.atan2(toPoint[1], toPoint[0])
        clear = p_origin.angleOutside(originAngle)
        if not clear:
            continue
        debug_intersectionsTested = 0
        for square in pathSeg.gridSquares():
            if square in grid:
                for edge in grid[square]:
                    debug_intersectionsTested += 1
                    if pathSeg.intersects(edge):
                        unobstructed = False
                        #print debug_intersectionsTested * len(other_points)
                        break
                    #print debug_intersectionsTested * len(other_points)
        if unobstructed:
            dist = p_origin.dist_to_point(point)
            adjacent[point] = dist
    return adjacent

def get_all_points_from_polys(polys):
    ''' Breaks a list of polygons into a list of points '''
    points = list()
    for poly in polys:
        points.extend(poly.points)
    return points

def add_all_segments_from_polys(polys, grid):
    #print 'get_all_segments_from_polys'
    for poly in polys:
        # take advantage of l[-1] being l[len-1]
        #print 'new poly'
        for i in range(len(poly.points)-1, -1, -1):
            #print i, i-1
            segment = LineSegment(poly.points[i].numpyRep,
                                  poly.points[i-1].numpyRep)
            for square in segment.gridSquares():
                if not square in grid:
                    grid[square] = []
                grid[square].append(segment)
            

def nearest_neighbor(p_origin, points):
    ''' Find the nearest neighboring point in the points list and returns it'''
    dist = 99999999999999
    best_point = None
    for point in points:
        if point.dist_to_point(p_origin) < dist:
            dist = point.dist_to_point(p_origin)
            best_point = point
    return point


# =============================================================================
# Line Segments
# =============================================================================

def ccw(A, B, C):
    return (C[1] - A[1])*(B[0] - A[0]) > (B[1] - A[1])*(C[0] - A[0])

def inRange(x, a, b):
    #print x, a, b, (x >= a) and (x <= b)
    return (x >= a) and (x <= b)

class LineSegment:
    '''uses numpy points'''
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        if self.p1[0] > self.p2[0]:
            temp = self.p2
            self.p2 = self.p1
            self.p1 = temp
        v = p2 - p1
        self.vertical = (v[0] == 0)
        if self.vertical:
            if self.p1[1] > self.p2[1]:            
                temp = self.p2
                self.p2 = self.p1
                self.p1 = temp            
        if not self.vertical:
            self.m = (v[1] / v[0])
            self.b = p2[1] - (self.m * p2[0])
        self.gridSize = 5 #TODO clean
    def __str__(self):
        return 'P1: '+  str(self.p1[0]) + ', ' + str(self.p1[1])  + '  P2: ' + str(self.p2[0]) + ', ' + str(self.p2[1])
    def intersectsInternet(self, other):
        return (ccw(self.p1, other.p1, other.p2) != ccw(self.p2, other.p1, other.p2)
                and ccw(self.p1, self.p2, other.p1) != ccw(self.p1, self.p2, other.p2))

    def intersects(self, other):
        #comparison of numpy arrays requires all
        if ((self.p1 == other.p1).all() or (self.p1 == other.p2).all()
            or (self.p2 == other.p1).all() or (self.p2  == other.p2).all()):
            return False
        if self.vertical:
            if other.vertical:
                if(self.p1[0] != other.p1[0]):
                    #print "both vertical different x"
                    return False
                return (inRange(other.p1[1], self.p1[1], self.p2[1])
                        or inRange(other.p2[1], self.p1[1], self.p2[1]))
            else:
                # y = mx + b
                otherY = (other.m * self.p1[0]) + other.b
                return (inRange(otherY, self.p1[1], self.p2[1])
                        and inRange(self.p1[0], other.p1[0], other.p2[0]))
        else:
            if other.vertical:
                selfY = (self.m * other.p1[0]) + self.b
                #print self.m, other.p1[0], self.b, selfY
                return (inRange(selfY, other.p1[1], other.p2[1])
                        and inRange(other.p1[0], self.p1[0], self.p2[0]))
            else:
                if self.m == other.m:
                    return ((self.b == other.b) and
                            (inRange(self.p1[0], other.p1[0], other.p2[0]) or
                             inRange(self.p2[0], other.p1[0], other.p2[0])))
                xIntersection = (other.b - self.b) / (self.m - other.m)
                return (inRange(xIntersection, self.p1[0], self.p2[0])
                        and inRange(xIntersection, other.p1[0], other.p2[0]))
    def gridSquares(self):
        def roundGrid(val):
            return int(val / self.gridSize)
        squares = []
        if (self.vertical):
            yIter = roundGrid(self.p1[1])
            xVal = roundGrid(self.p1[0])
            yStop = roundGrid(self.p2[1])
            while yIter <= yStop:
                squares.append((xVal, yIter))
                yIter += 1
        else:
            xIter = roundGrid(self.p1[0])
            xRight = roundGrid(self.p2[0])
            while xIter <= xRight:
                yIter = roundGrid(self.m * self.gridSize * xIter + self.b)
                yRight = roundGrid(self.m * self.gridSize * (xIter + 1) + self.b)
                yDir = 1 if yRight >= yIter else -1
                while yIter != yRight:
                    squares.append((xIter, yIter))
                    yIter += yDir
                squares.append((xIter, yIter))
                xIter += 1
        return squares
