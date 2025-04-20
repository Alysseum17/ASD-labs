from graph import *
def print_matrix(matrix):
  n = len(matrix)
  for i in range(n):
    for j in range(n):
      print(matrix[i][j], end = ' ')
    print()
def get_undirected_degrees(matrix):
  n = len(matrix)
  undirected_nodes_degrees = [0] * n
  for i in range(n):
    for j in range(n):
      undirected_nodes_degrees[i] += matrix[i][j]
  return undirected_nodes_degrees
def get_directed_in_out_degrees(matrix):
  n = len(matrix)
  directed_nodes_degrees = [0] * n
  in_degs =  [0] * n
  out_degs = [0] * n
  for i in range(n):
    for j in range(n):
      in_degs[i] += matrix[j][i]
      out_degs[i] += matrix[i][j]
      if matrix[i][j] == matrix[j][i]:
        directed_nodes_degrees[i] += matrix[i][j]
      else:
        directed_nodes_degrees[i] += matrix[i][j] + matrix[j][i]
  return directed_nodes_degrees, in_degs,out_degs

def is_regular_matrix(nodes_degrees):
  is_regular = True
  for i in range(len(nodes_degrees)):
    if i > 0:
      if nodes_degrees[i] != nodes_degrees[i-1]:
          is_regular = False
  if is_regular:
    print('Matrix is regular')
  else:
    print('Matrix is not regular')

def has_hanging_isolated_nodes(nodes_degrees):
  hanging_nodes = []
  isolated_nodes = []
  has_hanging = False
  has_isolated = False
  for i in range(len(nodes_degrees)):
    if nodes_degrees[i] == 1:
      hanging_nodes.append(i)
      has_hanging = True
    if nodes_degrees[i] == 0:
      isolated_nodes.append(i)
      has_isolated = True
  if has_hanging: 
    for i in range(len(hanging_nodes)):
      print(f'Node {i+1} is hanging')
    print()
  else:
    print('Matrix has not hanging nodes')
  if has_isolated:
    for i in range(len(isolated_nodes)):
      print(f'Node {i+1} is isolated')
    print()
  else:
    print('Matrix has not isolated nodes')

undirected_nodes_degrees = get_undirected_degrees(undirected_matrix)
directed_nodes_degrees, in_degs,out_degs = get_directed_in_out_degrees(directed_matrix)

print('\nUndirected matrix:\n')
for i in range(len(undirected_matrix)):
  print(f'Node {i+1} has degrees {undirected_nodes_degrees[i]}')
  print()
is_regular_matrix(undirected_nodes_degrees)
has_hanging_isolated_nodes(undirected_nodes_degrees)

print('\nDirected matrix:\n')
for i in range(len(undirected_matrix)):
  print(f'Node {i+1} has degrees {directed_nodes_degrees[i]}')  
  print(f'Node {i+1} has in degrees {in_degs[i]}')
  print(f'Node {i+1} has out degrees {out_degs[i]}')
  print()
is_regular_matrix(directed_nodes_degrees)
has_hanging_isolated_nodes(directed_nodes_degrees)

