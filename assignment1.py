# Store a Sparse Graph Using CSR Format

# Accept number of vertices
n = int(input("Enter number of vertices: "))

# Accept adjacency matrix
print("Enter the adjacency matrix:")
matrix = []

for i in range(n):
    row = list(map(int, input().split()))
    matrix.append(row)

# CSR arrays
values = []
column_index = []
row_pointer = [0]

# Convert adjacency matrix to CSR format
for i in range(n):
    for j in range(n):
        if matrix[i][j] != 0:
            values.append(matrix[i][j])
            column_index.append(j)

    row_pointer.append(len(values))

# Display CSR representation
print("\n--- CSR Representation ---")

print("Values:", values)
print("Column Index:", column_index)
print("Row Pointer:", row_pointer)

# Reconstruct adjacency matrix
reconstructed = [[0 for j in range(n)] for i in range(n)]

for i in range(n):
    for k in range(row_pointer[i], row_pointer[i + 1]):
        j = column_index[k]
        reconstructed[i][j] = values[k]

# Display reconstructed graph
print("\n--- Reconstructed Graph / Adjacency Matrix ---")

for row in reconstructed:
    print(*row)
