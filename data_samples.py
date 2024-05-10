import networkx as nx


def read_graph_from_file(file_path):
    G = nx.Graph()
    with open(file_path, 'r') as file:
        for line in file:
            u, v = map(int, line.strip().split())
            G.add_edge(u, v)
    return G


