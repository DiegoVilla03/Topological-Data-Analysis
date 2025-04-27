import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


class MapperPlot:
    @staticmethod
    def _get_layout(graph, layout):
        if layout == 'spring':
            return nx.spring_layout(graph)
        if layout == 'circular':
            return nx.circular_layout(graph)
        if layout == 'kamada_kawai':
            return nx.kamada_kawai_layout(graph)
        raise ValueError(f"Layout desconocido: {layout}")

    @staticmethod
    def plot_graph(graph, color_data=None, figsize=(8,6), layout='spring'):
        fig, ax = plt.subplots(figsize=figsize)
        pos = MapperPlot._get_layout(graph, layout)
        if color_data is not None:
            node_vals = [np.mean(color_data[graph.nodes[n]['indices']]) for n in graph.nodes]
            cmap = plt.cm.viridis
            vmin, vmax = min(node_vals), max(node_vals)
            nodes = nx.draw_networkx_nodes(graph, pos, node_color=node_vals,
                                           cmap=cmap, vmin=vmin, vmax=vmax,
                                           node_size=200, ax=ax)
            nx.draw_networkx_edges(graph, pos, ax=ax)
            nx.draw_networkx_labels(graph, pos, ax=ax)
            fig.colorbar(nodes, ax=ax, label='Valor de variable filtro')
        else:
            nx.draw(graph, pos, with_labels=True, node_size=200, ax=ax)
        ax.set_title(f'Grafo Mapper ({layout})')
        plt.show()

    @staticmethod
    def plot_hist(lens_values, bins=30):
        fig, ax = plt.subplots()
        ax.hist(lens_values, bins=bins)
        ax.set(title='Histograma Lens', xlabel='Valor lente', ylabel='Frecuencia')
        plt.show()

    @staticmethod
    def plot_data(X, clusters_map, figsize=(8,6), alpha=0.3, s=20):
        fig, ax = plt.subplots(figsize=figsize)
        X = np.asarray(X)
        cmap = plt.cm.tab20
        for i,(nid, inds) in enumerate(clusters_map.items()):
            pts = X[list(inds)]
            ax.scatter(pts[:,0], pts[:,1], s=s, alpha=alpha, c=[cmap(i%20)], label=f'Node {nid}')
        ax.set_title('Clusters en espacio de datos')
        ax.legend(bbox_to_anchor=(1.05,1), loc='upper left', fontsize='small')
        plt.show()