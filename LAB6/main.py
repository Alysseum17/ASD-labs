from graph import *
from help import *

def get_weights(matrix):
    n = len(matrix)
    B = [[0 for _ in range(n)] for _ in range(n)]
    C = [[0 for _ in range(n)] for _ in range(n)]
    D = [[0 for _ in range(n)] for _ in range(n)]
    H = [[0 for _ in range(n)] for _ in range(n)]
    Tr = [[0 for _ in range(n)] for _ in range(n)]
    W = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            B[i][j] = random.random() * 2

    for i in range(n):
        for j in range(n):
            C[i][j] = math.ceil(B[i][j] * 100 * matrix[i][j])

    for i in range(n):
        for j in range(n):
            if(C[i][j] > 0):
                D[i][j] = 1
            else:
                D[i][j] = 0
    for i in range(n):
        for j in range(n):
            if(D[i][j] != D[j][i]):
                H[i][j] = 1
            else:
                H[i][j] = 0
    for i in range(n):
        for j in range(n):
            if(i < j):
                Tr[i][j] = 1
            else:
                Tr[i][j] = 0
    for i in range(n):
        for j in range(n):
            weight = (D[i][j] + H[i][j] * Tr[i][j]) * C[i][j]
            if(i == j): 
                W[i][j] = W[j][i] = 0
            elif(weight == 0):
                W[i][j] = W[j][i] = math.inf
            else:
                W[i][j] = W[j][i] = weight
           
    return W
def print_matrix_formatted(matrix):
    size = len(matrix)
    for row in matrix:
        row_string = ""
        for element in row:
            if element == float('inf'):
                row_string += f"{'inf':<5}"
            else:
                row_string += f"{element:<5}"
        print(row_string)

CENTRE_CLEAR = 60      # радіус “натовпу” в центрі
SHIFT         = 30     # базовий зсув уздовж ребра
STEP_COLLIDE  = 10     # додатковий крок при конфліктах


def draw_weighted_graph(adj, Wmat):
    canvas.delete("all")
    draw_nodes(nodes)
    taken = []
    def collide(b):
        return any(not(b[2]<t[0] or b[0]>t[2] or b[3]<t[1] or b[1]>t[3]) for t in taken)


    for i in range(nodes):
        for j in range(i+1, nodes):
            if not adj[i][j]: continue
            x1,y1=get_node_x(i), get_node_y(i)
            x2,y2=get_node_x(j), get_node_y(j)
            tag_e   = f"edge_{i}_{j}"         
            tag_bg  = f"wbg_{i}_{j}"          
            tag_tx  = f"wtxt_{i}_{j}"        
            canvas.create_line(x1,y1,x2,y2,width=2,tags=(tag_e,))
            if Wmat[i][j] in (math.inf,0): continue
            dx,dy=x2-x1,y2-y1; L=math.hypot(dx,dy) or 1
            ux,uy=dx/L,dy/L
            mx,my=(x1+x2)/2,(y1+y2)/2
            if math.hypot(mx-center_x,my-center_y)<CENTRE_CLEAR:
                d1=math.hypot(x1-center_x,y1-center_y)
                d2=math.hypot(x2-center_x,y2-center_y)
                mx+=(-1 if d1>d2 else 1)*ux*SHIFT
                my+=(-1 if d1>d2 else 1)*uy*SHIFT
            txt=str(Wmat[i][j]); ww,hh=7*len(txt),12
            while True:
                box=(mx-ww/2-3,my-hh/2-3,mx+ww/2+3,my+hh/2+3)
                if collide(box): mx+=ux*STEP_COLLIDE; my+=uy*STEP_COLLIDE
                else: taken.append(box); break
            rect = canvas.create_rectangle(*box, fill="white", outline="",tags=("label", tag_bg))
            txt_id  = canvas.create_text(mx, my, text=txt,font=("Arial", 10), tags=("label", tag_tx))
    canvas.tag_raise("label")
  
    loop_r=R*1.4
    for i in range(nodes):
        if not adj[i][i]: continue
        draw_self_loop(i,0)
        if Wmat[i][i] in (math.inf,0): continue
        cx,cy=get_node_x(i), get_node_y(i)
        tx,ty=cx,cy-loop_r-8
        tag_bg  = f"wbg_{i}_{j}"           
        tag_tx  = f"wtxt_{i}_{j}"          
        txt=str(Wmat[i][i]); ww,hh=7*len(txt),12
        box=(tx-ww/2-3,ty-hh/2-3,tx+ww/2+3,ty+hh/2+3)
        rect=canvas.create_rectangle(*box,fill="white",outline="",tags=("label",tag_bg))
        txt_id=canvas.create_text(tx,ty,text=txt,font=("Arial",10),tags=("label",tag_tx))
        canvas.tag_raise(txt_id, rect)
    canvas.tag_raise(txt_id, rect)
    canvas.tag_raise("node")
    canvas.tag_raise("node_text")

def prim_stepwise(adj, Wmat):
    visited   = [False]*nodes
    parent    = [-1]*nodes        
    min_cost  = [math.inf]*nodes   
    start     = next(i for i in range(nodes) if any(adj[i]))
    min_cost[start] = 0

    print("=== Prim step by step ===")

    mst = []
    for _ in range(nodes):
        v = min(
            (i for i in range(nodes) if not visited[i]),
            key=lambda i: min_cost[i],
            default=None
        )
        if v is None or min_cost[v] is math.inf: break   
        visited[v] = True
        if parent[v] != -1:
            u = parent[v]
            w = Wmat[u][v]
            mst.append((u, v))

            input(f"({u+1}-{v+1}, w={w})  Enter → ")
            tag_e  = f"edge_{min(u,v)}_{max(u,v)}"
            tag_tx = f"wtxt_{min(u,v)}_{max(u,v)}"
            canvas.itemconfig(tag_e,  fill="red", width=3)
            canvas.itemconfig(f"node_{u}", fill="pale green")
            canvas.itemconfig(f"node_{v}", fill="pale green")
            canvas.itemconfig(tag_tx, fill="red")
            root.update()
            print(f"  added ({u+1},{v+1})")

        for x in range(nodes):
            if (not visited[x] and adj[v][x] and
                Wmat[v][x] not in (math.inf, 0) and
                Wmat[v][x] < min_cost[x]):
                min_cost[x] = Wmat[v][x]
                parent[x]   = v

    return mst


def edges_to_matrix(edges):
    M=[[0]*nodes for _ in range(nodes)]
    for u,v in edges: M[u][v]=M[v][u]=1
    return M

def show_tree(tree):
    canvas.delete("all")
    draw_nodes(nodes)                  
    for u, v in tree:
        x1, y1 = get_node_x(u), get_node_y(u)
        x2, y2 = get_node_x(v), get_node_y(v)
        canvas.create_line(x1, y1, x2, y2,
                           width=3, fill="red",
                           tags=("mst_edge",))

        mx, my = (x1+x2)/2, (y1+y2)/2
        txt = str(W[u][v])
        bg = canvas.create_rectangle(mx-15, my-9, mx+15, my+9,
                                     fill="white", outline="")
        fg = canvas.create_text(mx, my, text=txt,
                                 font=("Arial", 10, "bold"))
        canvas.tag_raise(fg, bg)
    
    canvas.tag_raise("node")         
    canvas.tag_raise("node_text")    
    total_w = sum(W[u][v] for u, v in tree)
    canvas.create_text(10, 10, anchor="nw",
                       text=f"Σ = {total_w}",
                       font=("Arial", 14, "bold"))
    root.update()
    input("MST is shown.  Enter → ")

print("Undirected matrix:")
print_matrix(undirected_matrix)
W = get_weights(undirected_matrix)
print_matrix_formatted(W)
# draw_graph(undirected_matrix,nodes,0)
draw_weighted_graph(undirected_matrix,W)
root.update()

mst_edges = prim_stepwise(undirected_matrix, W)
print("MST edges (1‑based):", [(u+1, v+1) for u, v in mst_edges])
input("Press Enter to continue…")
total_w = sum(W[u][v] for u, v in mst_edges)
print(f"Sum of the weights of the MST: {total_w}")
show_tree(mst_edges)
canvas.create_text(10, 10, anchor="nw",
                   text=f"Σ = {total_w}",
                   font=("Arial", 14, "bold"),
                   tags=("mst_sum",))
canvas.tag_raise("mst_sum")

root.mainloop()
