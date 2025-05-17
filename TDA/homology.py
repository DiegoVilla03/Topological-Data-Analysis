import numpy as np
import matplotlib.pyplot as plt
from persim import plot_diagrams
import gudhi

class HomologyAnalyzer:
    def __init__(self, maxdim=None):
        """maxdim: dimensión máxima para calcular homología. Si es None, se ajusta a la dimensión de los datos de entrada."""
        self.maxdim = maxdim
        self.diagrams = None
        self.betti = None

    def compute(self, X):
        """
        Construye la filtración alfa para el conjunto de puntos X
        y calcula su homología persistente.

        X: array-like de forma (n_points, dim)
        Devuelve los diagramas de persistencia.
        """
        X = np.asarray(X)
        data_dim = X.shape[1]-1
        if self.maxdim is None:
            self.maxdim = data_dim
        else:
            self.maxdim = min(self.maxdim, data_dim)

        alpha_complex = gudhi.AlphaComplex(points=X)
        simplex_tree = alpha_complex.create_simplex_tree(max_alpha_square=np.inf)
        simplex_tree.compute_persistence(
            homology_coeff_field=2,
            min_persistence=0,
            persistence_dim_max=self.maxdim
        )

        # Obtener diagramas usando persistence_intervals_in_dimension
        diagrams = []
        for dim in range(self.maxdim + 1):
            intervals = simplex_tree.persistence_intervals_in_dimension(dim)
            if intervals.size == 0:
                diagrams.append(np.empty((0, 2)))
            else:
                diagrams.append(intervals)

        self.diagrams = diagrams
        # Calcular números de Betti (clases que persisten hasta infinito)
        self.betti = [np.sum(np.isinf(d[:, 1])) for d in self.diagrams]
        return self.diagrams

    def plot(self, show=True, **kwargs):
        """
        Dibuja los diagramas de persistencia.
        """
        if self.diagrams is None:
            raise ValueError(
                "Primero ejecuta .compute(X) para obtener los diagramas."
            )
        plot_diagrams(self.diagrams, **kwargs)
        if show:
            plt.show()

    def get_betti(self):
        """Retorna la lista de números de Betti para dimensiones 0..maxdim"""
        if self.betti is None:
            raise ValueError(
                "Ejecuta primero .compute(X) para calcular Betti."
            )
        return self.betti
