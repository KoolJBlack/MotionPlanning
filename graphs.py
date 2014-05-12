from __future__ import generators
from util import *

# =============================================================================
# Visibility Graph
# =============================================================================

def shortest_path_visibility_graph(polys, start, end):
    # Create the visibility grpah
    visibility_graph = compute_visibility_graph(polys, start, end)
    # Run dijkstra
    path = shortest_path(visibility_graph, start, end)
    # Return the points in the path
    return path

def compute_visibility_graph(polys, start, end):
    # Assign an arc weight to each item in the graph
    points = get_all_points_from_polys(polys)
    points.extend([start, end])
    segments = get_all_segments_from_polys(polys)
    graph = dict()
    for index, point in enumerate(points):
        graph[point] = compute_adjacency_list(point,
                                              points[:index] + points[index + 1:],
                                              segments)
    return graph


# =============================================================================
# Graph Search Algorithms
# =============================================================================

# Priority dictionary using binary heaps
# David Eppstein, UC Irvine, 8 Mar 2002


class priorityDictionary(dict):
    def __init__(self):
        '''Initialize priorityDictionary by creating binary heap
of pairs (value,key).  Note that changing or removing a dict entry will
not remove the old pair from the heap until it is found by smallest() or
until the heap is rebuilt.'''
        self.__heap = []
        dict.__init__(self)

    def smallest(self):
        '''Find smallest item after removing deleted items from heap.'''
        if len(self) == 0:
            raise IndexError, "smallest of empty priorityDictionary"
        heap = self.__heap
        while heap[0][1] not in self or self[heap[0][1]] != heap[0][0]:
            lastItem = heap.pop()
            insertionPoint = 0
            while 1:
                smallChild = 2*insertionPoint+1
                if smallChild+1 < len(heap) and \
                        heap[smallChild] > heap[smallChild+1]:
                    smallChild += 1
                if smallChild >= len(heap) or lastItem <= heap[smallChild]:
                    heap[insertionPoint] = lastItem
                    break
                heap[insertionPoint] = heap[smallChild]
                insertionPoint = smallChild
        return heap[0][1]
        
    def __iter__(self):
        '''Create destructive sorted iterator of priorityDictionary.'''
        def iterfn():
            while len(self) > 0:
                x = self.smallest()
                yield x
                del self[x]
        return iterfn()
        
    def __setitem__(self,key,val):
        '''Change value stored in dictionary and add corresponding
pair to heap.  Rebuilds the heap if the number of deleted items grows
too large, to avoid memory leakage.'''
        dict.__setitem__(self,key,val)
        heap = self.__heap
        if len(heap) > 2 * len(self):
            self.__heap = [(v,k) for k,v in self.iteritems()]
            self.__heap.sort()  # builtin sort likely faster than O(n) heapify
        else:
            newPair = (val,key)
            insertionPoint = len(heap)
            heap.append(None)
            while insertionPoint > 0 and \
                    newPair < heap[(insertionPoint-1)//2]:
                heap[insertionPoint] = heap[(insertionPoint-1)//2]
                insertionPoint = (insertionPoint-1)//2
            heap[insertionPoint] = newPair
        
    def setdefault(self,key,val):
        '''Reimplement setdefault to call our customized __setitem__.'''
        if key not in self:
            self[key] = val
        return self[key]


# Dijkstra's algorithm for shortest paths
# David Eppstein, UC Irvine, 4 April 2002

# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/117228

def dijkstra(graph,start,end=None):
        """
        Find shortest paths from the start vertex to all
        vertices nearer than or equal to the end.

        The input graph G is assumed to have the following
        representation: A vertex can be any object that can
        be used as an index into a dictionary.  G is a
        dictionary, indexed by vertices.  For any vertex v,
        G[v] is itself a dictionary, indexed by the neighbors
        of v.  For any edge v->w, G[v][w] is the length of
        the edge.  This is related to the representation in
        <http://www.python.org/doc/essays/graphs.html>
        where Guido van Rossum suggests representing graphs
        as dictionaries mapping vertices to lists of neighbors,
        however dictionaries of edges have many advantages
        over lists: they can store extra information (here,
        the lengths), they support fast existence tests,
        and they allow easy modification of the graph by edge
        insertion and removal.  Such modifications are not
        needed here but are important in other graph algorithms.
        Since dictionaries obey iterator protocol, a graph
        represented as described here could be handed without
        modification to an algorithm using Guido's representation.

        Of course, G and G[v] need not be Python dict objects;
        they can be any other object that obeys dict protocol,
        for instance a wrapper in which vertices are URLs
        and a call to G[v] loads the web page and finds its links.

        The output is a pair (D,P) where D[v] is the distance
        from start to v and P[v] is the predecessor of v along
        the shortest path from s to v.

        Dijkstra's algorithm is only guaranteed to work correctly
        when all edge lengths are positive. This code does not
        verify this property for all edges (only the edges seen
        before the end vertex is reached), but will correctly
        compute shortest paths even for some graphs with negative
        edges, and will raise an exception if it discovers that
        a negative edge has caused it to make a mistake.
        """

        final_distances = {}    # dictionary of final distances
        predecessors = {}       # dictionary of predecessors
        estimated_distances = priorityDictionary()   # est.dist. of non-final vert.
        estimated_distances[start] = 0

        for vertex in estimated_distances:
                final_distances[vertex] = estimated_distances[vertex]
                if vertex == end: break

                for edge in graph[vertex]:
                        path_distance = final_distances[vertex] + graph[vertex][edge]
                        if edge in final_distances:
                                if path_distance < final_distances[edge]:
                                        raise ValueError, \
  "Dijkstra: found better path to already-final vertex"
                        elif edge not in estimated_distances or path_distance < estimated_distances[edge]:
                                estimated_distances[edge] = path_distance
                                predecessors[edge] = vertex

        return (final_distances,predecessors)

def shortest_path(graph,start,end):
        """
        Find a single shortest path from the given start vertex
        to the given end vertex.
        The input has the same conventions as Dijkstra().
        The output is a list of the vertices in order along
        the shortest path.
        """
        final_distances,predecessors = dijkstra(graph,start,end)
        path = []
        while 1:
                path.append(end)
                if end == start: break
                end = predecessors[end]
        path.reverse()
        return path


# =============================================================================
# Main
# =============================================================================


def main():
    # For testing
    test_graph = { 's': {'u' : 10, 'x' : 5}, 'u': {'v' : 1, 'x' : 2}, 'v': {'y' : 4}, 'x': {'u' : 3, 'v' : 9, 'y' : 2}, 'y': {'s' : 7, 'v' : 6} }
    start = 's'
    end  = 'v'

    # Get shortest path
    path = shortest_path(test_graph, start, end)
    print 'Shortest path with string graph', path

    a = Point(0, 0)
    b = Point(3, 3)
    c = Point(3, 6)
    d = Point(6, 6)

    test_graph_points = dict()
    test_graph_points[a] = compute_adjacency_list(a, [b, c])
    test_graph_points[b] = compute_adjacency_list(b, [a, c, d])
    test_graph_points[c] = compute_adjacency_list(c, [a, b, d])
    test_graph_points[d] = compute_adjacency_list(d, [b, c])

    start = a
    end = d

    # Get shortest path
    path = shortest_path(test_graph_points, start, end)
    print 'Shortest path with point graph'
    for point in path:
        print point.x, point.y




if __name__ == "__main__":
    main()
