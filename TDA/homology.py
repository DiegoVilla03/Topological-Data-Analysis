import numpy as np
from ripser import ripser
from persim import plot_diagrams
import matplotlib.pyplot as plt

class HomologyAnalyzer:
    def __init__(self, maxdim=1):
        """maxdim: dimensión máxima para calcular homología."""
        self.maxdim = maxdim
        self.diagrams = None
        self.betti = None

    def compute(self, X):
        """
        Calcula la homología persistente del punto X.
        Devuelve los diagramas de persistencia.
        """
        result = ripser(X, maxdim=self.maxdim)
        self.diagrams = result['dgms']
        # Betti: número de clases que persisten hasta infinito
        self.betti = [np.sum(np.isinf(d[:,1])) for d in self.diagrams]
        return self.diagrams

    def plot(self, show=True, **kwargs):
        """
        Dibuja los diagramas de persistencia.
        """
        if self.diagrams is None:
            raise ValueError("Primero ejecuta .compute(X) para obtener los diagramas.")
        plot_diagrams(self.diagrams, **kwargs)
        if show:
            plt.show()

    def get_betti(self):
        """Retorna la lista de números de Betti para dimensiones 0..maxdim"""
        return self.betti