import numpy as np

class CoverGenerator:
    def __init__(self, n_intervals=10, overlap=0.1):
        if not (0 <= overlap < 1):
            raise ValueError("overlap debe estar entre 0 y 1 (no incluido)")
        self.n_intervals = n_intervals
        self.overlap = overlap

    def compute_cover(self, lens_values):
        """
        Retorna lista de (start, end, indices) basada en lens_values.
        """
        min_l, max_l = lens_values.min(), lens_values.max()
        length = max_l - min_l
        if length == 0:
            raise ValueError("Valores de lente idénticos; no se puede generar cubierta.")

        size = length / (self.n_intervals - (self.n_intervals - 1) * self.overlap)
        step = size * (1 - self.overlap)
        cover = []
        start = min_l
        for _ in range(self.n_intervals):
            end = start + size
            inds = np.where((lens_values >= start) & (lens_values <= end))[0]
            cover.append((start, end, inds))
            start += step
        return cover
