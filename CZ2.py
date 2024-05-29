import networkx as nx
import random
import os
import matplotlib.pyplot as plt
import timeit
import statistics

# Parametry, które można łatwo modyfikować
n_start = 3
n_stop = 15
n_step = 1
graph_density = 0.5  # Nasycenie grafu, 0.5 oznacza 50%
ti_repeat = 1
ti_number = 1
find_all_cycles = True  # False dla szukania pierwszego cyklu, True dla szukania wszystkich cykli

class Graph():
    def __init__(self, vertices):
        self.adjacency_matrix = [[0 for column in range(vertices)]
                                 for row in range(vertices)]
        self.vertices_count = vertices
        self.all_cycles = []

    def is_safe_to_add(self, v, pos, path):
        if self.adjacency_matrix[path[pos-1]][v] == 0:
            return False

        for vertex in path:
            if vertex == v:
                return False

        return True

    def hamiltonian_cycle_util(self, path, pos):
        if pos == self.vertices_count:
            if self.adjacency_matrix[path[pos-1]][path[0]] == 1:
                self.all_cycles.append(path[:])
                if not find_all_cycles:
                    return True
                return False
            else:
                return False

        for v in range(1, self.vertices_count):
            if self.is_safe_to_add(v, pos, path):
                path[pos] = v

                if self.hamiltonian_cycle_util(path, pos+1):
                    return True

                path[pos] = -1

        return False

    def find_hamiltonian_cycle(self):
        self.all_cycles.clear()
        path = [-1] * self.vertices_count
        path[0] = 0

        if not self.hamiltonian_cycle_util(path, 1):
            if find_all_cycles and self.all_cycles:
                return self.all_cycles
            return None

        return self.all_cycles if find_all_cycles else path

def ensure_even_degrees(G):
    odd_degree_nodes = [node for node in G.nodes() if G.degree(node) % 2 != 0]
    while odd_degree_nodes:
        u = odd_degree_nodes.pop()
        if odd_degree_nodes:
            v = odd_degree_nodes.pop()
            G.add_edge(u, v)
        else:
            v = random.choice([node for node in G.nodes() if node != u])
            G.add_edge(u, v)

def create_eulerian_graph(n, density):
    G = nx.Graph()
    G.add_nodes_from(range(1, n + 1))
    possible_edges = [(i, j) for i in range(1, n + 1) for j in range(i + 1, n + 1)]
    random.shuffle(possible_edges)
    num_edges = int(density * (n * (n - 1) / 2))
    G.add_edges_from(possible_edges[:num_edges])
    ensure_even_degrees(G)
    return G

def save_graph_as_edge_list(G, file_name, folder):
    list_folder = os.path.join(folder, "lists")
    if not os.path.exists(list_folder):
        os.makedirs(list_folder)
    path = os.path.join(list_folder, file_name)
    with open(path, 'w', encoding='utf-8') as file:
        for u, v in sorted(G.edges()):
            file.write(f"{u} {v}\n")

def draw_graph(G, file_name, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    plt.figure(figsize=(8, 8))
    nx.draw(G, with_labels=True, pos=nx.circular_layout(G), node_color='lightblue', edge_color='gray')
    image_path = os.path.join(folder, file_name)
    plt.savefig(image_path)
    plt.close()
    print(f"Graph image saved in {image_path}")

def generate_base_file_name(folder, base_name):
    i = 1
    base_path = os.path.join(folder, f"{base_name}.txt")
    while os.path.exists(base_path):
        base_path = os.path.join(folder, f"{base_name}_{i}.txt")
        i += 1
    return base_path

base_folder = 'grafy_eulera'
image_folder = os.path.join(base_folder, 'obrazy')
results_folder = os.path.join(base_folder, 'wyniki')

if not os.path.exists(base_folder):
    os.makedirs(base_folder)
if not os.path.exists(image_folder):
    os.makedirs(image_folder)
if not os.path.exists(results_folder):
    os.makedirs(results_folder)

results_file = generate_base_file_name(results_folder, "wyniki_czasow")

# Tworzenie nagłówka w pliku wyników
with open(results_file, 'w', encoding='utf-8') as file:
    file.write("Number of vertices\tMin time\tMax time\tAverage time\n")

for n in range(n_start, n_stop + 1, n_step):
    G = create_eulerian_graph(n, graph_density)
    file_name = f"graf_eulerowski_{n}_wierzcholkow.txt"
    save_graph_as_edge_list(G, file_name, base_folder)
    draw_graph(G, f"graf_eulerowski_{n}_wierzcholkow.png", image_folder)

    # Convert the NetworkX graph to our Graph class
    hc_graph = Graph(n)
    for u, v in G.edges():
        hc_graph.adjacency_matrix[u-1][v-1] = 1
        hc_graph.adjacency_matrix[v-1][u-1] = 1

    setup_code = f'''
from __main__ import Graph, find_all_cycles
hc_graph = Graph({n})
hc_graph.adjacency_matrix = {hc_graph.adjacency_matrix}
hc_graph.find_hamiltonian_cycle()
'''
    stmt = "hc_graph.find_hamiltonian_cycle()"
    timer = timeit.Timer(stmt, setup=setup_code)

    results_times = []
    for _ in range(ti_repeat):
        t = timer.timeit(number=ti_number)
        results_times.append(t)

    result_stats = {
        'sample_size': n,
        'min': min(results_times),
        'max': max(results_times),
        'avg': statistics.mean(results_times)
    }

    with open(results_file, 'a', encoding='utf-8') as file:
        file.write(f"{n}\t{result_stats['min']}\t{result_stats['max']}\t{result_stats['avg']}\n")

    print(f"Execution times for {n} vertices: {result_stats}")

    # Drukowanie cykli Hamiltona
    hamiltonian_cycles = hc_graph.find_hamiltonian_cycle()
    if hamiltonian_cycles:
        if find_all_cycles:
            print(f"Found {len(hamiltonian_cycles)} Hamiltonian cycles for {n} vertices.")
        else:
            print(f"Found a Hamiltonian cycle for {n} vertices: {hamiltonian_cycles}")
    else:
        print(f"No Hamiltonian cycles found for {n} vertices.")
