# vtpk-reader

[![CI](https://github.com/kshklovsky/vtpk-reader/actions/workflows/ci.yml/badge.svg)](https://github.com/kshklovsky/vtpk-reader/actions/workflows/ci.yml)
[![Coverage Status](https://coveralls.io/repos/github/kshklovsky/vtpk-reader/badge.svg?branch=main)](https://coveralls.io/github/kshklovsky/vtpk-reader?branch=main)

A library to read ESRI Vector Tile Package (.vtpk) files

## Installation
```
pip install vtpk_reader
```

## Getting started
Read vtpk file and extract some features

```Python
from vtpk_reader import Vtpk

vtpk = Vtpk("path/to/your/vtpk/file.vtpk")
# Get all tiles at LOD (level of detail) zero, there should only be one tiles
tiles = vtpk.get_tiles(0, None)  
# Get the one of the tiles
one_tile = list(tiles)[0]
# Extract the tile features
features = vtpk.tile_features(one_tile)
# Look at the keys in the data
print(f"{features.keys()})
```

## More detailed example using `dodge_city.vtpk`

This file is can be found at by [searching](https://www.arcgis.com/home/search.html?searchTerm=dodge+vtpk#content) for "vtpk" and "dodge" on www.arcgis.com. Based on the name and the description, it probably does not contain content not available elsewhere, but being small it is a useful test file.

```python
from vtpk_reader import Vtpk
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as cx

# Load the vtpk
vtpk = Vtpk("dodge_city.vtpk")
# Create a matplotlib plot
fig, ax = plt.subplots(figsize=(10, 10))
# Get all the tiles at the maximum Level Of Detail (LOD)
# ... not normally recommended, but in case of small VTPKs it should be OK?
tiles = vtpk.get_tiles([vtpk.max_lod], None)
# Get a color palette from matplotlib
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

for idx_tile, tile in enumerate(tiles):
  features = vtpk.tile_features(tile)

  # Plot every kind of feature there is
  for feature_key_idx, feature_key in enumerate(features.keys()):
    gdf = gpd.GeoDataFrame(
      [prop["geometry"] for prop in features[feature_key]["features"]], 
      columns=["geometry"],
      crs=vtpk.crs, 
      geometry="geometry",
    )
    gdf.plot(ax=ax, alpha=0.25, color=colors[idx_tile])

# Add a basemap
cx.add_basemap(ax, source=cx.providers.CartoDB.DarkMatter)
# Expand the plot limits by a factor
increase_factor = 0.125
xlim = ax.get_xlim() 
xextent = xlim[1] - xlim[0]
ylim = ax.get_ylim() 
yextent = ylim[1] - ylim[0]
ax.set_xlim(xlim[0] - xextent*increase_factor, xlim[1] + xextent*increase_factor/2)
ax.set_ylim(ylim[0] - yextent*increase_factor, ylim[1] + yextent*increase_factor/2)
ax.set_axis_off()
```

You should get something like this:
![logo](sample.png)

