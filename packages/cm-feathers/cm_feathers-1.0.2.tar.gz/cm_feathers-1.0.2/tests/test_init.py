from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

import feathers


def test_version():
    assert feathers.__version__

def test_list_cmaps():
    cmaps = feathers.list_cmaps()
    assert isinstance(cmaps, list)
    assert len(cmaps) > 0
    assert all(isinstance(cmap, str) for cmap in cmaps)
    assert all(cmap in cmaps for cmap in ["spotted_pardalote", "plains_wanderer", "bee_eater"])

def test_get_cmap():
    # Get from package
    cmap = feathers.get_cmap("spotted_pardalote")
    assert isinstance(cmap, LinearSegmentedColormap)
    assert cmap.name == "spotted_pardalote"
    assert cmap(0.0)

    # Test reverse colormap
    cmap_r = feathers.get_cmap("spotted_pardalote_r")
    assert isinstance(cmap_r, LinearSegmentedColormap)
    assert cmap_r.name == "spotted_pardalote_r"
    assert cmap_r(1.0) == cmap(0.0)

def test_registered_cmap():
    # Check if the colormap is registered with matplotlib
    cmap = plt.get_cmap("spotted_pardalote")
    assert isinstance(cmap, LinearSegmentedColormap)
    assert cmap.name == "spotted_pardalote"
