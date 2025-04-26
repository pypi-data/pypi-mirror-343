from __future__ import annotations

from matplotlib import colormaps
from matplotlib.colors import LinearSegmentedColormap

# Converted from https://github.com/shandiya/feathers/blob/main/R/feathers.R
_palettes = {
    "spotted_pardalote" : ("#feca00", "#d36328", "#cb0300", "#b4b9b3", "#424847", "#000100"),
    "plains_wanderer"   : ("#edd8c5", "#d09a5e", "#e7aa01", "#ac570f", "#73481b", "#442c0e", "#0d0403"),
    "bee_eater"         : ("#00346E", "#007CBF", "#06ABDF", "#EDD03E", "#F5A200", "#6D8600", "#424D0C"),
    "fruit_dove"        : ("#BD338F", "#EB8252", "#F5DC83", "#CDD4DC", "#8098A2", "#8FA33F", "#5F7929", "#014820"),
    "eastern_rosella"   : ("#cd3122", "#f4c623", "#bee183", "#6c905e", "#2f533c", "#b8c9dc", "#2f7ab9"),
    "oriole"            : ("#8a3223", "#bb5645", "#d97878", "#e2aba0", "#d0cfe9", "#a29eb8", "#6c6b75", "#b8a53f", "#93862a", "#4d4019"),
    "princess_parrot"   : ("#7090c9", "#8cb3de", "#afbe9f", "#616020", "#6eb245", "#214917", "#cf2236", "#d683ad"),
    "superb_fairy_wren" : ("#4F3321", "#AA7853", "#D9C4A7", "#B03F05", "#020503"),
    "cassowary"         : ("#BDA14D", "#3EBCB6", "#0169C4", "#153460", "#D5114E", "#A56EB6", "#4B1C57", "#09090C"),
    "yellow_robin"      : ("#E19E00", "#FBEB5B", "#85773A", "#979EB9", "#727B98", "#454B56", "#201B1E"),
    "galah"             : ("#FFD2CF", "#E9A7BB", "#D05478", "#AAB9CC", "#8390A2", "#4C5766"),
    "blue_kookaburra"   : ("#b5effb", "#0b7595", "#02407c", "#06213a", "#c45829", "#9C4620", "#622C14", "#d4d8e3", "#b8bcd8", "#ad8d9f", "#725f77")
}

def get_cmap(name: str) -> LinearSegmentedColormap:
    """
    Get a colormap by name.

    Parameters
    ----------
    name : str
        The name of the colormap to get.

    Returns
    -------
    matplotlib.colors.LinearSegmentedColormap
        The colormap.
    """

    reverse = name.endswith("_r")
    if reverse:
        key = name[:-2]
    else:
        key = name

    if key not in _palettes:
        raise ValueError(f"Key {key} not found in feathers.")

    colors = _palettes[key]
    if reverse:
        colors = colors[::-1]

    return LinearSegmentedColormap.from_list(name, colors)

def _register_all():
    """
    Register all colormaps with matplotlib.
    """
    for name, colors in _palettes.items():
        for suffix in ("", "_r"):
            colormaps.register(get_cmap(name+suffix))

def list_cmaps():
    """
    List all available colormaps.

    Returns
    -------
    list
        A list of colormap names.
    """
    return list(_palettes.keys())

