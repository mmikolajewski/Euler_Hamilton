# Przykład testu funkcji wczytującej
import networkx as nx

import data_samples


base_directory = 'graphs'
process_and_measure(base_directory)

def process_and_measure(base_directory):
    density_30_directory = os.path.join(base_directory, 'density_30')
    density_70_directory = os.path.join(base_directory, 'density_70')

    results_30 = process_graph_files(density_30_directory, '30')
    results_70 = process_graph_files(density_70_directory, '70')

    results = results_30 + results_70
    save_results_to_csv(results, 'results_graph_operations.csv')

    for result in results:
        print(result)
