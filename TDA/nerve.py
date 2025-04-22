import itertools

class NerveBuilder:
    @staticmethod
    def compute_nerve(clusters_indices, max_order=2):
        """
        clusters_indices: dict nodo->iterable de índices
        max_order: orden máximo de símplices a generar (2 = pares, 3 = tríos, etc.)
        Retorna lista de tuplas representando los símplices hasta max_order.
        """
        # Convertir a sets
        clusters_sets = {nid: set(inds) for nid, inds in clusters_indices.items()}
        nerve = []
        nodes = list(clusters_sets.keys())
        # Generar simplices de tamaño 2 a max_order
        for r in range(2, min(max_order, len(nodes)) + 1):
            for combo in itertools.combinations(nodes, r):
                inter = set.intersection(*(clusters_sets[n] for n in combo))
                if inter:
                    nerve.append(combo)
        return nerve