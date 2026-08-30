# Store a Sparse Graph Using CSR Format

Sparse graph representation using **Compressed Sparse Row (CSR)** format.

| Property | Details |
|---|---|
| Domain | Graph / Data Structures |
| Representation | Compressed Sparse Row (CSR) |
| Input | Adjacency Matrix |
| Output | CSR Arrays + Reconstructed Graph |
| Language | Python |
| Time Complexity | O(n²) |
| Space Complexity | O(n²) worst case |

---

## Table of Contents

- [A. Problem Title](#a-problem-title)
- [B. Problem Statement](#b-problem-statement)
- [Graph Model](#graph-model)
- [Understanding Sparse Graphs](#understanding-sparse-graphs)
- [CSR Representation](#csr-representation)
- [Key Observation](#key-observation)
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

**Store a Sparse Graph Using CSR Format**

---

## B. Problem Statement

Write a program to convert an adjacency matrix into a simple **Compressed Sparse Row (CSR)** representation.

The program accepts an adjacency matrix representing a sparse graph and identifies all non-zero entries row by row.

The non-zero values and their corresponding column indices are stored in separate arrays. A row pointer array is then created to identify the range of entries belonging to each row.

Finally, the program displays the CSR representation and reconstructs the adjacency matrix from the CSR arrays to verify that the graph information has been preserved.

### Required Operations

1. Accept the number of vertices.
2. Accept the adjacency matrix.
3. Identify all non-zero entries row by row.
4. Store the non-zero values.
5. Store their column indices.
6. Create the row pointer array.
7. Display the CSR representation.
8. Reconstruct the adjacency matrix.
9. Display the reconstructed graph.

---

## Graph Model

The adjacency matrix represents the graph using rows and columns.

| Graph Entity | Representation |
|---|---|
| Vertex | Matrix row/column |
| Edge | Non-zero matrix entry |
| Edge value | Non-zero matrix value |
| No edge | Zero matrix entry |
| Sparse graph | Graph containing relatively few non-zero entries |

For a graph with `n` vertices, the adjacency matrix contains `n × n` entries.

---

## Understanding Sparse Graphs

A sparse graph contains relatively few edges compared with the maximum possible number of edges.

When represented using an adjacency matrix, this means that a large number of matrix entries are zero.

For example:

```text
0 5 0 0
5 0 3 0
0 3 0 7
0 0 7 0
```

Most entries in this matrix are zero.

CSR representation avoids storing these zero entries. Instead, it stores only the non-zero values and enough information to determine their original positions.

---

## CSR Representation

Compressed Sparse Row representation uses three main arrays:

### 1. Values

The `values` array stores all non-zero entries of the matrix in row-major order.

Example:

```text
Values = [5, 5, 3, 3, 7, 7]
```

### 2. Column Index

The `column_index` array stores the column position corresponding to every value in `values`.

Example:

```text
Column Index = [1, 0, 2, 1, 3, 2]
```

### 3. Row Pointer

The `row_pointer` array identifies where each row begins and ends in the `values` and `column_index` arrays.

Example:

```text
Row Pointer = [0, 1, 3, 5, 6]
```

The first value is always `0`.

The final value equals the total number of non-zero entries.

---

## Key Observation

The matrix can be converted into CSR by scanning it row by row.

For every matrix element:

```text
IF matrix[i][j] != 0
    store matrix[i][j] in values
    store j in column_index
```

After an entire row has been processed:

```text
row_pointer.append(len(values))
```

This records the boundary of that row inside the CSR arrays.

---

## Solution Steps / Algorithm

1. Read the number of vertices `n`.
2. Read the `n × n` adjacency matrix.
3. Initialize an empty `values` list.
4. Initialize an empty `column_index` list.
5. Initialize `row_pointer` with `[0]`.
6. Traverse every row of the matrix.
7. Traverse every column in the current row.
8. If the matrix value is non-zero:
   - Append the value to `values`.
   - Append its column index to `column_index`.
9. After completing each row, append the current length of `values` to `row_pointer`.
10. Display the three CSR arrays.
11. Create an `n × n` matrix filled with zeroes.
12. Use the row pointer values to determine which CSR entries belong to each row.
13. Use `column_index` to determine the original column.
14. Use `values` to restore the original non-zero value.
15. Display the reconstructed adjacency matrix.

---

## Flowchart

```text
START
  |
  v
Read number of vertices n
  |
  v
Read adjacency matrix
  |
  v
Initialize:
values = []
column_index = []
row_pointer = [0]
  |
  v
Process each row
  |
  v
Process each column
  |
  v
Is matrix[i][j] != 0?
  |                 |
 YES                NO
  |                 |
  v                 |
Store value         |
Store column index |
  |                 |
  +-------<---------+
  |
  v
End of row?
  |
 YES
  |
  v
Append len(values)
to row_pointer
  |
  v
All rows processed?
  |
 YES
  |
  v
Display CSR arrays
  |
  v
Reconstruct adjacency matrix
  |
  v
Display reconstructed graph
  |
  v
END
```

---

## Pseudocode

```text
FUNCTION convertToCSR(matrix, n)

    values = empty list
    column_index = empty list
    row_pointer = [0]

    FOR i FROM 0 TO n - 1

        FOR j FROM 0 TO n - 1

            IF matrix[i][j] != 0

                APPEND matrix[i][j] TO values
                APPEND j TO column_index

        APPEND length(values) TO row_pointer

    RETURN values, column_index, row_pointer


FUNCTION reconstructGraph(values, column_index, row_pointer, n)

    reconstructed = n × n matrix filled with 0

    FOR i FROM 0 TO n - 1

        FOR k FROM row_pointer[i] TO row_pointer[i + 1] - 1

            j = column_index[k]

            reconstructed[i][j] = values[k]

    RETURN reconstructed
```

---

## Correctness / Why the Algorithm Works

The algorithm correctly converts the adjacency matrix into CSR format because every non-zero matrix entry is processed exactly once.

For every non-zero entry:

- Its value is stored in `values`.
- Its column position is stored in `column_index`.
- Its row is represented by the corresponding range in `row_pointer`.

The `row_pointer` array contains one additional value beyond the number of rows. This allows the program to determine the starting and ending positions of every row in the CSR arrays.

During reconstruction, for every row `i`, the program processes the CSR entries from:

```text
row_pointer[i]
```

through:

```text
row_pointer[i + 1] - 1
```

The corresponding column is obtained from `column_index`, while the original matrix value is obtained from `values`.

Therefore, every stored non-zero entry is restored to its original row and column, while all unstored positions remain zero.

Hence, the reconstructed adjacency matrix preserves the graph information of the original matrix.

---

## Example Walkthrough

### Input

Number of vertices:

```text
4
```

Adjacency matrix:

```text
0 5 0 0
5 0 3 0
0 3 0 7
0 0 7 0
```

### Step 1 — Process Row 0

```text
0 5 0 0
```

Non-zero entry:

```text
Value = 5
Column = 1
```

Arrays:

```text
Values       = [5]
Column Index = [1]
Row Pointer  = [0, 1]
```

### Step 2 — Process Row 1

```text
5 0 3 0
```

Non-zero entries:

```text
Value = 5, Column = 0
Value = 3, Column = 2
```

Arrays:

```text
Values       = [5, 5, 3]
Column Index = [1, 0, 2]
Row Pointer  = [0, 1, 3]
```

### Step 3 — Process Row 2

```text
0 3 0 7
```

Non-zero entries:

```text
Value = 3, Column = 1
Value = 7, Column = 3
```

Arrays:

```text
Values       = [5, 5, 3, 3, 7]
Column Index = [1, 0, 2, 1, 3]
Row Pointer  = [0, 1, 3, 5]
```

### Step 4 — Process Row 3

```text
0 0 7 0
```

Non-zero entry:

```text
Value = 7
Column = 2
```

Final CSR representation:

```text
Values       = [5, 5, 3, 3, 7, 7]
Column Index = [1, 0, 2, 1, 3, 2]
Row Pointer  = [0, 1, 3, 5, 6]
```

---

## CSR Interpretation

The row pointer array:

```text
[0, 1, 3, 5, 6]
```

can be interpreted as:

| Row | Start | End | Number of Non-Zero Entries |
|---:|---:|---:|---:|
| 0 | 0 | 1 | 1 |
| 1 | 1 | 3 | 2 |
| 2 | 3 | 5 | 2 |
| 3 | 5 | 6 | 1 |

For example, row `1` uses CSR positions:

```text
1 to 2
```

Therefore:

```text
Values       → [5, 3]
Column Index → [0, 2]
```

which reconstructs:

```text
5 0 3 0
```

---

## Reconstruction

Using the CSR arrays, the program reconstructs:

```text
0 5 0 0
5 0 3 0
0 3 0 7
0 0 7 0
```

This is identical to the original adjacency matrix.

---

## Second Example

Consider:

```text
0 0 4
0 0 0
4 0 0
```

The non-zero entries are:

```text
Value = 4, Column = 2
Value = 4, Column = 0
```

CSR representation:

```text
Values       = [4, 4]
Column Index = [2, 0]
Row Pointer  = [0, 1, 1, 2]
```

The second value in `row_pointer` remains `1` because row `1` contains no non-zero entries.

Reconstruction gives:

```text
0 0 4
0 0 0
4 0 0
```

---

## Edge Cases

| Edge Case | Expected Behaviour |
|---|---|
| `n = 1` | Process the single matrix element |
| All entries are `0` | `values` and `column_index` remain empty |
| One non-zero entry | One value and one column index are stored |
| Empty rows | Consecutive values in `row_pointer` may be equal |
| Self-loop | Non-zero diagonal value is stored normally |
| Negative value | Stored because it is non-zero |
| Fully dense matrix | Almost every matrix entry is stored |

### All-Zero Example

Input:

```text
0 0 0
0 0 0
0 0 0
```

CSR:

```text
Values       = []
Column Index = []
Row Pointer  = [0, 0, 0, 0]
```

This correctly indicates that there are no non-zero graph entries.

---

## Complexity Analysis

Let `n` be the number of vertices and `k` be the number of non-zero entries.

### Matrix Traversal

The program checks every position of the adjacency matrix.

There are:

```text
n × n
```

positions.

Therefore:

```text
Time Complexity = O(n²)
```

### CSR Storage

The CSR arrays store:

```text
values       → O(k)
column_index → O(k)
row_pointer  → O(n)
```

Therefore:

```text
CSR Space = O(n + k)
```

For a sparse graph, `k` is much smaller than `n²`, so CSR can use considerably less storage for the non-zero graph information.

### Reconstruction

The reconstruction processes every non-zero CSR entry and every row:

```text
O(n + k)
```

### Overall

| Phase | Time | Space |
|---|---:|---:|
| Read matrix | O(n²) | O(n²) |
| CSR conversion | O(n²) | O(n + k) |
| Reconstruction | O(n + k) | O(n²) |
| **Overall** | **O(n²)** | **O(n²)** |

The overall space is `O(n²)` because the program initially accepts and later reconstructs the full adjacency matrix. The CSR representation itself requires only `O(n + k)` space.

---

## Data Structures Used

| Data Structure | Purpose |
|---|---|
| `matrix` | Stores the input adjacency matrix |
| `values` | Stores non-zero matrix values |
| `column_index` | Stores column indices of non-zero values |
| `row_pointer` | Stores row boundaries in CSR arrays |
| `reconstructed` | Stores the reconstructed adjacency matrix |
| Python `list` | Used for all array-like structures |

---

## Technical Pipeline

```text
Adjacency Matrix
       |
       v
Scan Row by Row
       |
       v
Identify Non-Zero Entries
       |
       +------------------+
       |                  |
       v                  v
Store Values       Store Column Indices
       |                  |
       +---------+--------+
                 |
                 v
        Create Row Pointer
                 |
                 v
        CSR Representation
                 |
                 v
       Reconstruct Matrix
                 |
                 v
       Display Graph
```

---

## Code Developed

The solution is implemented in Python.

### Key Implementation Characteristics

- The number of vertices is accepted from the user.
- The adjacency matrix is entered row by row.
- Every matrix entry is checked.
- Zero entries are ignored during CSR conversion.
- Non-zero values are stored in `values`.
- Their column positions are stored in `column_index`.
- `row_pointer` is updated after every row.
- The CSR representation is displayed.
- A new matrix is created for reconstruction.
- CSR arrays are used to restore the original graph information.
- The reconstructed adjacency matrix is displayed.

### Main CSR Conversion Logic

```python
values = []
column_index = []
row_pointer = [0]

for i in range(n):
    for j in range(n):
        if matrix[i][j] != 0:
            values.append(matrix[i][j])
            column_index.append(j)

    row_pointer.append(len(values))
```

### Main Reconstruction Logic

```python
reconstructed = [[0 for j in range(n)] for i in range(n)]

for i in range(n):
    for k in range(row_pointer[i], row_pointer[i + 1]):
        j = column_index[k]
        reconstructed[i][j] = values[k]
```

---

## Program Output Format

The program displays:

```text
--- CSR Representation ---

Values: [...]
Column Index: [...]
Row Pointer: [...]

--- Reconstructed Graph / Adjacency Matrix ---

...
```

The reconstructed matrix can be compared with the original input matrix to verify correctness.

---

## Repository Structure

```text
Store-Sparse-Graph-CSR/
│
├── README.md
├── sparse_graph_csr.py
└── report/
    └── Store_Sparse_Graph_CSR_Report.pdf
```

### File Description

| File | Description |
|---|---|
| `README.md` | Problem explanation, CSR representation, algorithm, examples, and analysis |
| `sparse_graph_csr.py` | Python implementation |
| `report/Store_Sparse_Graph_CSR_Report.pdf` | Supporting written report |

---

## Final Technical Summary

```text
Problem
   ↓
Adjacency Matrix Input
   ↓
Identify Non-Zero Entries
   ↓
Store Values
   ↓
Store Column Indices
   ↓
Create Row Pointer
   ↓
CSR Representation
   ↓
Reconstruct Adjacency Matrix
   ↓
Verify Graph Information
```

The program demonstrates how a sparse graph represented by an adjacency matrix can be converted into a simple CSR representation.

The three CSR arrays — `values`, `column_index`, and `row_pointer` — collectively preserve the locations and values of all non-zero entries.

The final reconstruction verifies that the CSR representation retains the original graph information.
