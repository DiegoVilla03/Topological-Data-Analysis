import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class TimeEmbedding(BaseEstimator, TransformerMixin):
    """
    Reconstruye el espacio de fases de una serie de tiempo mediante el embedding de Takens.

    Parámetros
    ----------
    dimension : int
        Número de dimensiones del embedding (m).
    time_delay : int
        Retardo temporal (tau) entre coordenadas.
    stride : int, default=1
        Paso entre embeddings consecutivos.
    """
    def __init__(self, dimension: int = 3, time_delay: int = 1, stride: int = 1):
        self.dimension = dimension
        self.time_delay = time_delay
        self.stride = stride

    def fit(self, X, y=None):
        # No hay parámetros a ajustar
        return self

    def transform(self, X, y=None):
        """
        Aplica el embedding de Takens a una o varias series univariantes.

        Parameters
        ----------
        X : array-like, shape (n_timestamps,) o (n_samples, n_timestamps)
            Serie(s) de tiempo univariante(s).

        Returns
        -------
        embeddings : np.ndarray
            Embeddings reconstruidos. Si X es 1D, devuelve un array de forma
            (n_vectors, dimension). Si X es 2D, devuelve
            (n_samples, n_vectors, dimension).
        """
        X_arr = np.asarray(X)
        # Asegurar forma (n_samples, T)
        if X_arr.ndim == 1:
            X_arr = X_arr[np.newaxis, :]
        n_samples, T = X_arr.shape
        m = self.dimension
        tau = self.time_delay
        # Cantidad de vectores posibles
        max_start = T - (m - 1) * tau
        if max_start <= 0:
            raise ValueError(
                f"Serie demasiado corta para dimension={m}, time_delay={tau}"
            )
        n_vectors = 1 + (max_start - 1) // self.stride
        # Preparar output
        out = np.empty((n_samples, n_vectors, m))
        for i in range(n_samples):
            for j in range(n_vectors):
                start = j * self.stride
                indices = start + np.arange(0, m * tau, tau)
                out[i, j] = X_arr[i, indices]
        # Si el usuario pasó una sola serie, quitamos la dimensión de batch
        if out.shape[0] == 1:
            return out[0]
        return out