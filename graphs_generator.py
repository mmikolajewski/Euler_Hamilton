
import networkx as nx
import random
import os


def generate_euler_hamilton_graph(n, edge_density):
    # Tworzenie pustego grafu
    G = nx.Graph()

    # Dodawanie wierzchołków
    G.add_nodes_from(range(1, n + 1))

    # Obliczanie maksymalnej liczby krawędzi w grafie pełnym
    max_edges = n * (n - 1) // 2

    # Obliczanie liczby krawędzi do dodania w grafie na podstawie współczynnika nasycenia
    num_edges = int(edge_density * max_edges)

    # Dodawanie krawędzi
    added_edges = 1
    G.add_edge(n, 1)
    for v in range(2, n + 1):
        G.add_edge(v - 1, v)
        added_edges += 1
    while added_edges < num_edges:
        u = random.randint(1, n)
        v = random.randint(1, n)
        if u != v and not G.has_edge(u, v):
            G.add_edge(u, v)
            added_edges += 1
    # print(added_edges)
    v = 1
    while v < n:
        if G.degree(v) % 2 == 1:
            u = v + 1
            while u <= n:
                if G.degree(u) % 2 == 1 and not G.has_edge(u, v):
                    G.add_edge(u, v)
                    added_edges += 1
                u += 1
        v += 1
    # print(added_edges)
    for v in range(1, n + 1):
        if G.degree(v) % 2 == 1:
            for u in range(1, n + 1):
                if G.degree(u) % 2 == 1 and u != v:
                    G.remove_edge(v, u)
                    added_edges -= 1

    # Mieszanie wierzchołków
    mapping = dict(zip(G.nodes(), random.sample(list(G.nodes()), len(G.nodes()))))
    G = nx.relabel_nodes(G, mapping)

    return G


def save_graph_as_edge_list(G, filename, folder):
    # Sprawdzenie istnienia folderu, stworzenie jeśli nie istnieje
    if not os.path.exists(folder):
        os.makedirs(folder)

    path = os.path.join(folder, filename)
    with open(path, 'w') as file:
        for u, v in G.edges():
            file.write(f"{u} {v}\n")


def generate_and_save_graphs(start, stop, step, edge_densities):
    base_folder = 'graphs'
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)

    for n in range(start, stop + 1, step):
        for density in edge_densities:
            print(f"Generating graph for {n} nodes with density {density * 100}%.")
            graph = generate_euler_hamilton_graph(n, density)
            density_folder = os.path.join(base_folder, f'density_{int(density * 100)}')
            filename = f'graph_{n}_nodes.txt'
            save_graph_as_edge_list(graph, filename, density_folder)
            print(f"Graph with {n} nodes and density {int(density * 100)}% saved in '{density_folder}/{filename}'")



# Ustawienia
start_n = 10
stop_n = 150
step_n = 10
edge_densities = [0.3, 0.7]  # Dwie różne gęstości

# Wygeneruj i zapisz grafy
generate_and_save_graphs(start_n, stop_n, step_n, edge_densities)
