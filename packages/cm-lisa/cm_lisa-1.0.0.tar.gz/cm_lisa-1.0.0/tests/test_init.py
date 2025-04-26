from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

import lisa


def test_version():
    assert lisa.__version__

def test_list_cmaps():
    cmaps = lisa.list_cmaps()
    assert isinstance(cmaps, list)
    assert len(cmaps) > 0
    assert all(isinstance(cmap, str) for cmap in cmaps)
    assert all(cmap in cmaps for cmap in ["Cezanne", "vanGogh", "Turner"])

def test_get_cmap():
    # Get from package
    cmap = lisa.get_cmap("Rembrandt")
    assert isinstance(cmap, LinearSegmentedColormap)
    assert cmap.name == "Rembrandt"
    assert cmap(0.0)

    # Test reverse colormap
    cmap_r = lisa.get_cmap("Rembrandt_r")
    assert isinstance(cmap_r, LinearSegmentedColormap)
    assert cmap_r.name == "Rembrandt_r"
    assert cmap_r(1.0) == cmap(0.0)

def test_registered_cmap():
    # Check if the colormap is registered with matplotlib
    cmap = plt.get_cmap("Warhol")
    assert isinstance(cmap, LinearSegmentedColormap)
    assert cmap.name == "Warhol"
