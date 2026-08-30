# Crab Graphs

Maximum vertex coverage using vertex-disjoint crab subgraphs solved using a maximum-flow based graph transformation.

| **Property** | **Details** |
|---|---|
| Platform | HackerRank |
| Domain | Graph Theory / Network Flow |
| Problem Type | Maximum Vertex Coverage |
| Algorithm | Maximum Flow |
| Technique | Bipartite Flow Network |
| Language | Python 3 |
| Input Graph | Undirected Graph |
| Main Constraint | Each crab has at most `T` feet |
| Time Complexity | O(V²E) with the matrix-based Edmonds-Karp implementation |
| Space Complexity | O(V²) |

---

## Table of Contents

- [A. Problem Title](#a-problem-title)
- [B. Problem Statement](#b-problem-statement)
- [Graph Model](#graph-model)
- [Understanding a Crab Graph](#understanding-a-crab-graph)
- [Key Observation](#key-observation)
- [Maximum Flow Transformation](#maximum-flow-transformation)
- [Flow Network Construction](#flow-network-construction)
- [Solution Steps / Algorithm](#solution-steps--algorithm)
- [Flowchart](#flowchart)
- [Pseudocode](#pseudocode)
- [Correctness / Why the Algorithm Works](#correctness--why-the-algorithm-works)
- [Example Walkthrough](#example-walkthrough)
- [Second Example](#second-example)
- [Edge Cases](#edge-cases)
- [Complexity Analysis](#complexity-analysis)
- [Data Structures Used](#data-structures-used)
- [Technical Pipeline](#technical-pipeline)
- [Code Developed](#code-developed)
- [Repository Structure](#repository-structure)
- [Final Technical Summary](#final-technical-summary)

---

## A. Problem Title

**Crab Graphs**

---

## B. Problem Statement

A crab is an undirected graph consisting of:

- One **head** vertex.
- `K` **feet** vertices.
- Exactly `K` edges connecting the head to each of its feet.
- `1 <= K <= T`, where `T` is the maximum allowed number of feet.

Given an undirected graph, the task is to select some **vertex-disjoint crab subgraphs** so that the total number of covered vertices is maximized.

Two subgraphs are vertex-disjoint when they do not contain any common vertices.

### Objective

Find the maximum number of vertices that can be covered by a collection of vertex-disjoint crabs.

### Input Parameters

| Symbol | Meaning |
|---|---|
| `C` | Number of test cases |
| `N` | Number of vertices |
| `T` | Maximum number of feet allowed for one crab |
| `M` | Number of edges |
| `(u, v)` | An undirected edge between vertices `u` and `v` |

### Constraints

```text
1 <= C <= 10
2 <= T <= 100
2 <= N <= 100
0 <= M <= N * (N - 1) / 2
1 <= u, v <= N
```

The graph contains no parallel edges and no self-loops.

### Output

For each test case, output one integer representing the maximum number of vertices that can be covered by vertex-disjoint crab graphs.

---

## Graph Model

The original problem is an undirected graph.

| Real-World / Problem Entity | Graph Representation |
|---|---|
| Vertex | Node |
| Edge | Undirected connection |
| Crab head | Selected head vertex |
| Crab foot | Selected neighboring vertex |
| Crab | One head connected to one or more feet |
| Vertex-disjoint crabs | Crabs sharing no vertices |

For a crab with `K` feet:

```text
Number of vertices = K + 1
```

because there is one head and `K` feet.

Since:

```text
K <= T
```

a crab can contain at most:

```text
T + 1
```

vertices.

---

## Understanding a Crab Graph

A crab has one central head and several feet.

For example, if:

```text
T = 2
```

a crab can have at most two feet:

```text
       Foot
         |
         |
Foot --- Head
```

This crab contains three vertices.

For `T = 3`:

```text
        Foot
          |
Foot ---- Head ---- Foot
```

This crab contains four vertices.

The objective is not to find just one crab. Multiple crabs can be selected as long as they do not share vertices.

---

## Key Observation

The problem can be transformed into a **maximum-flow problem**.

The important idea is to create two copies of every original vertex:

1. A **head-side copy**.
2. A **foot-side copy**.

This allows the problem to separately control:

- How many feet a head can select.
- How many times a vertex can be selected as a foot.

The flow network is constructed so that every unit of flow represents the selection of one head-to-foot relationship.

---

## Maximum Flow Transformation

For every original vertex `v`, create:

```text
Head(v)
Foot(v)
```

Then create:

```text
SOURCE
SINK
```

The network has the following structure:

```text
                 HEAD SIDE             FOOT SIDE

              Head(1)  ------------  Foot(4)
                 |                       |
                 |                       |
SOURCE ----------+---- Head(2) -----> Foot(3) ---- SINK
                 |                       |
                 |                       |
              Head(5)  ------------  Foot(6)
```

The actual connections are determined by the original graph edges.

For every original undirected edge:

```text
u -- v
```

the flow network contains:

```text
Head(u) -> Foot(v)
Head(v) -> Foot(u)
```

with capacity `1`.

This represents both possible choices of the two vertices as head and foot.

---

## Flow Network Construction

### 1. Source to Head

For every vertex `v`:

```text
SOURCE -> Head(v)
```

with capacity:

```text
min(T, degree(v))
```

This means a vertex can act as a head for at most `T` feet.

The degree limit also prevents allocating more feet than the vertex actually has neighbors.

---

### 2. Head to Foot

For every original edge:

```text
u -- v
```

add:

```text
Head(u) -> Foot(v)
```

and:

```text
Head(v) -> Foot(u)
```

with capacity `1`.

This ensures that a head can select only an actual neighboring vertex as a foot.

---

### 3. Foot to Sink

For every vertex `v`:

```text
Foot(v) -> SINK
```

with capacity:

```text
1
```

This ensures that each vertex can be used as a foot at most once.

---

## Why Maximum Flow Gives the Answer

Every unit of flow corresponds to one selected head-foot edge.

Suppose a head receives `K` units of flow.

That means the corresponding vertex is selected as a crab head with `K` feet.

Because:

```text
SOURCE -> Head(v) <= T
```

the crab has at most `T` feet.

Because:

```text
Foot(v) -> SINK <= 1
```

a vertex can be used as a foot only once.

Therefore, the maximum flow gives the maximum number of selected **head-foot relationships**.

Each selected foot is one covered vertex.

However, a head can itself be a foot of another head in the flow formulation. This is why the final covered-vertex count is obtained from the number of selected relationships together with the selected head vertices.

For the standard Crab Graphs transformation used here, the maximum-flow value represents the maximum number of feet that can be assigned under the head and foot capacity constraints. The resulting coverage is determined by the selected crab structure.

---

## Solution Steps / Algorithm

1. Read the number of test cases `C`.
2. For each test case, read `N`, `T`, and `M`.
3. Read the `M` undirected edges.
4. Create a flow network containing:
   - `N` head nodes.
   - `N` foot nodes.
   - One source.
   - One sink.
5. Calculate the degree of every original vertex.
6. Add an edge from the source to every head node.
7. Give this edge capacity `min(T, degree[v])`.
8. For every original graph edge `(u, v)`:
   - Add `Head(u) -> Foot(v)` with capacity `1`.
   - Add `Head(v) -> Foot(u)` with capacity `1`.
9. Add `Foot(v) -> Sink` with capacity `1` for every vertex.
10. Run the maximum-flow algorithm.
11. Return the maximum flow value according to the flow formulation.

---

## Flowchart

```text
START
  |
  v
Read number of test cases C
  |
  v
Read N, T, M
  |
  v
Read M undirected edges
  |
  v
Calculate vertex degrees
  |
  v
Create flow network
  |
  v
Create Head and Foot
copies of every vertex
  |
  v
Add SOURCE -> HEAD
capacity = min(T, degree)
  |
  v
For every graph edge (u, v)
  |
  +----------------------------+
  |                            |
  v                            v
Head(u) -> Foot(v)       Head(v) -> Foot(u)
capacity = 1             capacity = 1
  |                            |
  +-------------+--------------+
                |
                v
       Add FOOT -> SINK
       capacity = 1
                |
                v
          Run Max Flow
                |
                v
          Store Result
                |
                v
        More test cases?
          |          |
         YES         NO
          |           |
          +---->      v
                    OUTPUT
                      |
                      v
                     END
```

---

## Pseudocode

```text
FUNCTION crabGraphs(n, t, graph)

    total_nodes = 2 * n + 2

    source = 2 * n
    sink = 2 * n + 1

    CREATE capacity[total_nodes][total_nodes]
    initialized to 0

    degree = array of n zeros

    FOR each edge (u, v) in graph

        convert u and v to zero-based indices

        degree[u] += 1
        degree[v] += 1

        capacity[u][n + v] = 1
        capacity[v][n + u] = 1

    FOR i FROM 0 TO n - 1

        capacity[source][i] = min(t, degree[i])

    FOR i FROM 0 TO n - 1

        capacity[n + i][sink] = 1

    answer = max_flow(capacity, source, sink)

    RETURN answer
```

### Maximum Flow Pseudocode

```text
FUNCTION max_flow(capacity, source, sink)

    flow = 0

    REPEAT

        Find an augmenting path from source to sink
        using BFS.

        IF no augmenting path exists

            BREAK

        Find the minimum residual capacity
        on the path.

        Update forward residual capacities.

        Update reverse residual capacities.

        Add path flow to flow.

    RETURN flow
```

---

## Correctness / Why the Algorithm Works

The flow network enforces the main restrictions of the crab graph.

### 1. A head can have at most `T` feet

The capacity:

```text
SOURCE -> Head(v) = min(T, degree(v))
```

limits the amount of flow leaving each head.

Therefore, no head can be assigned more than `T` feet.

---

### 2. A foot must be adjacent to its head

A flow connection from a head to a foot is created only when the corresponding vertices are connected by an edge in the original graph.

Therefore, every selected head-foot relationship corresponds to a valid edge of the original graph.

---

### 3. A vertex can be used as a foot at most once

Every foot node has:

```text
Foot(v) -> SINK = 1
```

Therefore, at most one unit of flow can pass through each foot node.

This prevents the same vertex from being selected as a foot multiple times.

---

### 4. Maximum flow maximizes the number of selected relationships

Every unit of flow represents one valid head-foot assignment.

Therefore, maximizing flow maximizes the number of valid assignments subject to the crab constraints.

The flow construction provides the required combinatorial optimization framework for selecting the maximum possible collection of crab structures.

---

## Example Walkthrough

### Test Case 1

Input:

```text
N = 8
T = 2
M = 7
```

Edges:

```text
1 4
2 4
3 4
5 4
5 8
5 7
5 6
```

The graph can be viewed as two dense regions around vertices `4` and `5`.

Because:

```text
T = 2
```

each crab can contain at most:

```text
1 head + 2 feet = 3 vertices
```

One valid selection is:

```text
Crab 1:
Head = 4
Feet = 1, 3

Crab 2:
Head = 5
Feet = 7, 8
```

The covered vertices are:

```text
{1, 3, 4, 5, 7, 8}
```

Total:

```text
6 vertices
```

Therefore:

```text
Output = 6
```

Another valid selection could use:

```text
Head 4 -> Feet 1, 2
Head 5 -> Feet 6, 7
```

which also covers six vertices.

---

## Second Example

### Test Case 2

Input:

```text
N = 6
T = 3
M = 8
```

Edges:

```text
1 2
2 3
3 4
4 5
5 6
6 1
1 4
2 5
```

A valid selection is:

```text
Crab 1:
Head = 2
Feet = 1, 3

Crab 2:
Head = 5
Feet = 4, 6
```

All six vertices are covered:

```text
{1, 2, 3, 4, 5, 6}
```

Therefore:

```text
Output = 6
```

---

## Sample Input

```text
2
8 2 7
1 4
2 4
3 4
5 4
5 8
5 7
5 6
6 3 8
1 2
2 3
3 4
4 5
5 6
6 1
1 4
2 5
```

## Sample Output

```text
6
6
```

---

## Edge Cases

| Edge Case | Expected Behaviour |
|---|---|
| `M = 0` | No crab can contain an edge, so coverage is `0` |
| `T = 2` | Every head can have at most 2 feet |
| `T` greater than vertex degree | Head capacity is limited by its degree |
| Isolated vertex | It cannot form a crab as a head or foot |
| Single edge | At most one head-foot pair can be selected |
| Multiple disconnected components | Flow network processes all components independently |
| Dense graph | Many possible head-foot assignments exist |
| Vertex already used as foot | Its foot capacity prevents another use |

---

## Complexity Analysis

Let:

```text
V = N
E = M
```

The flow network contains:

```text
2N + 2
```

nodes.

The original graph contributes up to two directed head-to-foot edges per undirected edge.

The implementation uses a **capacity matrix** and **BFS-based augmenting paths**, corresponding to the Edmonds-Karp style maximum-flow approach.

### Number of Flow-Network Vertices

```text
O(N)
```

### Capacity Matrix

The capacity matrix requires:

```text
O(N²)
```

space because the flow network has `2N + 2` nodes.

### Maximum Flow

For Edmonds-Karp, the worst-case time complexity is:

```text
O(V E²)
```

where `V` and `E` refer to the vertices and edges of the flow network.

Because this implementation searches the capacity matrix during BFS, the practical implementation can be expressed in terms of the transformed network size as approximately:

```text
O(V_f² × F)
```

where `V_f = 2N + 2` and `F` is the number of augmentations.

For the constraints of this problem (`N <= 100`), the matrix-based implementation is manageable.

### Space Complexity

The dominant structure is:

```text
capacity = O(N²)
```

Therefore:

```text
Space Complexity = O(N²)
```

---

## Data Structures Used

| Data Structure | Purpose |
|---|---|
| `graph` | Stores the original undirected edges |
| `degree` | Stores the degree of every original vertex |
| `capacity` | Stores residual capacities of the flow network |
| `deque` | Implements BFS queue |
| `parent` | Stores the augmenting path |
| Integer variables | Store capacities and flow values |

---

## Why BFS Is Used

The maximum-flow implementation uses **Breadth-First Search (BFS)** to find an augmenting path from the source to the sink.

BFS is suitable because it systematically searches the residual network for a path and works well with the Edmonds-Karp maximum-flow method.

The `parent` array records how each node was reached so that, once the sink is found, the algorithm can reconstruct the path and update the residual capacities.

---

## Residual Graph

During maximum flow, the capacity matrix represents the current residual network.

When flow is sent from:

```text
u -> v
```

the forward capacity decreases:

```text
capacity[u][v] -= flow
```

and the reverse capacity increases:

```text
capacity[v][u] += flow
```

This allows the algorithm to reconsider previous choices and redirect flow when a better solution becomes possible.

---

## Technical Pipeline

```text
Original Undirected Graph
          |
          v
Calculate Vertex Degrees
          |
          v
Create Head / Foot Copies
          |
          v
SOURCE -> HEAD
Capacity = min(T, degree)
          |
          v
HEAD -> FOOT
Capacity = 1 for Graph Edges
          |
          v
FOOT -> SINK
Capacity = 1
          |
          v
Residual Flow Network
          |
          v
BFS Augmenting Paths
          |
          v
Maximum Flow
          |
          v
Maximum Valid Crab Coverage
```

---

## Code Developed

The solution is implemented in **Python 3**.

### Key Implementation Characteristics

- Supports multiple test cases.
- Converts the undirected graph into a flow network.
- Creates separate head and foot nodes for every original vertex.
- Uses vertex degree to limit source-to-head capacity.
- Uses capacity `1` for head-to-foot relationships.
- Uses capacity `1` from every foot to the sink.
- Uses BFS to find augmenting paths.
- Maintains a residual capacity matrix.
- Returns the computed maximum-flow value.
- Uses the HackerRank `OUTPUT_PATH` format in the submission template.

### Main Flow-Network Construction

```python
for u, v in graph:

    u -= 1
    v -= 1

    degree[u] += 1
    degree[v] += 1

    capacity[u][n + v] = 1
    capacity[v][n + u] = 1
```

### Source-to-Head Capacity

```python
for i in range(n):
    capacity[source][i] = min(t, degree[i])
```

### Foot-to-Sink Capacity

```python
for i in range(n):
    capacity[n + i][sink] = 1
```

---

## Program Input Format

The program first reads:

```text
C
```

where `C` is the number of test cases.

For every test case:

```text
N T M
```

is entered, followed by `M` lines containing graph edges.

Example:

```text
2
8 2 7
1 4
2 4
3 4
5 4
5 8
5 7
5 6
6 3 8
1 2
2 3
3 4
4 5
5 6
6 1
1 4
2 5
```

---

## Program Output

For each test case, the program writes one integer.

For the sample:

```text
6
6
```

The values represent the maximum coverage calculated by the implemented flow formulation.

---

## Repository Structure

```text
Crab-Graphs/
│
├── README.md
├── crab_graphs.py
└── report/
    └── Crab_Graphs_Report.pdf
```

### File Description

| File | Description |
|---|---|
| `README.md` | Problem explanation, graph transformation, algorithm, examples, and analysis |
| `crab_graphs.py` | Python implementation |
| `report/Crab_Graphs_Report.pdf` | Supporting written report |

---

## Final Technical Summary

```text
Problem
   ↓
Undirected Graph
   ↓
Crab Graph Modeling
   ↓
Separate Head and Foot Copies
   ↓
Build Flow Network
   ↓
Source → Head Capacity
   ↓
Head → Foot Capacity
   ↓
Foot → Sink Capacity
   ↓
Residual Network
   ↓
BFS Augmenting Paths
   ↓
Maximum Flow
   ↓
Maximum Crab Coverage
```

The Crab Graphs problem is transformed into a network-flow optimization problem.

Each original vertex is represented on both the head side and the foot side. Source capacities enforce the maximum number of feet a head can have, while foot-to-sink capacities ensure that each vertex can be used as a foot at most once. Original graph edges determine which head-foot assignments are possible.

The maximum-flow algorithm then finds the largest feasible collection of head-foot assignments under these constraints.
