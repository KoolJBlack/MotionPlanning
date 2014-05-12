from util import *
import numpy as np

def intersectTest():
    O = np.array([0.0, 0.0])
    A = np.array([10.0,0.0])
    B = np.array([10.0,10.0])
    C = np.array([5.0, 5.0])
    D = np.array([8.0,0.0])
    E = np.array([0.0,8.0])
    F = np.array([-300.0, 0.0])
    G = np.array([0.0, 10.0])

    H = np.array([2.0, 2.0])
    I = np.array([4.0, 8.0])
    J = np.array([2.0, 4.0])
    K = np.array([4.0, 6.0])
    
    print "OG-FB T", LineSegment(O, G).intersects(LineSegment(F, B))
    print "OA-OB T", LineSegment(O, A).intersects(LineSegment(O, B))
    print "OA-DA T", LineSegment(O, A).intersects(LineSegment(D, A))
    print "EC-BA F", LineSegment(E, C).intersects(LineSegment(B, A))
    print "OD-BA F", LineSegment(O, D).intersects(LineSegment(B, A))
    print "BA-OD F", LineSegment(B, A).intersects(LineSegment(O, D))
    print "DE-BO T", LineSegment(D, E).intersects(LineSegment(B, O))
    print "OG-AB F", LineSegment(O, G).intersects(LineSegment(A, B))
    print "HI-JK T", LineSegment(H, I).intersects(LineSegment(J, K))

def main():
    intersectTest()

if __name__ == "__main__":
    main()



