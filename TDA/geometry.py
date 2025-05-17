import numpy as np
import plotly.graph_objects as go

class geometry:
    def __init__(self, points: np.ndarray):
        """
        Internal constructor. Use classmethods to create from surface types.
        """
        self.points = points  

    @classmethod
    def from_sphere(cls, radius=1, n=1000):
        def sample():
            u = np.random.uniform()
            v = np.random.uniform()
            theta = 2 * np.pi * u
            phi = np.arccos(2 * v - 1)
            x = radius * np.sin(phi) * np.cos(theta)
            y = radius * np.sin(phi) * np.sin(theta)
            z = radius * np.cos(phi)
            return np.array([x, y, z])
        return cls(np.array([sample() for _ in range(n)]))

    @classmethod
    def from_torus(cls, R=3, r=1, n=1000):
        def sample():
            theta = np.random.uniform(0, 2 * np.pi)
            phi = np.random.uniform(0, 2 * np.pi)
            x = (R + r * np.cos(theta)) * np.cos(phi)
            y = (R + r * np.cos(theta)) * np.sin(phi)
            z = r * np.sin(theta)
            return np.array([x, y, z])
        return cls(np.array([sample() for _ in range(n)]))

    @classmethod
    def from_mobius(cls, width=1, n=1000):
        def sample():
            u = np.random.uniform(0, 2 * np.pi)
            v = np.random.uniform(-width, width)
            x = (1 + (v / 2) * np.cos(u / 2)) * np.cos(u)
            y = (1 + (v / 2) * np.cos(u / 2)) * np.sin(u)
            z = (v / 2) * np.sin(u / 2)
            return np.array([x, y, z])
        return cls(np.array([sample() for _ in range(n)]))

    @classmethod
    def from_klein(cls, n=1000):
        def sample():
            u = np.random.uniform(0, 2 * np.pi)
            v = np.random.uniform(0, 2 * np.pi)
            x = (2 + np.cos(u / 2) * np.sin(v) - np.sin(u / 2) * np.sin(2 * v)) * np.cos(u)
            y = (2 + np.cos(u / 2) * np.sin(v) - np.sin(u / 2) * np.sin(2 * v)) * np.sin(u)
            z = np.sin(u / 2) * np.sin(v) + np.cos(u / 2) * np.sin(2 * v)
            return np.array([x, y, z])
        return cls(np.array([sample() for _ in range(n)]))

    def plot(self, size=2, color=None, title="Random Points"):
        x, y, z = self.points.T
        fig = go.Figure(data=[go.Scatter3d(
            x=x, y=y, z=z,
            mode='markers',
            marker=dict(size=size, color=color if color is not None else z, colorscale='Viridis')
        )])
        fig.update_layout(
            title=title,
            scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'),
            margin=dict(l=0, r=0, b=0, t=30)
        )
        fig.show()

    

    def get(self):
        """
        Returns the point array (3, N).
        """
        return self.points

