import numpy as np
import networkx as nx
from .cover import CoverGenerator
from .mapper_base import MapperBase
from .plot import MapperPlot
from .nerve import NerveBuilder
from .homology import HomologyAnalyzer

class Mapper:
    def __init__(self, lens_func=None, n_intervals=10, overlap=0.1,
                 clusterer=None, nerve_order=2, homology_dim=1):
        self.lens_func = lens_func
        self.cover_generator = CoverGenerator(n_intervals, overlap)
        self.base = MapperBase(clusterer)
        self.plotter = MapperPlot
        self.nerve_builder = NerveBuilder
        self.homology = HomologyAnalyzer(maxdim=homology_dim)
        self.nerve_order = nerve_order
        self.data = None
        self.lens_values = None
        self.cover = None
        self.graph = None
        self.nerve = None
        self.diagrams = None
        self.betti = None
        self.clusters_map = None

    def fit(self, X):
        X = np.asarray(X)
        self.data = X
        self.lens_values = self.lens_func(X) if self.lens_func else X.mean(axis=1)
        self.cover = self.cover_generator.compute_cover(self.lens_values)
        self.graph = self.base.build_graph(X, self.cover)
        self.clusters_map = self.base.clusters_map.copy()
        raw_idx = nx.get_node_attributes(self.graph, 'indices')
        clusters_idx = {nid: set(vals) for nid, vals in raw_idx.items()}
        self.nerve = self.nerve_builder.compute_nerve(clusters_idx, max_order=self.nerve_order)
        return self

    def analyze_homology(self, X=None):
        if X is None:
            X = self.data
        self.diagrams = self.homology.compute(X)
        self.betti = self.homology.get_betti()
        return self.diagrams

    def plot(self, plot_graph=True, plot_hist=True, plot_data=False,
             plot_homology=False, **kwargs):
        if plot_graph and self.graph is not None:
            self.plotter.plot_graph(self.graph, **kwargs)
        if plot_hist and self.lens_values is not None:
            self.plotter.plot_lens_hist(self.lens_values)
        if plot_data and self.data is not None and self.clusters_map is not None:
            self.plotter.plot_data_clusters(self.data, self.clusters_map, **kwargs)
        if plot_homology:
            self.homology.plot()

    def get_cover(self): return self.cover
    def get_graph(self): return self.graph
    def get_nerve(self): return self.nerve
    def get_diagrams(self): return self.diagrams
    def get_betti(self): return self.betti
