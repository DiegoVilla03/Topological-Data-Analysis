import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

class MapperPlot:
    @staticmethod
    def plot_graph(graph, figsize=(8,6), layout='kawaii'):
        pos = nx.spring_layout(graph) if layout=='kawaii' else nx.circular_layout(graph)
        plt.figure(figsize=figsize)
        nx.draw(graph, pos, with_labels=True, node_size=200)
        plt.title('Grafo Mapper')
        plt.show()

    @staticmethod
    def plot_lens_hist(lens_values, bins=30):
        plt.figure()
        plt.hist(lens_values, bins=bins)
        plt.title('Distribución de la función lente')
        plt.xlabel('Valor lente')
        plt.ylabel('Frecuencia')
        plt.show()

    @staticmethod
    def plot_data_clusters(X, clusters_map, figsize=(8,6), alpha=0.3, s=20):
        """
        Scatter de datos X coloreados por cluster.
        """
        plt.figure(figsize=figsize)
        X = np.asarray(X)
        cmap = plt.get_cmap('tab20')
        for i, (nid, inds_set) in enumerate(clusters_map.items()):
            inds = list(inds_set)
            if not inds:
                continue
            pts = X[inds]
            plt.scatter(pts[:,0], pts[:,1], color=cmap(i % 20), alpha=alpha, s=s, label=f'Node {nid}')
        plt.title('Clusters Mapper en el espacio')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')
        plt.show()