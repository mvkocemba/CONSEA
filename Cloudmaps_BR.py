#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 13:17:18 2023

@author: michele
"""

# load in all libraries
import os
import geopandas as gpd
import rasterio 
import matplotlib.pyplot as plt
from matplotlib import pyplot
from matplotlib import colors
from rasterio.plot import show
import matplotlib.lines as mlines

# set directories
os.chdir('X')
inputdir = 'X'

### load in vector data ###

#boundary 5km buffer
boundaryelgon = "boundaryelgon.shp"
boundaryelgon = gpd.read_file(boundaryelgon)

# hillshade large
hillshade2 = inputdir + "/anahillshade.tif"
hillshade2 = rasterio.open(hillshade2)

yearlist = ["1973", "1987", "1995", "2003", "2014", "2021"]
ans = []

# creation of a custom colormap
# values
levels = [1,2]
# 1 = NF >> NF
# 2 = NF > F
# 3 = F > NF
# 4 = F > F
clrs = ['#eed5b7', 'darkolivegreen']

cmap, norm = colors.from_levels_and_colors(levels, clrs, extend='max')
    

def brvis(year):
    
    clouddir = "DEFINECLOUDDIR"
    
    cloud = clouddir + year + "_clouds.shp"
    cloud = gpd.read_file(cloud)
    
    inputdir = "DEFINEINPUTDIR"
        
    p1 = inputdir + year + "ND.tif"

    raster_p1 = rasterio.open(p1)
    
    fig, ax = plt.subplots(figsize = (20,12))
    
    plt.title('Cloud coverage for year ' + year, fontsize=16)
    #fig.subplots_adjust(top=0.8)

    ax.set_box_aspect(1)
    # set labelsize
    ax.tick_params(axis='both', which='major', labelsize=9)
    
    show((raster_p1), ax=ax,
         #title='Forest cover development for '+ year,
         cmap = cmap, norm=norm, interpolation = 'bilinear')
    
    show((hillshade2),ax=ax, cmap='Greys', zorder=1, alpha=.2)
    
    
    cloud.boundary.plot(ax=ax, zorder=2, color='red', linewidth=0.6)
    boundaryelgon.boundary.plot(ax=ax, zorder=2, color='k', linewidth=0.6)
    # legend

    cld = mlines.Line2D([],[],color='red', label='cloud')

    ax.legend(handles=[cld],
                loc='upper center',
                bbox_to_anchor=(0.9,0.25),
                ncol=1,
                fontsize=12,
                frameon=False)
    # export to current working directory
    plt.savefig("scenes_"+year+".png",
                dpi = 500,
                # specifying tight here so that legend is not cut
                bbox_inches= "tight")

    pyplot.show()

for x in yearlist:
    ans.append(brvis(x))
    
show(ans)