#!/bin/python3

import os
from collections import deque


def max_flow(capacity, source, sink):
    n = len(capacity)
    flow = 0

    while True:
        parent = [-1] * n
        parent[source] = source

        queue = deque([source])

        # BFS to find an augmenting path
        while queue and parent[sink] == -1:
            u = queue.popleft()

            for v in range(n):
                if parent[v] == -1 and capacity[u][v] > 0:
                    parent[v] = u
                    queue.append(v)

                    if v == sink:
                        break

        # No augmenting path
        if parent[sink] == -1:
            break

        # Find minimum capacity on the path
        path_flow = float('inf')
        v = sink

        while v != source:
            u = parent[v]
            path_flow = min(path_flow, capacity[u][v])
            v = u

        # Update residual capacities
        v = sink

        while v != source:
            u = parent[v]

            capacity[u][v] -= path_flow
            capacity[v][u] += path_flow

            v = u

        flow += path_flow

    return flow


#
# Complete the 'crabGraphs' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER n
#  2. INTEGER t
#  3. 2D_INTEGER_ARRAY graph
#

def crabGraphs(n, t, graph):

    # Total nodes in flow network:
    #
    # Original vertices:
    #   0 ... n-1       -> Head side
    #   n ... 2n-1      -> Foot side
    #
    # Plus:
    #   source
    #   sink
    #
    total_nodes = 2 * n + 2

    source = 2 * n
    sink = 2 * n + 1

    # Capacity matrix
    capacity = [
        [0 for _ in range(total_nodes)]
        for _ in range(total_nodes)
    ]

    # Degree of each original vertex
    degree = [0] * n

    # --------------------------------------------------
    # Build head -> foot connections
    # --------------------------------------------------

    for u, v in graph:

        # Convert from 1-based to 0-based
        u -= 1
        v -= 1

        degree[u] += 1
        degree[v] += 1

        # u can be head and v can be its foot
        capacity[u][n + v] = 1

        # v can be head and u can be its foot
        capacity[v][n + u] = 1

    # --------------------------------------------------
    # Source -> head
    # A head can have at most T feet.
    #
    # Also, a head cannot have more feet than
    # its actual degree.
    # --------------------------------------------------

    for i in range(n):

        capacity[source][i] = min(t, degree[i])

    # --------------------------------------------------
    # Foot -> sink
    #
    # Each vertex can be used as a foot only once.
    # --------------------------------------------------

    for i in range(n):

        capacity[n + i][sink] = 1

    # --------------------------------------------------
    # Calculate maximum flow
    # --------------------------------------------------

    return max_flow(capacity, source, sink)


if __name__ == '__main__':

    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    c = int(input().strip())

    for c_itr in range(c):

        first_multiple_input = input().rstrip().split()

        n = int(first_multiple_input[0])
        t = int(first_multiple_input[1])
        m = int(first_multiple_input[2])

        graph = []

        for _ in range(m):
            graph.append(
                list(map(int, input().rstrip().split()))
            )

        result = crabGraphs(n, t, graph)

        fptr.write(str(result) + '\n')

    fptr.close()
