from graph import Graph
from collections import deque
import random
from tqdm import tqdm
import time
from multiprocessing import Pool, cpu_count


page_graph = Graph()

with open('C:/Users/alvar/Documents/UDESA/tercer/algoritmos/Tp4/web-Google.txt', 'r') as file:
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


def min_todos_estimation(graph: Graph, sample_size: int = 1000) -> dict: 
    distances = {}
    random_v = set()

    while len(random_v) < sample_size:
        random_v.add(random.choice(list(graph._graph.keys())))

    start_time = time.time()
    for vertex in tqdm(random_v, desc="Calculando caminos mínimos"):
        distances[vertex] = bfs(graph, vertex)

    end_time = time.time()
    total_time = end_time - start_time

    print(f"\n⏱ Tiempo total: {total_time:.2f} segundos")
        
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

def triangles_directed(graph: Graph) -> int:
    cant = 0
    for a in graph._graph:
        neighbors_a = set(graph.get_neighbors(a))
        for b in graph.get_neighbors(a):
            neighbors_b = set(graph.get_neighbors(b))
            intersection = neighbors_a & neighbors_b

            for c in intersection:
                cant += 1 if a in graph.get_neighbors(c) else 0

    return cant // 3

def diameter_from_estimation(distances: dict) -> int:
    diameter = 0
    for dist in distances.values():
        diameter = max(diameter, max(dist.values()))

    return diameter

if __name__ == "__main__":
    print("Análisis de grafo web\n")

    # Punto 1: Componentes conexas
    #componentes = max_component(undirected_graph)
    #print(f"1) Componente conexa más grande: {componentes['mayor']} nodos")
    #print(f"   Cantidad de componentes conexas: {componentes['cant']}")

    # Punto 2: Estimar tiempo de caminos mínimos (comentado para evitar ejecuciones largas)
    print("2) Caminos mínimos entre todas las páginas:\n")
    distancias = min_todos_estimation(page_graph, 1000)

    # Punto 3: Triángulos
    cantidad_triangulos = triangles(undirected_graph)
    print(f"3) Cantidad de triángulos en el grafo: {cantidad_triangulos}")

    # Punto 4: Diámetro
    diametro = diameter_from_estimation(distancias)
    print(f"4) Diámetro del grafo: {diametro}")

    # Punto 5 y 6 no implementados en el código actual
    #print("5) PageRank: no implementado aún")
    #print("6) Circunferencia del grafo: no implementado aún")
