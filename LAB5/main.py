from graph import *
from help import *

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

def dfs_with_color(adj):
    n = len(adj)
    visited = [False] * n
    dfs_tree = []

    def step(msg):
        print(msg)
        input("Press Enter…")

    for start in range(n):
        if not visited[start] and any(adj[start][j] for j in range(n)):
            visited[start] = True
            canvas.itemconfig(f"node_{start}", fill="lightblue")
            root.update()
            step(f"Start DFS from node {start+1}")
            stack = [(start, 0)]
            step(f"  Entering dfs({start+1})")
            while stack:
                u, idx = stack[-1]
                while idx < n and not (adj[u][idx] and not visited[idx]):
                    idx += 1
                if idx < n:
                    v = idx
                    stack[-1] = (u, idx+1)
                    dfs_tree.append((u, v))
                    canvas.itemconfig(f"edge_{u}_{v}", fill="red", width=3)
                    root.update()
                    step(f"Colored edge {u+1}->{v+1}")
                    visited[v] = True
                    canvas.itemconfig(f"node_{v}", fill="lightblue")
                    root.update()
                    step(f"Discovered node {v+1}")
                    stack.append((v, 0))
                    step(f"  Entering dfs({v+1})")
                else:
                    stack.pop()
                    step(f"Backtracking from {u+1}")
    step("DFS complete")
    print("DFS tree edges:", [(u+1, v+1) for u, v in dfs_tree])
    return dfs_tree


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
draw_graph(new_directed_matrix, nodes, 1)
root.update()
input("Initial graph shown. Press Enter to continue...")
root.title('BFS')
bfs_edges = bfs_with_color(new_directed_matrix)
canvas.delete("all")
root.title('DFS')
draw_graph(new_directed_matrix, nodes, 1)
root.update()
dfs_edges = dfs_with_color(new_directed_matrix)
n = len(new_directed_matrix)
bfs_mat = edges_to_matrix(bfs_edges, n)
dfs_mat = edges_to_matrix(dfs_edges, n)

print("\nBFS‑tree adjacency matrix:")
print_matrix(bfs_mat)

print("\nDFS‑tree adjacency matrix:")
print_matrix(dfs_mat)

draw_graph(new_directed_matrix, n, True)
root.update()

input("Original graph displayed.  Press Enter to show BFS‑tree…")
canvas.delete("all")
draw_graph(new_directed_matrix, nodes, 1)
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

root.mainloop()