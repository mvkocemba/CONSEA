#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 13:33:49 2023

@author: michele
"""


import geopandas as gpd
import pandas as pd
import numpy as np
import os

import matplotlib.pyplot as plt
from matplotlib import pyplot
from matplotlib import colors
import rasterio
import seaborn as sns
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



distlist = ["Bududa", "Bukwo", "Bulambuli", "Kapchorwa", "Kween", "Manafwa", "Mbale", "Namisindwa", "Sironko"]
ans = []

import matplotlib.pylab as pylab

def periodvis(district):
    sns.set_theme()
    # load vector data
    #districts
    distshp = "/home/michele/programming/python/data/CDAdistricts/districtselgon.shp"
    dshp = gpd.read_file(distshp)
    dshp['name'] = ['Namisindwa','Manafwa', 'Bududa','Mbale','Sironko','Bulambuli','Kapchorwa','Kween','Bukwo','Bududa', 'Bukwo', 'Bulambuli','Kapchorwa','Kween', 'Manafwa', 'Mbale', 'Namisindwa','Sironko']
    
    global selection
    selection = dshp[dshp['name'] == district]
    
    ### load in vector data ###
    # load BR data
    BR = "MtElgonBRUgandaOutline.shp"
    BR = gpd.read_file(BR)
    
    # load transition
    transition = "transitionzone.shp"
    transition = gpd.read_file(transition)
    
    # load buffer
    buffer = "bufferzone.shp"
    buffer = gpd.read_file(buffer)
    
    # load core
    core = "core.shp"
    core = gpd.read_file(core)
    
    ### load other raster data ###
    # load hillshade
    hillshade = inputdir + "/hillshade.tif"
    hillshade = rasterio.open(hillshade)
    
    
    # creation of a custom colormap
    # values
    levels = [0,1,2,3]
    # 1 = NF >> NF
    # 2 = NF > F
    # 3 = F > NF
    # 4 = F > F
    clrs = ['#eed5b7', 'yellowgreen', '#CD5555', 'darkolivegreen']
    
    cmap, norm = colors.from_levels_and_colors(levels, clrs, extend='max')
    
    distlist = ["Bududa", "Bukwo", "Bulambuli", "Kapchorwa", "Kween", "Manafwa", "Mbale", "Namisindwa", "Sironko"]
    ans = []

    p1 = inputdir + "/Combination [1973 "+district+" - 1987 "+district+"].tif"
    p2 = inputdir + "/Combination [1987 "+district+" - 1995 "+district+"].tif"
    p3 = inputdir + "/Combination [1995 "+district+" - 2003 "+district+"].tif"
    p4 = inputdir + "/Combination [2003 "+district+" - 2014 "+district+"].tif"
    p5 = inputdir + "/Combination [2014 "+district+" - 2021 "+district+"].tif"

    raster_p1 = rasterio.open(p1)
    raster_p2 = rasterio.open(p2)
    raster_p3 = rasterio.open(p3)
    raster_p4 = rasterio.open(p4)
    raster_p5 = rasterio.open(p5)
    
    #distplot = dshp[(dshp.Source==district)]
    
    fig, ((axp1, axp2, axp3), (axp4, axp5, axmm)) = pyplot.subplots(ncols=3,
                                                                    nrows=2,
                                                                    figsize=(20,12))
    fig.suptitle(district+' District Forest Cover Development between 1973-2021', fontsize=20)
    fig.subplots_adjust(top=0.88)

    # set one aspect for all subplots
    # this one here ensures that we have the same 'frame' for the plots 
    selection.total_bounds
    xlim=([selection.total_bounds[0], selection.total_bounds[2]])
    ylim=([selection.total_bounds[1], selection.total_bounds[3]])
    
    axp1.set_box_aspect(1)
    axp2.set_box_aspect(1)
    axp3.set_box_aspect(1)
    axp4.set_box_aspect(1)
    axp5.set_box_aspect(1)
    axmm.set_box_aspect(1) 
    
    # set labelsize
    axp1.tick_params(axis='both', which='major', labelsize=7)
    axp1.set_xlim(xlim)
    axp1.set_ylim(ylim)
    
    axp2.tick_params(axis='both', which='major', labelsize=7)
    axp2.set_xlim(xlim)
    axp2.set_ylim(ylim)
    
    axp3.tick_params(axis='both', which='major', labelsize=7)
    axp3.set_xlim(xlim)
    axp3.set_ylim(ylim)
    
    axp4.tick_params(axis='both', which='major', labelsize=7)
    axp4.set_xlim(xlim)
    axp4.set_ylim(ylim)
    
    axp5.tick_params(axis='both', which='major', labelsize=7)
    axp5.set_xlim(xlim)
    axp5.set_ylim(ylim)
    
    axmm.tick_params(axis='both', which='major', labelsize=7)

    
    show((raster_p1), ax=axp1, title='1973-1987', cmap = cmap, norm=norm, interpolation = 'bilinear')
    show((raster_p2), ax=axp2, title='1987-1995', cmap = cmap, norm=norm, interpolation = 'bilinear')
    show((raster_p3), ax=axp3, title='1995-2003', cmap = cmap, norm=norm, interpolation = 'bilinear')
    show((raster_p4), ax=axp4, title='2003-2014', cmap = cmap, norm=norm, interpolation = 'bilinear')
    show((raster_p5), ax=axp5, title='2014-2021', cmap = cmap, norm=norm, interpolation = 'bilinear')
    dshp.boundary.plot(ax=axmm, zorder=2, color='k', linewidth=0.2)
    dshp.boundary.plot(ax=axp1, zorder=2, color='k', linewidth=0.2)
    dshp.boundary.plot(ax=axp2, zorder=2, color='k', linewidth=0.2)
    dshp.boundary.plot(ax=axp3, zorder=2, color='k', linewidth=0.2)
    dshp.boundary.plot(ax=axp4, zorder=2, color='k', linewidth=0.2)
    dshp.boundary.plot(ax=axp5, zorder=2, color='k', linewidth=0.2)
    show((hillshade),ax=axp1, cmap='Greys', zorder=1, alpha=.2)
    show((hillshade),ax=axp2, cmap='Greys', zorder=1, alpha=.2)
    show((hillshade),ax=axp3, cmap='Greys', zorder=1, alpha=.2)
    show((hillshade),ax=axp4, cmap='Greys', zorder=1, alpha=.2)
    show((hillshade),ax=axp5, cmap='Greys', zorder=1, alpha=.2)
    show((hillshade),ax=axmm, cmap='Greys', zorder=1, alpha=.2)
    
    selection.plot(ax=axmm, zorder=2, color='none', edgecolor='red', linewidth=.2)
    #place legend
    transition.plot(ax=axmm, zorder=1, facecolor='#EBFF93', linewidth=0.0)
    buffer.plot(ax=axmm, facecolor='#B5CF43',linewidth=0.0)
    core.plot(ax=axmm, facecolor='darkolivegreen',linewidth=0.0)

    # BR legend
    transitionp = mpatches.Patch(color='#EBFF93', label='transition zone')
    
    bufferp = mpatches.Patch(color='#B5CF43', label='buffer zone')
    
    corep = mpatches.Patch(color='darkolivegreen', label='core zone')
    
    dd = mlines.Line2D([],[],color='red', label='district')
    
    axmm.legend(handles=[transitionp, bufferp, corep, dd],
                loc='lower right',
                #bbox_to_anchor=(1.75,1.21),
                ncol=1,
                fontsize=10,
                frameon=False)

    
    yellow_patch = mpatches.Patch(color='#eed5b7', label='NF >> NF')
    
    red_patch = mpatches.Patch(color='#CD5555', label='F >> NF')
    
    green_patch = mpatches.Patch(color='yellowgreen', label='NF >> F')
    
    lightgreen_patch = mpatches.Patch(color='darkolivegreen', label='F >> F')
    
    labelpatch = mpatches.Patch(color='white', label='(F = forest, NF = non-forest)')
    
    axp1.legend(handles=[yellow_patch, red_patch, green_patch, lightgreen_patch],
                loc='upper center',
                bbox_to_anchor=(1.77,1.23),
                ncol=4,
                fontsize=14,
                frameon=False)
    
    axp2.legend(handles=[labelpatch],
                loc='upper center',
                bbox_to_anchor=(0.45,1.15),
                ncol=1,
                fontsize=12,
                frameon=False)
    
    # insert scalebar
    scalebar = AnchoredSizeBar(axp1.transData,
                               5000, '5km', 'lower right',
                               pad=0.1,
                               color='black',
                               frameon=False,
                               size_vertical=1)
    
    # insert scalebar
    scalebar2 = AnchoredSizeBar(axp1.transData,
                               5000, '5km', 'lower right',
                               pad=0.1,
                               color='black',
                               frameon=False,
                               size_vertical=1)
    
    # insert scalebar
    scalebar3 = AnchoredSizeBar(axp1.transData,
                               5000, '5km', 'lower right',
                               pad=0.1,
                               color='black',
                               frameon=False,
                               size_vertical=1)
    
    # insert scalebar
    scalebar4 = AnchoredSizeBar(axp1.transData,
                               5000, '5km', 'lower right',
                               pad=0.1,
                               color='black',
                               frameon=False,
                               size_vertical=1)
    
    # insert scalebar
    scalebar5 = AnchoredSizeBar(axp1.transData,
                               5000, '5km', 'lower right',
                               pad=0.1,
                               color='black',
                               frameon=False,
                               size_vertical=1)
    
    

    axp1.add_artist(scalebar)
    axp2.add_artist(scalebar2)
    axp3.add_artist(scalebar3)
    axp4.add_artist(scalebar4)
    axp5.add_artist(scalebar5)
    
    
    # export to current working directory
    plt.savefig("testFCdev"+district+".png",
                dpi = 500,
                # specifying tight here so that legend is not cut
                bbox_inches= "tight")
    
    pyplot.show()


#periodvis('Kween')
# carry out the function for the distlist

for x in distlist:
    ans.append(periodvis(x))
    
#show(ans)


