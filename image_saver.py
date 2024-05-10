import os
import data_samples
import matplotlib.pyplot as plt
import networkx as nx

def draw_and_save_graphs(g1, g2, image_path, title1, title2):
    print("Starting to draw graphs...")
    plt.figure(figsize=(16, 8))  # Ustawienie wielkości całego obrazu
    plt.subplot(1, 2, 1)
    nx.draw(g1, with_labels=True, pos=nx.circular_layout(g1), node_color='lightblue', edge_color='gray')
    plt.title(title1)
    plt.subplot(1, 2, 2)
    nx.draw(g2, with_labels=True, pos=nx.circular_layout(g2), node_color='lightgreen', edge_color='gray')
    plt.title(title2)
    plt.savefig(image_path)
    plt.close()
    print(f"Saved image at {image_path}")

def generate_images_from_files(base_folder='graphs'):
    density_folders = ['density_30', 'density_70']
    for i in range(len(density_folders) - 1):
        folder1 = os.path.join(base_folder, density_folders[i])
        folder2 = os.path.join(base_folder, density_folders[i + 1])
        image_folder = 'images'

        if not os.path.exists(image_folder):
            os.makedirs(image_folder)
            print(f"Created folder: {image_folder}")

        files1 = os.listdir(folder1)
        files2 = os.listdir(folder2)
        print(f"Processing {len(files1)} files from {folder1} and {len(files2)} files from {folder2}")

        for filename1, filename2 in zip(files1, files2):
            if filename1.endswith('.txt') and filename2.endswith('.txt'):
                file_path1 = os.path.join(folder1, filename1)
                file_path2 = os.path.join(folder2, filename2)
                g1 = reader.read_graph_from_file(file_path1)
                g2 = reader.read_graph_from_file(file_path2)
                image_path = os.path.join(image_folder, filename1.replace('.txt', '_comparison.png'))
                title1 = f"Graph with {density_folders[i].split('_')[1]}% edge density"
                title2 = f"Graph with {density_folders[i + 1].split('_')[1]}% edge density"
                draw_and_save_graphs(g1, g2, image_path, title1, title2)

# Wywołanie funkcji
generate_images_from_files()
