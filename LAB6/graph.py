import tkinter as tk
import random
import math


n1 = 4
n2 = 2
n3 = 2
n4 = 1
variant = 4221
random.seed(variant)
nodes = n3 + 10
# Fill matrix with 0
def create_zero_matrix(n):
    return [[0 for _ in range(n)] for _ in range(n)]
undirected_matrix = create_zero_matrix(nodes)
directed_matrix = create_zero_matrix(nodes)
new_directed_matrix = create_zero_matrix(nodes)
k = 1 - n3 * 0.01 - n4 * 0.005 - 0.05
def calc_matrix_el(k):
    return math.floor(random.random() * 2 * k)
# print('\nDirected matrix:\n')
for i in range(nodes):
    for j in range(nodes):
      directed_matrix[i][j] = calc_matrix_el(k)


# print('\nUndirected matrix:\n')
for i in range(nodes):
    for j in range(nodes):
      undirected_matrix[i][j] = directed_matrix[i][j] or directed_matrix[j][i]

# print('\nNew directed matrix:\n')
# for i in range(nodes):
#     for j in range(nodes):
#       new_directed_matrix[i][j] = calc_matrix_el(k)
root = tk.Tk()
root.title("Lab3 Graph")
canvas_width = 800
canvas_height = 800
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='white')
canvas.pack()

center_x = center_y = canvas_width / 2
R = 25 
circle_radius = 250 
angle = math.pi * 2 / nodes 

def get_node_x(i):
    return center_x + math.sin(i * angle) * circle_radius
def get_node_y(i):
    return center_y - math.cos(i * angle) * circle_radius

def draw_nodes(num_nodes):
    for i in range(num_nodes):
        x = get_node_x(i)
        y = get_node_y(i)
        canvas.create_oval(
            x-R, y-R, x+R, y+R,
            fill="white", outline="black",
            tags=(f"node_{i}","node")    
        )
        canvas.create_text(
            x, y, text=str(i+1),
            font=("Rubik", 15),
            tags=(f"node_label_{i}","node_text")  
        )

def draw_edges(matrix, num_nodes, is_directed):
    for i in range(num_nodes):
        for j in range(num_nodes):
            if matrix[i][j] == 1:
                if i == j:
                    draw_self_loop(i, is_directed)
                else:
                    draw_normal_edge(i, j, is_directed, tag=f"edge_{i}_{j}")

def draw_self_loop(i, is_directed):
    cx, cy = get_node_x(i), get_node_y(i) 
    loop_radius = R * 1.2 
    loop_angle_offset = math.pi / 2 
    current_node_angle = i * angle
    loop_center_x = cx + math.sin(current_node_angle) * (R + loop_radius * 0.6)
    loop_center_y = cy - math.cos(current_node_angle) * (R + loop_radius * 0.6)
    angle1 = current_node_angle - loop_angle_offset / 2
    angle2 = current_node_angle + loop_angle_offset / 2
    if is_directed:
         touch_offset = R * 0.9
         cp_dist = loop_radius * 2.3 
    else: 
         touch_offset = R * 0.15
         cp_dist = loop_radius * 2
    start_x = cx + math.sin(current_node_angle) * touch_offset
    start_y = cy - math.cos(current_node_angle) * touch_offset
    end_x = cx + math.sin(current_node_angle) * touch_offset
    end_y = cy - math.cos(current_node_angle) * touch_offset
    cp1x = loop_center_x + math.sin(angle1) * cp_dist
    cp1y = loop_center_y - math.cos(angle1) * cp_dist
    cp2x = loop_center_x + math.sin(angle2) * cp_dist
    cp2y = loop_center_y - math.cos(angle2) * cp_dist
    points = [start_x, start_y, cp1x, cp1y, cp2x, cp2y, end_x, end_y]

    if is_directed:
         canvas.create_line(*points, smooth=True, splinesteps=36, width=2, arrow=tk.LAST)
    else:
        canvas.create_line(*points, smooth=True, splinesteps=36, width=2)

def draw_normal_edge(i, j, is_directed, tag=None):
    x1, y1 = get_node_x(i), get_node_y(i)
    x2, y2 = get_node_x(j), get_node_y(j)
    dx, dy = x2 - x1, y2 - y1
    dist = math.hypot(dx, dy)
    if dist == 0:
        return
    ux, uy = dx/dist, dy/dist
    sx, sy = x1 + ux*R, y1 + uy*R
    ex, ey = x2 - ux*R, y2 - uy*R
    canvas.create_line(
        sx, sy, ex, ey,
        width=2,
        arrow=(tk.LAST if is_directed else None),
        tag=tag
    )

def draw_graph(matrix,nodes, is_directed):
    draw_edges(matrix, nodes, is_directed) 
    draw_nodes(nodes) 
    canvas.tag_raise("node")       
    canvas.tag_raise("node_text")  
