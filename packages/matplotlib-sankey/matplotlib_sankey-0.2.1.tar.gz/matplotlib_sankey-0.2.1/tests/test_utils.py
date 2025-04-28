from matplotlib import colormaps
from matplotlib.colors import Colormap

from matplotlib_sankey._utils import _generate_cmap, from_matrix


def test_utils_cmap() -> None:
    """Testing utils function to generate cmap."""
    assert isinstance(_generate_cmap("tab10", 4), Colormap)
    assert isinstance(_generate_cmap("viridis", 4), Colormap)
    assert _generate_cmap("viridis", 4).N == 4
    assert isinstance(_generate_cmap(["#ec4899", "#0284c7", "#16a34a", "#f59e0b"], 4), Colormap)
    assert isinstance(_generate_cmap([(0.4, 0.1, 0.9), (0.1, 0.1, 0.7)], 4), Colormap)
    assert isinstance(_generate_cmap(colormaps["tab10"], 4), Colormap)


def test_from_matrix() -> None:
    """Testing from matrix helper function."""
    assert len(from_matrix([[0, 0], [0, 0]])) == 0

    assert len(from_matrix([[0, 1], [0, 0]])) == 1

    assert len(from_matrix([[0, 1], [0, 1]])) == 2
