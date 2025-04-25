import numpy as np
import networkx as nx

class MapperBase:
    def __init__(self, clusterer):
        """Recibe un clusterer de scikit-learn"""
        self.clusterer = clusterer
        self.graph = nx.Graph()
        self.clusters_map = {}  

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
        self.graph.clear()
        self.clusters_map.clear()
        node_counter = 0

        for entry in cover:
            if len(entry) == 2:
                bounds, inds = entry
            else:
                raise ValueError("Cada elemento de la cubierta debe ser una tupla (bounds, indices)")

            if len(inds) == 0:
                continue
            subset = X[inds]
            new_nodes, node_counter = self._cluster_interval(subset, inds, node_counter)
            for nid, members in new_nodes:
                self.graph.add_node(nid, indices=members, bounds=bounds)
                self.clusters_map[nid] = set(members)

        for id1, set1 in self.clusters_map.items():
            for id2, set2 in self.clusters_map.items():
                if id1 < id2 and set1 & set2:
                    self.graph.add_edge(id1, id2)

        return self.graph