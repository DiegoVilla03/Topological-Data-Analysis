import numpy as np
import itertools

class CoverGenerator:
    def __init__(self, n_intervals=10, overlap=0.1):
        if not (0 <= overlap < 1):
            raise ValueError("overlap debe estar entre 0 y 1 (no incluido)")
        self.n_intervals = n_intervals
        self.overlap = overlap

    def compute_cover(self, lens_values):
        lens_values = np.asarray(lens_values)
        if lens_values.ndim == 1:
            lens_values = lens_values.reshape(-1, 1)

        n_samples, n_dims = lens_values.shape
        min_vals = lens_values.min(axis=0)
        max_vals = lens_values.max(axis=0)
        lengths = max_vals - min_vals

        if np.any(lengths == 0):
            raise ValueError("Al menos una dimensión tiene valores constantes; no se puede generar cubierta.")

        interval_sizes = lengths / (self.n_intervals - (self.n_intervals - 1) * self.overlap)
        steps = interval_sizes * (1 - self.overlap)

        starts_list = [np.linspace(min_vals[d], max_vals[d] - interval_sizes[d], self.n_intervals) for d in range(n_dims)]
        cover = []

        for starts in itertools.product(*starts_list):
            bounds = [(s, s + interval_sizes[d]) for d, s in enumerate(starts)]
            mask = np.ones(n_samples, dtype=bool)
            for d in range(n_dims):
                mask &= (lens_values[:, d] >= bounds[d][0]) & (lens_values[:, d] <= bounds[d][1])
            inds = np.where(mask)[0]
            cover.append((bounds, inds))

        return cover

