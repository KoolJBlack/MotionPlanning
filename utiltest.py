from util import *
import numpy as np

def intersectTest():
    O = np.array([0, 0])
    A = np.array([10,0])
    B = np.array([10,10])
    C = np.array([5, 5])
    D = np.array([8,0])
    E = np.array([0,8])
    F = np.array([-300, 0])
    G = np.array([0, 10])
    
    print "OG-FB", LineSegment(O,G).intersects(LineSegment(F, B))
    print "OA-OB", LineSegment(O,A).intersects(LineSegment(O, B))
    print "OA-DA", LineSegment(O,A).intersects(LineSegment(D, A))
    


def main():
    intersectTest()

if __name__ == "__main__":
    main()



