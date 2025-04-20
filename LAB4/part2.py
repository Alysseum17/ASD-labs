from graph import *
from part1 import *

def matrix_multiply(A,B):
  n = len(A)
  C = [[0 for _ in range(n)] for _ in range(n)]
  for i in range(n):
    for j in range(n):
      s = 0
      for k in range(n):
        s += A[i][k] * B[k][j]
      C[i][j] = s
  return C
def matrix_power(A,power):
  result = A
  for _ in range(power-1):
    result = matrix_multiply(result,A)
  return result

def matrix_sum(A, B):
  n = len(A)
  C = [[0 for _ in range(n)] for _ in range(n)]
  for i in range(n):
      for j in range(n):
          C[i][j] = A[i][j] + B[i][j]
  return C

def boolean_transform(A):
  n = len(A)
  for i in range(n):
    for j in range(n):
        A[i][j] = 1 if A[i][j] > 0 else 0 
  return A

def print_paths_length_2(matrix):
    n = len(matrix)
    matrix_2_power = matrix_power(matrix,2)
    for i in range(n):
        for j in range(n):
            if matrix_2_power[i][j] > 0:
              for k in range(n):
                  if matrix[i][k] == 1 and matrix[k][j] == 1:
                      print(f"{i+1} -> {k+1} -> {j+1}")

def print_paths_length_3(matrix):
    n = len(matrix)
    matrix_3_power = matrix_power(matrix,3)
    for i in range(n):
        for j in range(n):
            if matrix_3_power[i][j] > 0:
              for k in range(n):
                  for p in range(n):
                    if matrix[i][k] == 1 and matrix[k][p] == 1 and matrix[p][j]:
                      print(f"{i+1} -> {k+1} -> {p+1} -> {j+1}")

def reachability_matrix_method(matrix):
  n = len(matrix)
  sum_matrix = [[0 for _ in range(n)] for _ in range(n)]
  for power in range(1,n+1):
     powered_matrix = matrix_power(matrix,power)
     sum_matrix = matrix_sum(sum_matrix,powered_matrix)
  reachability_matrix = boolean_transform(sum_matrix)
  return reachability_matrix

def transpose_matrix(matrix):
  n = len(matrix)
  transposed_matrix = [[0 for _ in range(n)] for _ in range(n)]
  for i in range(n):
    for j in range(n):
        transposed_matrix[i][j] = matrix[j][i]
  return transposed_matrix
def strong_connectivity_matrix(matrix):
   return boolean_transform(matrix_multiply(matrix,transpose_matrix(matrix)))
def find_strong_components(reach_matrix):
  n = len(reach_matrix)
  is_visited = [False] * n
  strong_components = []
  
  for node in range(n):
      if not is_visited[node]:
          is_visited[node] = True
          component = [node + 1]
          for another_node in range(n):
              if reach_matrix[node][another_node] == 1 and reach_matrix[another_node][node] == 1 and node != another_node and not is_visited[another_node]:
                  component.append(another_node + 1)  
                  is_visited[another_node] = True
          strong_components.append(component)

  return strong_components
def create_condensation_matrix(matrix, components):
    k = len(components)
    cond_mat = [[0] * k for _ in range(k)]
    owner = {}
    for comp_id, comp in enumerate(components):
        for v1 in comp:
            owner[v1 - 1] = comp_id
    for u, row in enumerate(matrix):
        for v, has_edge in enumerate(row):
            if has_edge:
                cu = owner[u]
                cv = owner[v]
                if cu != cv:
                    cond_mat[cu][cv] = 1

    return cond_mat
print('\nNew directed matrix:\n')
print_matrix(new_directed_matrix)
new_directed_nodes_degrees, in_degs,out_degs = get_directed_in_out_degrees(new_directed_matrix)
for i in range(len(new_directed_matrix)):
  print(f'Node {i+1} has degrees {new_directed_nodes_degrees[i]}')  
  print(f'Node {i+1} has in degrees {in_degs[i]}')
  print(f'Node {i+1} has out degrees {out_degs[i]}')
  print()
is_regular_matrix(new_directed_nodes_degrees)
has_hanging_isolated_nodes(new_directed_nodes_degrees)
print('\nDirected matrix(2 power):\n')
matrix_2_power = matrix_power(new_directed_matrix,2)
print_matrix(matrix_2_power)
print_paths_length_2(new_directed_matrix)

print('\nDirected matrix(3 power):\n')

matrix_3_power = matrix_power(new_directed_matrix,3)
print_matrix(matrix_3_power)
print_paths_length_3(new_directed_matrix)

print('\nReachability matrix:\n')
reachability_matrix = reachability_matrix_method(new_directed_matrix)
print_matrix(reachability_matrix)

print('\nStrong connectivity matrix:\n')
strong_connectivity_matrix = strong_connectivity_matrix(reachability_matrix_method(new_directed_matrix))
for i in range(nodes):
    for j in range(nodes):
      print(strong_connectivity_matrix[i][j], end = ' ')
    print()
print('\nStrong connectivity components\n')
strong_components = find_strong_components(reachability_matrix)
for i in range(len(strong_components)):
   print(f'{i+1} strong component: {strong_components[i]}\n')
print('\nCondensation\n')
condensed_matrix = create_condensation_matrix(new_directed_matrix,strong_components)
print(condensed_matrix)
k = len(condensed_matrix)
draw_graph(directed_matrix, nodes,1)
input("Enter to show next graph")
canvas.delete("all")
draw_graph(undirected_matrix, nodes, 0)
input("Enter to show next graph")
canvas.delete("all")
draw_graph(new_directed_matrix, nodes,1)
input("Enter to show condensed graph")
canvas.delete("all")
draw_graph(condensed_matrix, k, 1)
root.mainloop()