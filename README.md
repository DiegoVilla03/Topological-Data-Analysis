# Python TDA Mapper

## Description

This project offers a Python implementation of the Mapper algorithm, a tool used in Topological Data Analysis (TDA) for visualizing and understanding the shape of high-dimensional data.

## Features

- Implementation of the Mapper algorithm.
- Flexible lens function input.
- Customizable cover generation (number of intervals, overlap).
- Support for various clustering algorithms (via `clusterer` parameter).
- Nerve complex construction (up to a specified order).
- Basic homology analysis (e.g., Betti numbers from `HomologyAnalyzer`).
- Visualization tools for Mapper graphs, lens histograms, original data clusters, and homology diagrams.

## Installation

To get started with this project, it's recommended to set up a virtual environment.

1.  **Navigate to the project directory:**
    Open your terminal and navigate to the folder where you have the project files.

2.  **Create and activate a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Here's a basic example of how to use the `Mapper` class:

```python
import numpy as np
from sklearn.datasets import make_circles
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt

from TDA import Mapper # Assuming Mapper is directly importable from TDA

# 1. Generate sample data
X, y = make_circles(n_samples=1000, noise=0.05, factor=0.3, random_state=42)

# 2. Define a lens function (e.g., projection onto the first coordinate)
# The lens_func should take the data X as input and return a 1D numpy array.
lens_func = lambda data: data[:, 0]

# 3. Initialize a clustering algorithm
clusterer = DBSCAN(eps=0.1, min_samples=5)

# 4. Initialize the Mapper
# - lens_func: The function to project data to a lower dimension.
# - n_intervals: Number of intervals to create in the cover of the lens range.
# - overlap: Percentage of overlap between adjacent intervals.
# - clusterer: The clustering algorithm to use on data subsets.
# - nerve_order: Maximum dimension of simplices to include in the nerve (default is 2, i.e., nodes, edges, triangles).
# - homology_dim: Maximum dimension of homology groups to compute (default is 1, i.e., H0, H1).
mapper = Mapper(
    lens_func=lens_func,
    n_intervals=10,
    overlap=0.3,
    clusterer=clusterer,
    nerve_order=2, 
    homology_dim=1 
)

# 5. Fit the mapper to the data
# This step applies the lens, generates the cover, clusters data in each part of the cover,
# and builds the nerve complex.
mapper.fit(X)

# 6. Plot the mapper graph
# - color_data: A 1D array of the same length as X, used to color the nodes of the Mapper graph.
#   This can be, for example, class labels, or values of another function on the data.
#   Here, we use the 'y' labels from make_circles.
# - layout: The layout algorithm for positioning nodes (e.g., 'spring', 'kamada_kawai', 'spectral').
mapper.plot_graph(color_data=y, layout='spring')
plt.title("Mapper Graph of Two Circles")
plt.show() # This will display the Mapper graph visualization.
```

## File Structure

-   `TDA/`: Core directory containing the Mapper algorithm implementation and related modules (`cover.py`, `homology.py`, `mapper_base.py`, etc.).
-   `Blobs.ipynb`, `homology.ipynb`, `rings.ipynb`: Jupyter notebooks with usage examples.
-   `requirements.txt`: A list of project dependencies.
-   `LICENSE`: Contains the license information for the project.
-   `README.md`: This file.

## Dependencies

The project relies on several Python libraries. Key dependencies include:

-   NumPy: For numerical operations.
-   scikit-learn: For clustering algorithms and potentially lens functions.
-   NetworkX: For graph creation and manipulation.
-   Gudhi / Ripser: For persistent homology calculations.
-   Matplotlib / Plotly: For generating visualizations.

A complete list of dependencies can be found in `requirements.txt`.

## License

This project is licensed under the terms of the LICENSE file.

## Examples

The repository includes several Jupyter notebooks that provide more detailed examples and use cases:

-   `Blobs.ipynb`: Demonstrates the Mapper algorithm on a dataset of Gaussian blobs.
-   `homology.ipynb`: Shows how to perform homology calculations and visualize persistence diagrams.
-   `rings.ipynb`: Applies Mapper to a dataset of concentric rings.

These notebooks serve as excellent starting points for exploring the capabilities of this library.
