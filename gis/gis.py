import geopandas as gpd
import matplotlib.pyplot as plt

# File paths
base1_file = "kumpula/L4133D_palstaalue.shp"
base2_file = "kumpula/L4133D_palstatunnus.shp" # ID column
buildings_file = "kumpula/L4133D_kiinteistoraja.shp"
border_marks_file = "kumpula/L4133D_rajamerkki.shp"

# read files
base1 = gpd.read_file(base1_file)
base2 = gpd.read_file(base2_file)
buildings = gpd.read_file(buildings_file)
border_marks = gpd.read_file(border_marks_file)

f, ax = plt.subplots(1)
base1.plot(ax=ax, cmap='Greys')
#base2.plot(ax=ax, c)
buildings.plot(ax=ax, cmap='Blues')
border_marks.plot(ax=ax, cmap='Reds')
plt.show()

#base1_plot = base1.plot()
#base2_plot = base2.plot(ax=base1)
#buildings_plot = buildings.plot(ax=base2_plot)
#border_marks_plot = border_marks.plot(ax=buildings_plot)

#grid.plot(ax=basemap, linewidth=0.02)
#plt.tight_layout()

#result = gpd.overlay(grid, hel, how='intersection')
#result.plot(color="b")
#
#plt.tight_layout()
#plt.show()
