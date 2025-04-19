from graph import *
from help import *
import heapq

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
    canvas.tag_raise(txt_id, rect)
  
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

def prim_stepwise(adj, Wmat):
    visited=[False]*nodes
    start  = next(i for i in range(nodes) if any(adj[i]))
    visited[start]=True
    pq=[(Wmat[start][v],start,v) for v in range(nodes)
        if adj[start][v] and Wmat[start][v] not in (math.inf,0)]
    heapq.heapify(pq)
    mst=[]
    print("=== Prim step by step ===")
    while pq:
        w,u,v = heapq.heappop(pq)
        input(f"({u+1}-{v+1}, w={w})  Enter → ")
        if visited[v]:
            print("  skip (visited)")
            continue

        tag_e=f"edge_{min(u,v)}_{max(u,v)}"
        tag_tx = f"wtxt_{min(u,v)}_{max(u,v)}"
        canvas.itemconfig(tag_e,  fill="red",       width=3)        
        canvas.itemconfig(f"node_{u}", fill="pale green")          
        canvas.itemconfig(f"node_{v}", fill="pale green")
        canvas.itemconfig(tag_tx,fill="red")                      
        root.update()

        visited[v]=True
        mst.append((u,v))
        print(f"  added ({u+1},{v+1})")

        for x in range(nodes):
            if not visited[x] and adj[v][x] and Wmat[v][x] not in (math.inf,0):
                heapq.heappush(pq,(Wmat[v][x],v,x))
    return mst


def edges_to_matrix(edges):
    M=[[0]*nodes for _ in range(nodes)]
    for u,v in edges: M[u][v]=M[v][u]=1
    return M

def show_tree(tree):
    canvas.delete("all")
    draw_nodes(nodes)
    draw_edges(edges_to_matrix(tree),nodes,False)
    root.update()
    input("MST shown.  Enter → ")

W = get_weights(undirected_matrix)
print_matrix_formatted(W)
# draw_graph(undirected_matrix,nodes,0)
draw_weighted_graph(undirected_matrix,W)
root.update()

mst_edges = prim_stepwise(undirected_matrix, W)
print("MST edges (1‑based):", [(u+1, v+1) for u, v in mst_edges])

show_tree(mst_edges)


root.mainloop()
