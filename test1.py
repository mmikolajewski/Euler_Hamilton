import networkx as nx
import timeit
import statistics
import os
import service  # Załóżmy, że zawiera funkcję zapisu wyników
from data_samples import read_graph_from_file  # Załóżmy, że przeniosłeś tu wcześniejszą funkcję do wczytywania grafów

def measure_graph_operations(graph, operation):
    start_time = timeit.default_timer()
    result = operation(graph)
    end_time = timeit.default_timer()
    return end_time - start_time, result

def process_graph_files(directory, density):
    results = []
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            filepath = os.path.join(directory, filename)
            graph = read_graph_from_file(filepath)
            euler_time, has_euler_cycle = measure_graph_operations(graph, find_eulerian_cycle)
            hamilton_time, has_hamilton_cycle = measure_graph_operations(graph, find_hamiltonian_cycle)
            results.append({
                'file_name': filename,
                'density': density,
                'euler_cycle_time': euler_time,
                'hamilton_cycle_time': hamilton_time
            })
    return results


def find_eulerian_cycle(graph):
    # Sprawdzanie, czy graf jest spójny
    nodes = list(graph.nodes())
    if not nodes:
        return False, []

    start = nodes[0]  # Rozpocznij od pierwszego wierzchołka w grafie
    stack = [start]
    path = []

    while stack:
        v = stack[-1]
        neighbors = list(graph[v])
        if neighbors:
            u = neighbors[0]
            graph.remove_edge(v, u)  # Usuń krawędź, aby uniknąć ponownego odwiedzenia
            stack.append(u)
        else:
            path.append(stack.pop())

    # Sprawdzanie, czy wszystkie krawędzie zostały odwiedzone
    if any(graph.edges()):
        return False, []

    return True, path


def is_valid(v, graph, path, pos):
    if graph.has_edge(path[pos - 1], v) is False:
        return False
    if v in path:
        return False
    return True

def hamilton_cycle_util(graph, path, pos):
    n = graph.number_of_nodes()

    # Jeśli wszystkie wierzchołki zostały odwiedzone i istnieje krawędź z ostatniego do pierwszego
    if pos == n:
        if graph.has_edge(path[pos - 1], path[0]):
            return True
        else:
            return False

    for v in graph.nodes():
        if is_valid(v, graph, path, pos):
            path[pos] = v
            if hamilton_cycle_util(graph, path, pos + 1):
                return True
            path[pos] = -1  # Backtracking

    return False

def find_hamiltonian_cycle(graph):
    nodes = list(graph.nodes())
    path = [-1] * len(nodes)
    path[0] = nodes[0]  # start from the first node in the list

    if not hamilton_cycle_util(graph, path, 1):
        return False, []

    return True, path


def sort_by_node_count(result):
    # Wyciągamy liczbę węzłów z nazwy pliku, zakładając format 'graph_X_nodes.txt'
    node_count = int(result['file_name'].split('_')[1])
    return node_count

def process_and_measure(base_directory):
    density_30_directory = os.path.join(base_directory, 'density_30')
    density_70_directory = os.path.join(base_directory, 'density_70')

    results_30 = process_graph_files(density_30_directory, '30')
    results_70 = process_graph_files(density_70_directory, '70')

    # Sortowanie wyników przed zapisem
    results_30.sort(key=sort_by_node_count)
    results_70.sort(key=sort_by_node_count)

    # Zapis do dwóch różnych plików
    service.save_results_to_csv(results_30, 'results_graph_operations_density_30.csv')
    service.save_results_to_csv(results_70, 'results_graph_operations_density_70.csv')

    for result in results_30:
        print(result)
    for result in results_70:
        print(result)



base_directory = 'graphs'
process_and_measure(base_directory)