#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 10:10:06 2023

@author: michele
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 13:17:18 2023

@author: michele
"""

import geopandas as gpd
import pandas as pd
import numpy as np
import rasterio 
import os

import matplotlib.pyplot as plt
from matplotlib import pyplot
from matplotlib import colors
import rasterio
from rasterio.plot import show
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar

# set directories
os.chdir('/home/michele/programming/python/data/CDAdistricts')
inputdir = '/home/michele/programming/python/data/CDAdistricts'

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
hillshade = inputdir + "/hillshade.tif"
hillshade = rasterio.open(hillshade)


# creation of a custom colormap
levels = [0,1,2,3]
# 1 = NF >> NF
# 2 = NF > F
# 3 = F > NF
# 4 = F > F
clrs = ['#eed5b7', 'yellowgreen', '#CD5555', 'darkolivegreen']

cmap, norm = colors.from_levels_and_colors(levels, clrs, extend='max')

os.chdir('/home/michele/programming/python/data/cd_br')
inputdir = '/home/michele/programming/python/data/cd_br/'


# hillshade large
hillshade2 = inputdir + "/anahillshade.tif"
hillshade2 = rasterio.open(hillshade2)

yearlist = ["1973-1987", "1987-1995", "1995-2003", "2003-2014", "2014-2021", "1973-2021"]
ans = []
    

def brvis(year):
        
    p1 = inputdir + year + ".tif"

    raster_p1 = rasterio.open(p1)
    
    fig, ax = plt.subplots(figsize = (20,12))
    
    plt.title('UNESCO BR Mount Elgon - Forest Cover Development for ' + year, fontsize=16)
    #fig.subplots_adjust(top=0.8)

    ax.set_box_aspect(1)
    # set labelsize
    ax.tick_params(axis='both', which='major', labelsize=7)
    
    show((raster_p1), ax=ax,
         #title='Forest cover development for '+ year,
         cmap = cmap, norm=norm, interpolation = 'bilinear')
    transition.boundary.plot(ax=ax, zorder=2, color='k', linewidth=0.6, ls="dashed")
    buffer.boundary.plot(ax=ax, zorder=2, color='#B5CF43', linewidth=0.6)
    core.boundary.plot(ax=ax, zorder=2, color='darkolivegreen', linewidth=0.6)   
    np.boundary.plot(ax=ax, zorder=2, color='red', linewidth=0.6)
    show((hillshade2),ax=ax, cmap='Greys', zorder=1, alpha=.2)
    
    # BR legend
    transitionp = mlines.Line2D([],[],color='k', label='transition zone')

    bufferp =mlines.Line2D([],[],color='#B5CF43', label='buffer zone')

    corep = mlines.Line2D([],[],color='darkolivegreen', label='core zone')

    dd = mlines.Line2D([],[],color='red', label='national park')

    be = mpatches.Patch(color='lightgrey', label='5km buffer BR')

    yellow_patch = mpatches.Patch(color='#eed5b7', label='NF >> NF')
    
    red_patch = mpatches.Patch(color='#CD5555', label='F >> NF')
    
    green_patch = mpatches.Patch(color='yellowgreen', label='NF >> F')
    
    lightgreen_patch = mpatches.Patch(color='darkolivegreen', label='F >> F')
    
    labelpatch = mpatches.Patch(color='white', label='(F = forest, NF = non-forest)')

    ax.legend(handles=[yellow_patch, red_patch, green_patch, lightgreen_patch, transitionp, bufferp, corep, dd],
                loc='upper center',
                bbox_to_anchor=(0.9,0.25),
                ncol=1,
                fontsize=12,
                frameon=False)
    
    # insert scalebar
    scalebar = AnchoredSizeBar(ax.transData,
                               25000, '25km', 'upper left',
                               pad=1,
                               color='black',
                               frameon=False,
                               size_vertical=1)
    
    ax.add_artist(scalebar)
    # export to current working directory
    plt.savefig("testFCdev_BR_"+year+".png",
                dpi = 500,
                # specifying tight here so that legend is not cut
                bbox_inches= "tight")

    pyplot.show()

# plot the list of years indicated before so that all years are plotted
for x in yearlist:
    ans.append(brvis(x))
    
show(ans)