from graph import *
from part1 import *

def bfs_with_color(matrix):
    n = len(matrix)
    visited = [False]*n
    bfs_tree = []

    def step(msg):
        print(msg)
        input("Press Enter to continue…")
    
    for start in range(n):
        if not visited[start] and any(matrix[start][j] for j in range(n)):
            visited[start] = True
            canvas.itemconfig(f"node_{start}", fill="lightgreen")
            root.update()
            step(f"Start BFS from node {start+1}")

            queue = [start]
            while queue:
                u = queue.pop(0)
                step(f"Popped node {u+1}")

                for v in range(n):
                    if matrix[u][v] and not visited[v]:
                        visited[v] = True
                        queue.append(v)
                        bfs_tree.append((u, v))
                        canvas.itemconfig(f"edge_{u}_{v}",
                                          fill="red",
                                          width=3)
                        canvas.itemconfig(f"node_{v}", fill="lightgreen")
                        
                        root.update()
                        step(f"  Visited node {v+1} via edge {u+1}->{v+1}")

    step("BFS complete.")
    print("BFS tree edges:", [(u+1, v+1) for u, v in bfs_tree])
    return bfs_tree

# def dfs_with_color(adj):
#     """
#     Iterative DFS over adjacency matrix `adj` using a stack.
#     - Highlights each node when first visited (lightblue).
#     - Highlights each tree‑edge when traversed (red, thicker).
#     - Pauses at every step for Enter key.
#     """
#     n = len(adj)
#     visited = [False] * n
#     dfs_tree = []

#     def step(msg):
#         print(msg)
#         input("Press Enter to continue…")

#     # For each possible starting vertex
#     for start in range(n):
#         # only start from unvisited nodes that have at least one outgoing edge
#         if not visited[start] and any(adj[start][j] for j in range(n)):
#             # mark & color the start node
#             visited[start] = True
#             canvas.itemconfig(f"node_{start}", fill="lightblue")
#             root.update()
#             step(f"Start DFS from node {start+1}")

#             # initialize stack
#             stack = [start]
#             while stack:
#                 u = stack.pop()
#                 step(f"Popped node {u+1} from stack")

#                 # explore neighbors in ascending order
#                 for v in range(n):
#                     if adj[u][v] and not visited[v]:
#                         # discover v
#                         visited[v] = True
#                         dfs_tree.append((u, v))

#                         # color the tree‑edge
#                         canvas.itemconfig(f"edge_{u}_{v}", fill="red", width=3)
#                         # color the newly visited node
#                         canvas.itemconfig(f"node_{v}", fill="lightblue")
#                         root.update()
#                         step(f"  Visit node {v+1} via edge {u+1}->{v+1}")

#                         # push the neighbor onto stack to continue deeper
#                         stack.append(v)
#                 # end for neighbors
#             # end while stack
#     # end for start

#     step("=== Iterative DFS complete ===")
#     print("DFS tree edges:", [(u+1, v+1) for u, v in dfs_tree])
#     return dfs_tree

def dfs_with_color(adj):
    n = len(adj)
    visited = [False]*n
    dfs_tree = []

    def step(msg):
        print(msg)
        input("Press Enter…")

    def dfs(u):
        step(f"  Entering dfs({u+1})")
        for v in range(n):
            if adj[u][v] and not visited[v]:
                dfs_tree.append((u, v))
                canvas.itemconfig(f"edge_{u}_{v}", fill="red", width=3)
                root.update()
                step(f"Colored edge {u+1}->{v+1}")
                visited[v] = True
                canvas.itemconfig(f"node_{v}", fill="lightblue")
                root.update()
                step(f"Discovered node {v+1}")
                dfs(v)

        step(f"Backtracking from {u+1}")
    for start in range(n):
        if not visited[start] and any(adj[start][j] for j in range(n)):
            visited[start] = True
            canvas.itemconfig(f"node_{start}", fill="lightblue")
            root.update()
            step(f"Start DFS from node {start+1}")

            dfs(start)

    step("DFS complete")
    print("DFS tree edges:", [(u+1, v+1) for u, v in dfs_tree])
    return dfs_tree

def bfs_tree_edges(adj):

    n = len(adj)
    visited = [False]*n
    edges = []

    for s in range(n):

        if not visited[s] and any(adj[s][j] for j in range(n)):
            visited[s] = True
            queue = [s]
            while queue:
                u = queue.pop(0)
                for v in range(n):
                    if adj[u][v] and not visited[v]:
                        visited[v] = True
                        edges.append((u,v))
                        queue.append(v)
    return edges

def dfs_tree_edges(adj):
    n = len(adj)
    visited = [False]*n
    edges = []

    def dfs(u):
        for v in range(n):
            if adj[u][v] and not visited[v]:
                visited[v] = True
                edges.append((u,v))
                dfs(v)

    for s in range(n):
        if not visited[s] and any(adj[s][j] for j in range(n)):
            visited[s] = True
            dfs(s)

    return edges

def edges_to_matrix(edges, n):
    M = [[0]*n for _ in range(n)]
    for u, v in edges:
        M[u][v] = 1
    return M
def show_tree(matrix, n, title):

    root.title(title)
    canvas.delete("all")
    globals()['angle'] = math.pi*2 / n
    globals()['circle_radius'] = 200
    draw_graph(matrix, n, True)
    root.update()
    input(f"Showing '{title}'.  Press Enter to continue…")

def get_bfs_order(adj):

    n = len(adj)
    visited = [False]*n
    order = []
    from collections import deque

    for s in range(n):

        if not visited[s] and any(adj[s][j] for j in range(n)):
            visited[s] = True
            q = deque([s])
            while q:
                u = q.popleft()
                order.append(u)
                for v in range(n):
                    if adj[u][v] and not visited[v]:
                        visited[v] = True
                        q.append(v)
    return order

def get_dfs_order(adj):
    n = len(adj)
    visited = [False]*n
    order = []

    def dfs(u):
        order.append(u)
        for v in range(n):
            if adj[u][v] and not visited[v]:
                visited[v] = True
                dfs(v)

    for s in range(n):
        if not visited[s] and any(adj[s][j] for j in range(n)):
            visited[s] = True
            dfs(s)
    return order


print('\nNew directed matrix:\n')
print_matrix(new_directed_matrix)
draw_graph(new_directed_matrix, nodes, True)



root.update()
input("Initial graph shown. Press Enter to continue...")

bfs_edges = bfs_tree_edges(new_directed_matrix)
dfs_edges = dfs_tree_edges(new_directed_matrix)


n = len(new_directed_matrix)
bfs_mat = edges_to_matrix(bfs_edges, n)
dfs_mat = edges_to_matrix(dfs_edges, n)

print("\nBFS‑tree adjacency matrix:")
for row in bfs_mat:
    print(row)

print("\nDFS‑tree adjacency matrix:")
for row in dfs_mat:
    print(row)

draw_graph(new_directed_matrix, n, True)
root.update()
input("Original graph displayed.  Press Enter to show BFS‑tree…")

show_tree(bfs_mat, n, "BFS‑tree")    
show_tree(dfs_mat, n, "DFS‑tree")   
bfs_order = get_bfs_order(new_directed_matrix)
dfs_order = get_dfs_order(new_directed_matrix)

print("BFS traversal order:")
for new_idx, orig in enumerate(bfs_order, start=1):
    print(f"{orig+1} -> {new_idx}")

print("\nDFS traversal order:")
for new_idx, orig in enumerate(dfs_order, start=1):
    print(f"{orig+1} -> {new_idx}")
# draw_graph(condensed_matrix, k, True)
root.mainloop()