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

def max_component(graph: Graph) -> dict:
    visited = set()
    component = set()
    sol = {"mayor":0,"cant":0}

    for vertex in graph._graph:
        if vertex not in visited:
            component = dfs(graph, vertex)
            visited.update(component) 
            
            sol["mayor"] = max(sol["mayor"], len(component))

            sol["cant"] += 1
    
    return sol

#orden: O(n*(n+m)) | tiempo: (vertexs),n=875.713 (edges),m=5.105.039  O(875.713*(875.713 + 5.105.039)) |
def single_source_shortest(graph: Graph) -> dict: 
    distances = {}

    for vertex in graph._graph:
        distances[vertex] = bfs(graph, vertex)
        
    return distances 

def triangles(graph: Graph) -> int:
    cant = 0
    for a in graph._graph:
        neighbors_a = set(graph.get_neighbors(a))
        for b in graph.get_neighbors(a):
            neighbors_b = set(graph.get_neighbors(b))
            intersection = neighbors_a & neighbors_b

            for c in intersection:
                cant += 1 if a in graph.get_neighbors(c) else 0

    return cant // 3

