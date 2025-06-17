from graph import Graph
from collections import deque

page_graph = Graph()

with open('web-Google.txt', 'r') as file:
    for l in file:
        if "# FromNodeId	ToNodeId" in l:
            break
    for l in file:
        if not l:
            break
        edge = tuple(int(v.replace("\n", "").replace("\t", "")) for v in l.split("\t"))
        for v in edge:
            if not page_graph.vertex_exists(v):
                page_graph.add_vertex(str(v))
        page_graph.add_edge(str(edge[0]), str(edge[1]))

undirected_graph = Graph()

for vertex in page_graph._graph:
    undirected_graph.add_vertex(vertex)

for vertex in page_graph._graph:
    for neighbor in page_graph.get_neighbors(vertex):
        if not undirected_graph.edge_exists(vertex, neighbor) and not undirected_graph.edge_exists(neighbor, vertex):
            undirected_graph.add_edge(vertex, neighbor)
            undirected_graph.add_edge(neighbor, vertex)

def dfs(graph: Graph, vertex: str) -> set:
    visited = set()
    stack = deque()

    visited.add(vertex)
    stack.append(vertex)

    while stack:
        s = stack.pop()

        for n in reversed(graph.get_neighbors(s)):
            if n not in visited:    
                visited.add(n)
                stack.append(n)

    return visited

def bfs(graph: Graph, vertex: str) -> dict:
    distances = {}
    queue = deque()

    distances[vertex] = 0
    queue.append(vertex)

    while queue:
        s = queue.popleft()

        for n in graph.get_neighbors(s):
            if n not in distances:    
                distances[n] = distances[s] + 1 #por cada vecino que encontramos, le asignamos la distancia del nodo actual + 1
                queue.append(n)

    return distances

def max_component(undirected_graph: Graph) -> dict:
    visited = set()
    component = set()
    sol = {"mayor":0,"cant":0}

    for vertex in undirected_graph._graph:
        if vertex not in visited:
            component = dfs(undirected_graph, vertex)
            visited.update(component) 
            
            sol["mayor"] = max(sol["mayor"], len(component))

            sol["cant"] += 1
    
    return sol

#orden: O(n*(n+m)) | tiempo: (vertexs),n=875.713 (edges),m=5.105.039  O(875.713*(875.713 + 5.105.039)) |
def min_todos(graph: Graph) -> dict: 
    distances = {}

    for vertex in graph._graph:
        distances[vertex] = bfs(graph, vertex)
        
    return distances 

def triangles(undirected_graph: Graph) -> int:
    cant = 0
    for a in undirected_graph._graph:
        neighbors_a = set(undirected_graph.get_neighbors(a))
        for b in neighbors_a:
            if b > a:
                neighbors_b = set(undirected_graph.get_neighbors(b))
                intersection = neighbors_a & neighbors_b

            for c in intersection:
                cant += 1 if c > b else 0

    return cant

def graph_diameter(undirected_graph: Graph) -> int: #mejorar con 2 bfs
    visited = set()
    diameter = 0

    for vertex in undirected_graph._graph:
        if vertex not in visited:
            bfs_1 = bfs(undirected_graph, vertex)
            visited.update(bfs_1.keys())
            farthest_v = max(bfs_1, key=bfs_1.get)

            bfs_2 = bfs(undirected_graph, farthest_v)
            diameter = max(diameter, max(bfs_2.values()))


    return diameter

