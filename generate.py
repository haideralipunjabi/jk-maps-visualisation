import argparse
import os
import csv
import geopandas as gpd
import numpy
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib import cm
from mpl_toolkits.axes_grid1 import make_axes_locatable

parser = argparse.ArgumentParser(description='Make J&K Maps')
parser.add_argument("csv")
parser.add_argument("--color")
parser.add_argument("--label")
args = parser.parse_args()


file_location = args.csv
color = args.color if args.color else "GnBu"
label = args.label if args.label else ""

fp = "data/districts.shp"
map_data = gpd.read_file(fp)

if not os.path.exists(file_location):
    print("CSV file doesn't exist")
    exit()

reader = csv.reader(open(file_location, "r"))
district_data = {x[0]: x[1] for x in reader}

for index, row in map_data.iterrows():
    if row['dtname'] == 'Bandipore':
        map_data.loc[index, 'dtname'] = 'Bandipora'
    if row['dtname'] == 'Baramula':
        map_data.loc[index, 'dtname'] = 'Baramulla'
    if row['dtname'] == 'Badgam':
        map_data.loc[index, 'dtname'] = 'Budgam'
    if row['dtname'] == 'Punch':
        map_data.loc[index, 'dtname'] = 'Poonch'
    if row['dtname'] == 'Shupiyan':
        map_data.loc[index, 'dtname'] = 'Shopian'

map_data['value'] = numpy.NaN

for index, row in map_data.iterrows():
    if list(district_data.keys()).__contains__(row['dtname']):
        map_data.loc[index, 'value'] = float(
            district_data[row['dtname']]) if district_data[row['dtname']] != "NA" else numpy.NaN

fig, ax = plt.subplots(1, 1)
plt.axis("off")
ax1 = map_data.plot(column='value', ax=ax, cmap=color, edgecolor="black", linewidth=0.2, missing_kwds={
    "linewidth": 0.2,
    "edgecolor": "black",
    "facecolor": "white"
})


for index, row in map_data.iterrows():
    x = row['geometry'].centroid.x
    y = row['geometry'].centroid.y
    if row['dtname'] == "Muzaffarabad":
        x = row['geometry'].centroid.x - 0.1
        y = row['geometry'].centroid.y
    ax1.annotate(row['dtname'], xy=(x, y+0.02), ha="center", fontsize=4)
    ax1.plot(x, y, 'bo', markersize=1)

norm = Normalize(vmin=map_data['value'].min(), vmax=map_data['value'].max())
n_cmap = cm.ScalarMappable(norm=norm, cmap=color)
n_cmap.set_array([])
if not map_data['value'].min() == map_data['value'].max():
    divider = make_axes_locatable(ax1)
    cax = divider.new_vertical(size="2.5%", pad=0.2, pack_start=True)
    fig.add_axes(cax)
    fig.colorbar(n_cmap, label=label, cax=cax, orientation="horizontal")

plt.savefig("out.png", format='png', dpi=1200, bbox_inches='tight')
