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

def dfs(graph, node):
    visited = set()
    stack = deque()

    visited.add(node)
    stack.append(node)

    while stack:
        s = stack.pop(node)

        for n in reversed(graph[s]):
            if n not in visited:
                visited.add(n)
                stack.append(n)

    return visited
