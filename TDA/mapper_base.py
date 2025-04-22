import numpy as np
import networkx as nx

class MapperBase:
    def __init__(self, clusterer):
        """Recibe un clusterer de scikit-learn"""
        self.clusterer = clusterer
        self.graph = nx.Graph()

    def _cluster_interval(self, X_subset, indices, start_node_id):
        labels = self.clusterer.fit_predict(X_subset)
        nodes = []
        node_id = start_node_id
        for lbl in np.unique(labels):
            if lbl == -1:
                continue
            members = indices[labels == lbl]
            nodes.append((node_id, members))
            node_id += 1
        return nodes, node_id

    def build_graph(self, X, cover):
        """
        Construye el grafo Mapper a partir de los datos X y la cubierta.

        Parámetros:
            X: array-like, datos originales
            cover: lista de tuplas (start, end, indices)
        """
        self.graph.clear()
        clusters_map = {}
        node_counter = 0

        for start, end, inds in cover:
            if len(inds) == 0:
                continue
            subset = X[inds]
            new_nodes, node_counter = self._cluster_interval(subset, inds, node_counter)
            for nid, members in new_nodes:
                self.graph.add_node(nid, indices=members)
                clusters_map[nid] = set(members)

        for id1, set1 in clusters_map.items():
            for id2, set2 in clusters_map.items():
                if id1 < id2 and set1 & set2:
                    self.graph.add_edge(id1, id2)

        return self.graph