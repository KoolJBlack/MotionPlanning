# =============================================================================
# Map Primitives
# =============================================================================
class Point:
    ''' 2D class representaiton of a point '''
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.items = [x,y]

    def __getitem__(self, index):
        return self.items[index]

    def dist_to_point(self, other):
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def __len__(self):
        return 2

    def __str__(self):
        return str(self.x) + ', ' + str(self.y) 

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

class Poly:
    ''' A poly is a list of points '''
    def __init__(self):
        self.points = []

def p2p_dist(p1, p2):
    return p1.dist_to_point(p2) 


# =============================================================================
# Line Segments
# =============================================================================

def ccw(A, B, C):
    return (C[1] - A[1])*(B[0] - A[0]) > (B[1] - A[1])*(C[0] - A[0])

"""
class LineSegment:
    ''' uses numpy points '''
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        if self.p1[0] > self.p2[0]:
            temp = self.p2
            self.p2 = self.p1
            self.p1 = temp
        v = p2 - p1
        self.vertical = (v[1] == 0)
        if self.vertical:
        if self.p1[1] > self.p2[1]:
            temp = self.p2
            self.p2 = self.p1
            self.p1 = temp            
        if not self.vertical:
            self.m = (v[1] / v[0])
            self.b = p2[1] - (self.m * p2[1])
        def intersects(self, other):
            if self.vertical:
                if other.vertical:
                    if(self.p1[0] != other.p1[0]):
                        return False
                    #mx + b
                    otherY = (other.m * self.p1[0]) + other.b
                    return (otherY >= self.p1[1]) and (otherY <= self.p2[1])
                


            
            return (ccw(self.p1, other.p1, other.p2) != ccw(self.p2, other.p1, other.p2)
            and ccw(self.p1, self.p2, other.p1) != ccw(self.p1, self.p2, other.p2))
            
"""




