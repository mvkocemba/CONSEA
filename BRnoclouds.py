#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 16:56:14 2023

@author: michele
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 10:23:01 2023

@author: michele
"""

import numpy as np
import geopandas as gpd
import pandas as pd
import shapely.wkt
import shapely.geometry

from glob import glob
import numpy as np
import rasterio 
import os

import geopandas as gpd
import earthpy.plot as ep
import matplotlib.pyplot as plt
import earthpy.spatial as es
from osgeo import ogr, gdal
from matplotlib import pyplot
from matplotlib import colors
import rasterio
from rasterio.plot import show
import fiona
# set directories
os.chdir('/home/michele/programming/python/data/CDAdistricts')
inputdir = '/home/michele/programming/python/data/CDAdistricts'

from osgeo import gdal, ogr, osr
from rasterio.plot import show, show_hist
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle
import matplotlib.lines as mlines

### load in vector data ###
# load BR data
BR = "MtElgonBRUgandaOutline.shp"
BR = gpd.read_file(BR)

#boundary 5km buffer
boundaryelgon = "boundaryelgon.shp"
boundaryelgon = gpd.read_file(boundaryelgon)

# load transition
transition = "transitionzone.shp"
transition = gpd.read_file(transition)

# load buffer
buffer = "bufferzone.shp"
buffer = gpd.read_file(buffer)

# load core
core = "core.shp"
core = gpd.read_file(core)

# load national park
np = "IUCNNationalparkboundary.shp"
np = gpd.read_file(np)

### load other raster data ###
# load hillshade

# hillshade large
hillshade2 = "/home/michele/programming/python/data/cd_br/anahillshade.tif"
hillshade2 = rasterio.open(hillshade2)
    


# creation of a custom colormap
# values
levels = [0,1,2,3,4,5,6,7,8]
# 0 = NF >> NF  '#F0E68C'
# 1 = NF > F 'yellowgreen'
# 2 = NF >> unclassified moccasin
# 3 = F >> NF '#CD5555'
# 4 = F >> F 'olivedrab'
# 5 = F >> unclassified darkseagreen
# 6 = unclassified >> NF salmon
# 7 = unclassified >> F lightgreen
# 8 = unclassified >> unclassified  white

# 2 = F > NF
# 3 = F > F
clrs = ['#F0E68C', 'yellowgreen', 'lightsalmon', '#CD5555', 'olivedrab', 'lawngreen', 'salmon', 'forestgreen', 'white']

cmap, norm = colors.from_levels_and_colors(levels, clrs, extend='max')

os.chdir('/home/michele/programming/python/data/BRclouds')
inputdir = '/home/michele/programming/python/data/BRclouds'



    
p1 = inputdir + "/Combination [1973CC - 1987CC].tif"
p2 = inputdir + "/Combination [1987CC - 1995CC].tif"
p3 = inputdir + "/Combination [1995CC - 2003CC].tif"
p4 = inputdir + "/Combination [2003CC - 2014CC].tif"
p5 = inputdir + "/Combination [2014CC - 2021CC].tif"
p6 = inputdir + "/Combination [1973CC - 2021CC].tif"

raster_p1 = rasterio.open(p1)
raster_p2 = rasterio.open(p2)
raster_p3 = rasterio.open(p3)
raster_p4 = rasterio.open(p4)
raster_p5 = rasterio.open(p5)
raster_p6 = rasterio.open(p6)

fig, ((axp1, axp2, axp3), (axp4, axp5, axmm)) = pyplot.subplots(ncols=3,
                                                                nrows=2,
                                                                figsize=(20,12))
fig.suptitle('UNESCO BR Mount Elgon - Forest Cover Development between 1973-2021\n',
             fontsize=20,y=1.03)
#fig.subplots_adjust(top=0.88)

axp1.set_box_aspect(1)
axp2.set_box_aspect(1)
axp3.set_box_aspect(1)
axp4.set_box_aspect(1)
axp5.set_box_aspect(1)
axmm.set_box_aspect(1)
# set labelsize
axp1.tick_params(axis='both', which='major', labelsize=7)
#axp1.set_xlim(xlim)
#axp1.set_ylim(ylim)

axp2.tick_params(axis='both', which='major', labelsize=7)
#axp2.set_xlim(xlim)
#axp2.set_ylim(ylim)

axp3.tick_params(axis='both', which='major', labelsize=7)
#axp3.set_xlim(xlim)
#axp3.set_ylim(ylim)

axp4.tick_params(axis='both', which='major', labelsize=7)
#axp4.set_xlim(xlim)
#axp4.set_ylim(ylim)

axp5.tick_params(axis='both', which='major', labelsize=7)
#axp5.set_xlim(xlim)
#axp5.set_ylim(ylim)

axmm.tick_params(axis='both', which='major', labelsize=7)


show((raster_p1), ax=axp1, title='1973-1987', cmap = cmap, norm=norm, interpolation = 'bilinear')
show((raster_p2), ax=axp2, title='1987-1995', cmap = cmap, norm=norm, interpolation = 'bilinear')
show((raster_p3), ax=axp3, title='1995-2003', cmap = cmap, norm=norm, interpolation = 'bilinear')
show((raster_p4), ax=axp4, title='2003-2014', cmap = cmap, norm=norm, interpolation = 'bilinear')
show((raster_p5), ax=axp5, title='2014-2021', cmap = cmap, norm=norm, interpolation = 'bilinear')
# shapefiles
# UNESCO BR boundary
transition.boundary.plot(ax=axmm, zorder=2, color='#EBFF93', linewidth=0.4)
transition.boundary.plot(ax=axp1, zorder=2, color='k', linewidth=0.4, ls="dashed")
transition.boundary.plot(ax=axp2, zorder=2, color='k', linewidth=0.4, ls="dashed")
transition.boundary.plot(ax=axp3, zorder=2, color='k', linewidth=0.4, ls="dashed")
transition.boundary.plot(ax=axp4, zorder=2, color='k', linewidth=0.4, ls="dashed")
transition.boundary.plot(ax=axp5, zorder=2, color='k', linewidth=0.4, ls="dashed")
# buffer zone

buffer.boundary.plot(ax=axmm, zorder=2, color='#B5CF43', linewidth=0.4)
buffer.boundary.plot(ax=axp1, zorder=2, color='#B5CF43', linewidth=0.4)
buffer.boundary.plot(ax=axp2, zorder=2, color='#B5CF43', linewidth=0.4)
buffer.boundary.plot(ax=axp3, zorder=2, color='#B5CF43', linewidth=0.4)
buffer.boundary.plot(ax=axp4, zorder=2, color='#B5CF43', linewidth=0.4)
buffer.boundary.plot(ax=axp5, zorder=2, color='#B5CF43', linewidth=0.4)

# core zone

core.boundary.plot(ax=axmm, zorder=2, color='darkolivegreen', linewidth=0.4)
core.boundary.plot(ax=axp1, zorder=2, color='darkolivegreen', linewidth=0.4)
core.boundary.plot(ax=axp2, zorder=2, color='darkolivegreen', linewidth=0.4)
core.boundary.plot(ax=axp3, zorder=2, color='darkolivegreen', linewidth=0.4)
core.boundary.plot(ax=axp4, zorder=2, color='darkolivegreen', linewidth=0.4)
core.boundary.plot(ax=axp5, zorder=2, color='darkolivegreen', linewidth=0.4)

# nationalpark 

np.boundary.plot(ax=axmm, zorder=2, color='red', linewidth=0.4)
np.boundary.plot(ax=axp1, zorder=2, color='red', linewidth=0.4)
np.boundary.plot(ax=axp2, zorder=2, color='red', linewidth=0.4)
np.boundary.plot(ax=axp3, zorder=2, color='red', linewidth=0.4)
np.boundary.plot(ax=axp4, zorder=2, color='red', linewidth=0.4)
np.boundary.plot(ax=axp5, zorder=2, color='red', linewidth=0.4)


show((hillshade2),ax=axp1, cmap='Greys', zorder=1, alpha=.2)
show((hillshade2),ax=axp2, cmap='Greys', zorder=1, alpha=.2)
show((hillshade2),ax=axp3, cmap='Greys', zorder=1, alpha=.2)
show((hillshade2),ax=axp4, cmap='Greys', zorder=1, alpha=.2)
show((hillshade2),ax=axp5, cmap='Greys', zorder=1, alpha=.2)
show((hillshade2),ax=axmm, cmap='Greys', zorder=1, alpha=.2)

transition.plot(ax=axmm, zorder=1, facecolor='#EBFF93')
buffer.plot(ax=axmm, facecolor='#B5CF43')
core.plot(ax=axmm, facecolor='darkolivegreen')

# BR legend
transitionp = mpatches.Patch(color='#EBFF93', label='transition zone')

bufferp = mpatches.Patch(color='#B5CF43', label='buffer zone')

corep = mpatches.Patch(color='darkolivegreen', label='core zone')

dd = mlines.Line2D([],[],color='red', label='national park')

dd = mlines.Line2D([],[],color='red', label='national park')

be = mpatches.Patch(color='lightgrey', label='5km buffer BR')

axmm.legend(handles=[transitionp, bufferp, corep, dd],
            loc='lower right',
            #bbox_to_anchor=(1.75,1.21),
            ncol=1,
            fontsize=10,
            frameon=False)


yellow_patch = mpatches.Patch(color='#F0E68C', label='NF >> NF')
red_patch = mpatches.Patch(color='#CD5555', label='F >> NF')
green_patch = mpatches.Patch(color='yellowgreen', label='NF >> NF')
lightgreen_patch = mpatches.Patch(color='olivedrab', label='NF >> F')

F_to_u = mpatches.Patch(color='lawngreen', label='F >> unclassified')
NF_to_u = mpatches.Patch(color='lightsalmon', label='NF >> unclassified')
u_to_NF = mpatches.Patch(color='salmon', label='unclassified >> NF')
u_to_F = mpatches.Patch(color='forestgreen', label='unclassified >> F')
u_t_u = mpatches.Patch(color='white', label='unclassified >> unclassified')

# 0 = NF >> NF  '#F0E68C'
# 1 = NF > F 'yellowgreen'
# 2 = NF >> unclassified moccasin
# 3 = F >> NF '#CD5555'
# 4 = F >> F 'olivedrab'
# 5 = F >> unclassified palegreen
# 6 = unclassified >> NF salmon
# 7 = unclassified >> F greenyellow
# 8 = unclassified >> unclassified  white



labelpatch = mpatches.Patch(color='white', label='(F = forest, NF = non-forest)')

axp1.legend(handles=[yellow_patch, red_patch, green_patch, lightgreen_patch, F_to_u, NF_to_u, u_to_NF, u_to_F, u_t_u],
            loc='upper center',
            bbox_to_anchor=(1.87,1.37),
            ncol=3,
            fontsize=14,
            frameon=False)

axp2.legend(handles=[labelpatch],
            loc='upper center',
            bbox_to_anchor=(0.45,1.15),
            ncol=1,
            fontsize=12,
            frameon=False)


# export to current working directory
#plt.savefig("FCdev_BR_clouds.png",
#            dpi = 500,
#            # specifying tight here so that legend is not cut
#            bbox_inches= "tight")

pyplot.show()