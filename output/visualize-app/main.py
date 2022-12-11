
from flask import Flask
from flask import request
app = Flask(__name__)

# pip install geopandas

# pip install contextily

import numpy as np
import pandas as pd
import geopandas as gpd
import contextily as ctx
from IPython.display import display, Markdown
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

districts = gpd.read_file('india_district.geojson')
census = pd.read_csv("india_censusdata.csv")

districts["District name"] = districts["NAME_2"]
df = pd.merge(districts, census, on='District name', how='left')
gdf = gpd.GeoDataFrame(df)
gdf = gdf.to_crs(epsg=3857)

ax = gdf.plot(figsize=(8, 8), alpha=0.9, edgecolor='k')
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)
ctx.add_basemap(ax)

def plot(col="Population"):
    display(Markdown("#### &nbsp;&nbsp;"+col))
    fig, axis = plt.subplots(1, 1, figsize=(8,8))
    divider = make_axes_locatable(axis)
    cax = divider.append_axes("bottom", size="5%", pad=0.1)
    ax = gdf.plot(alpha=0.7,
                  edgecolor='k',
                  cmap="plasma",
                  column=col,
                  legend=True,
                  ax=axis,
                  cax=cax,
                  missing_kwds={'color': 'white'},
                  legend_kwds={'label': "Min: "+str(int(gdf[col].min()))+",   Max: "+str(int(gdf[col].max())),
                               'orientation': "horizontal"})
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    ctx.add_basemap(ax)
    plt.show()
    display(Markdown('***'))

display(Markdown('***'))
for col in gdf.columns[15:].to_list():
    plot(col)




if __name__ == '__main__':
    app.run()