from graph import Graph
from collections import deque
from collections import defaultdict
import random
from tqdm import tqdm
import time

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

def dfs_cycle(graph: Graph, start: str, visited: set, path: list, start_vertex: str, max_cycle: int, depth_limit: int) -> int:
    path.append(start)
    visited.add(start)
    
    if len(path) > max_cycle and start_vertex in graph.get_neighbors(start):
        max_cycle = len(path)
    
    if len(path) < depth_limit:
        for neighbor in graph.get_neighbors(start):
            if neighbor not in visited:
                max_cycle = dfs_cycle(graph, neighbor, visited, path, start_vertex, max_cycle, depth_limit)
    
    visited.remove(start)
    path.pop()
    
    return max_cycle


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

def min_todos_estimation(graph: Graph, sample_size: int) -> dict: 
    distances = {}
    random_v = set()

    while len(random_v) < sample_size:
        random_v.add(random.choice(list(graph._graph.keys())))

    start_time = time.time()
    for vertex in random_v:
        distances[vertex] = bfs(graph, vertex)

    end_time = time.time()
    total_time = end_time - start_time
    bfs_time = total_time/sample_size
    estimation_time = (bfs_time*875713)/86400 #en dias

    print(f"Tiempo total: {total_time:.2f} segundos")
    print(f"Tiempo promedio BFS: {bfs_time:.2f} segundos")
    print(f"Tiempo estimacion: {estimation_time:.2f} dias\n")
        
    return distances 

def triangles(graph: Graph) -> int:
    cant = 0
    visited_v = set()
    for a in graph._graph:
        visited_v.add(a)
        for b in graph.get_neighbors(a):
            if b not in visited_v:
                for c in graph.get_neighbors(b):
                    if c not in visited_v:
                        cant += 1 if a in graph.get_neighbors(c) else 0

    return cant

def diameter_from_estimation(distances: dict) -> int:
    diameter = 0
    visited_f = set()

    for dist in distances.values():
        farthest_v = max(dist, key=dist.get)

        if farthest_v not in visited_f:
            visited_f.add(farthest_v)
            bfs_2 = bfs(page_graph, farthest_v)
            diameter = max(diameter, max(bfs_2.values()), max(dist.values()))

    return diameter

def PageRank(graph: Graph, sample_size: int, step: int) -> dict:
    rank = defaultdict(int)
    random_v = set()

    while len(random_v) < sample_size:
        random_v.add(random.choice(list(graph._graph.keys())))

    for start in random_v:
        current = start

        for _ in range(step):
            rank[current] += 1
            neighbors = graph.get_neighbors(current)

            if not neighbors:
                break  

            current = random.choice(neighbors)
    
    return rank

def circumference(graph: Graph, ranked_vertices: list, depth_limit: int, sample_size: int) -> int:
    sampled = ranked_vertices[:sample_size]
    if len(sampled) < sample_size:
        pool = [v for v in graph._graph if v not in sampled]
        sampled += random.sample(pool, sample_size - len(sampled))
    
    return max(dfs_cycle(graph, v, set(), [], v, 0, depth_limit) for v in sampled)

def clustering_coefficient(graph: Graph) -> float:
    coefficients = []

    for vertex in graph._graph:
        neighbors = graph.get_neighbors(vertex)
        k = len(neighbors)
        if k < 2:
            coefficients.append(0)
            continue

        links = 0
        for i in range(k):
            for j in range(i+1, k):
                if graph.edge_exists(neighbors[i], neighbors[j]) or graph.edge_exists(neighbors[j], neighbors[i]):
                    links += 1

        coeff = (2*links)/(k*(k - 1))
        coefficients.append(coeff)

    if coefficients:
        return sum(coefficients)/len(coefficients)
    else:
        return 0

if __name__ == "__main__":
    print("Análisis de grafo web\n")

    # Punto 1: Componentes conexas
    componentes = max_component(undirected_graph)
    print(f"1) Componente conexa más grande: {componentes['mayor']} nodos")
    print(f"   Cantidad de componentes conexas: {componentes['cant']}\n")

    # Punto 2: Estimar tiempo de caminos mínimos
    print("2) Caminos mínimos entre todas las páginas:")
    distancias = min_todos_estimation(page_graph, 10)

    # Punto 3: Triángulos
    cantidad_triangulos = triangles(page_graph)
    print(f"3) Cantidad de triángulos en el grafo: {cantidad_triangulos}\n")

    # Punto 4: Estimacion diámetro
    diametro = diameter_from_estimation(distancias)
    print(f"4) Diámetro del grafo: {diametro}\n")

    # Punto 5: PageRank:
    resultados = PageRank(page_graph, sample_size=1000, step=200)
    rank_ordenado = sorted(resultados.items(), key=lambda x: x[1], reverse=True)
    print("5) PageRank:")
    for v, r in rank_ordenado[:10]:
        print(f"{v}: {r}")

    # Punto 6: Circunferencia
    sampled_vertices = [v for v, _ in rank_ordenado]
    circ = circumference(page_graph, sampled_vertices, 100, 200)
    print(f"\n6) Circunferencia del grafo: {circ}")

    # Adicionales 2: clustering
    #clustering = clustering_coefficient(undirected_graph)
    #print(f"\nPunto extra 2) Coeficiente de clustering global: {clustering:.4f}")

