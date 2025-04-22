import matplotlib.pyplot as plt
import networkx as nx

class MapperPlot:
    @staticmethod
    def plot_graph(graph, figsize=(8,6), layout='spring'):
        pos = nx.spring_layout(graph) if layout=='spring' else nx.circular_layout(graph)
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