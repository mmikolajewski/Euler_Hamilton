import networkx as nx
import matplotlib.pyplot as plt
import random
import copy
from collections import deque
from time import time


def shuffle_nodes(G):
    nodes = list(G.nodes())
    random.shuffle(nodes)
    mapping = dict(zip(G.nodes(), nodes))
    return mapping


def generate_connected_graph(n, edge_density):
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
    # mapping = shuffle_nodes(G)
    G = nx.relabel_nodes(G, mapping)

    return G


def euler_cycle(graph):
    # Sprawdzanie, czy graf jest spójny
    n = len(graph)
    visited = [False] * n
    for i in range(n):
        if sum(graph[i]) > 0:
            start = i
            break
    stack = [start]
    path = []

    while stack:
        v = stack[-1]
        if sum(graph[v]) == 0:
            path.append(v)
            stack.pop()
        else:
            for u in range(n):
                if graph[v][u] == 1:
                    graph[v][u] = 0
                    graph[u][v] = 0
                    stack.append(u)
                    break

    # Sprawdzanie, czy wszystkie krawędzie zostały odwiedzone
    for i in range(n):
        for j in range(n):
            if graph[i][j] == 1:
                return False, []

    # Sprawdzanie, czy każdy wierzchołek został odwiedzony
    for v in range(n):
        if sum(graph[v]) > 0:
            return False, []

    return True, path[::-1]


def is_valid(v, graph, path, pos):
    # Sprawdzanie, czy wierzchołek v można dodać do ścieżki
    if graph[path[pos - 1]][v] == 0:
        return False

    # Sprawdzanie, czy v był już dodany do ścieżki
    if v in path:
        return False

    return True


def hamilton_cycle_util(graph, path, pos):
    n = len(graph)

    # Jeśli wszystkie wierzchołki zostały odwiedzone
    if pos == n:
        # Sprawdzanie, czy istnieje krawędź między ostatnim a pierwszym wierzchołkiem
        if graph[path[pos - 1]][path[0]] == 1:
            return True
        else:
            return False

    for v in range(1, n):
        if is_valid(v, graph, path, pos):
            path[pos] = v

            # Rekurencyjne sprawdzanie kolejnych wierzchołków
            if hamilton_cycle_util(graph, path, pos + 1) == True:
                return True

            # Jeśli dodanie v do ścieżki nie prowadzi do rozwiązania, usuwamy go
            path[pos] = -1

    return False


def hamilton_cycle(graph):
    n = len(graph)
    path = [-1] * n

    # Rozpoczynamy z pierwszym wierzchołkiem jako startowym
    path[0] = 0

    if hamilton_cycle_util(graph, path, 1) == False:
        return False, []

    return True, path


def hamilton_cycles(graph):
    n = len(graph)
    cycles = []

    def is_valid(v, path, pos):
        # Sprawdzanie, czy wierzchołek v można dodać do ścieżki
        if graph[path[pos - 1]][v] == 0:
            return False

        # Sprawdzanie, czy v był już dodany do ścieżki
        if v in path:
            return False

        return True

    def bfs_cycle(start):
        q = deque([(start, [start])])

        while q:
            (v, path) = q.popleft()

            # Jeśli ścieżka zawiera wszystkie wierzchołki
            if len(path) == n:
                # Sprawdzanie, czy istnieje krawędź między ostatnim a pierwszym wierzchołkiem
                if graph[path[-1]][path[0]] == 1:
                    cycles.append(path)
                continue

            for u in range(n):
                if is_valid(u, path, len(path)):
                    new_path = path + [u]
                    q.append((u, new_path))

    for i in range(n):
        bfs_cycle(i)

    return cycles


def avg(czasy):
    avg = []
    for i in range(0, len(czasy)):
        suma = 0
        for k in range(3):
            suma += czasy[i][k]
        avg.append(suma / 3)
    return avg


def avg2(czasy):
    suma = 0
    for k in range(3):
        suma += czasy[k]
    return (suma / 3)


# for number_of_elements in range(42, 85, 3):
#     print("~~~~~~~~~~~~~~~~~~~~~~~~~~~ Liczba elemtów to: ", number_of_elements, " ~~~~~~~~~~~~~~~~~~~~~~~~~~~")
#     czasy = [[], []]
#     # edge_density = [0.3, 0.7]
#     x = 0.7
#     # for x in edge_density:
#     for _ in range(3):
#         is_hamilton = False
#         while not is_hamilton:
#             g1 = generate_connected_graph(number_of_elements, 0.3)

#             graph = [[0]*number_of_elements for _ in range(number_of_elements)]
#             for i in g1.edges():
#                 graph[i[0]-1][i[1]-1] = 1
#                 graph[i[1]-1][i[0]-1] = 1

#             # Szukanie cyklu Hamiltona
#             graph2 = copy.deepcopy(graph)
#             t0 = time()
#             is_hamilton, cycle_h = hamilton_cycle(graph2)
#             czas_szukania_cyklu_h = time() - t0
#             print (czas_szukania_cyklu_h)
#             if is_hamilton:
#                 czasy[1].append(czas_szukania_cyklu_h)
#             print (is_hamilton)
#         for i in range(len(cycle_h)):
#             cycle_h[i] += 1
#         cycle_h.append(cycle_h[0])
#         # print (cycle_h)

#         # Szukanie cyklu Eulera
#         graph1 = copy.deepcopy(graph)
#         t1 = time()
#         is_euler, cycle_e = euler_cycle(graph1)
#         czas_szukania_cyklu_e = time() - t1
#         print (czas_szukania_cyklu_e)
#         czasy[0].append(czas_szukania_cyklu_e)
#         print (is_euler)
#         for i in range(len(cycle_e)):
#             cycle_e[i] += 1
#         # print (cycle_e)
#     avgtime = avg(czasy)
#     print (avgtime)
for number_of_elements in range(10, 26):
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~ Liczba elemtów to: ", number_of_elements, " ~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    czasy = []
    # edge_density = [0.3, 0.7]
    x = 0.5
    # for x in edge_density:
    for _ in range(3):
        is_hamilton = False
        while not is_hamilton:
            g1 = generate_connected_graph(number_of_elements, 0.3)

            graph = [[0] * number_of_elements for _ in range(number_of_elements)]
            for i in g1.edges():
                graph[i[0] - 1][i[1] - 1] = 1
                graph[i[1] - 1][i[0] - 1] = 1

            # Szukanie cyklu Hamiltona
            graph2 = copy.deepcopy(graph)
            is_hamilton, cycle_h = hamilton_cycle(graph2)
            print(is_hamilton)
        plt.subplot(1, 2, 1)
        nx.draw(g1, with_labels=True, pos=nx.circular_layout(g1))
        plt.show()
        t0 = time()
        cycles_h = hamilton_cycles(graph2)
        czas_szukania_cykli_h = time() - t0
        czasy.append(czas_szukania_cykli_h)
        print(czas_szukania_cykli_h)
    avgtime = avg2(czasy)
    print(avgtime)
# Wszystkie cykle Hamiltona
cycles_h = hamilton_cycles(graph2)
# for i in range(len(cycles_h)):
#     cycles_h[i].append(cycles_h[i][0])
#     for j in range(len(cycles_h[i])):
#         cycles_h[i][j] += 1
# print (cycles_h)


# Przykładowe użycie
# n = 10  # liczba wierzchołków
# edge_density = 0.3  # współczynnik nasycenia krawędziami
# g1 = generate_connected_graph(n, 0.3)
# # print(g1.degree(range(1, n+1)))
# # g2 = generate_connected_graph(n, 0.7)
# # print(g2.degree(range(1, n+1)))
# # print("Wierzchołki grafu:", g1.nodes())
# # print("Krawędzie grafu:", g2.edges())

# # Przepisywanie grafu na macierz
# graph = [[0]*n for _ in range(n)]
# for i in g1.edges():
#     graph[i[0]-1][i[1]-1] = 1
#     graph[i[1]-1][i[0]-1] = 1

# Rysowanie grafów
# plt.subplot(1, 2, 1)
# nx.draw(g1, with_labels=True, pos=nx.circular_layout(g1))
# plt.subplot(1, 2, 2)
# nx.draw(g2, with_labels=True, pos=nx.circular_layout(g2))
# plt.show()