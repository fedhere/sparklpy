from __future__ import print_function
__author__ = '__fbb__'
#Federica B. Bianco, NYU
#github: @fedhere
#fedhere@gmail.com
#cosmo.nyu.edu/~fb55/
#created: December 2015
#module to plot time series as sparkle lines a' la Tufte.


import numpy as np
import pandas as pd
import matplotlib.pyplot as pl
import matplotlib as mpl
from distutils.version import LooseVersion


#color blindness safe colors
kelly_colors_hex = [
    '#FFB300', # Vivid Yellow
    '#803E75', # Strong Purple
    '#FF6800', # Vivid Orange
    '#A6BDD7', # Very Light Blue
    '#C10020', # Vivid Red
    '#CEA262', # Grayish Yellow
    '#817066', # Medium Gray
    '#007D34', # Vivid Green
    '#F6768E', # Strong Purplish Pink
    '#00538A', # Strong Blue
    '#FF7A5C', # Strong Yellowish Pink
    '#53377A', # Strong Violet
    '#FF8E00', # Vivid Orange Yellow
    '#B32851', # Strong Purplish Red
    '#F4C800', # Vivid Greenish Yellow
    '#7F180D', # Strong Reddish Brown
    '#93AA00', # Vivid Yellowish Green
    '#593315', # Deep Yellowish Brown
    '#F13A13', # Vivid Reddish Orange
    '#232C16', # Dark Olive Green
    ]

axiscycler_key = "axes.color_cycle"
axiscycler = lambda cc : cc
if LooseVersion(mpl.__version__) >= '1.5.0':
    from cycler import cycler
    axiscycler_key =  "axes.prop_cycle"
    axiscycler = lambda cc : (cycler('color',
                                     cc))
#the plots are on every other column of the subplot grid
#(alternate columns reserved for labels)

#the color cycle gets screwes since upgrade to MPL 1.5 and subbing
#'prop_cycle' for 'color_cycle'



newparams = {
    "lines.linewidth": 2.0,
    "axes.edgecolor": "#aaaaaa",
    "patch.linewidth": 1.0,
    "legend.fancybox": 'false',
    "axes.facecolor": "#ffffff",
    "axes.labelsize": "large",
    "axes.grid": 'false',
    "patch.edgecolor": "#555555",
    "axes.titlesize": "x-large",
    "svg.embed_char_paths": "path",
    axiscycler_key: axiscycler(kelly_colors_hex)
}


def sparklme(data, labels = None, datarange = None, rangecol = None, colors = None, figsize = None, figure = None, ncols = None, alpha=0.3, fontsize=15, minmaxformat = '%.1f', xrangeformat = '%.1f', labeloffset = 0, minmaxoffset = 0, flipy = False):
    #flipy is designad for astronomical mags:
    #min is at the top,
    #max at the bottom

    #setting up plotting parameters
    #number of columns in the plotting grid
    if not ncols : ncols = 2

    #plotting color list
    if colors :
        if not isinstance(colors, 
                               (list, tuple, np.ndarray)):
            colors = [colors]
        else: 
            colors = list(colors)
        newcolors = colors + kelly_colors_hex 
        newparams[axiscycler_key] = axiscycler(newcolors)


    #setting up data
    #if it is a DataFrame
    if type(data) ==  pd.core.frame.DataFrame:
        N = len(data.columns)
        if not labels:
            labels = data.columns
        if datarange :
            if (not isinstance(datarange, 
                               (list, tuple, np.ndarray)) 
                or not np.array(datarange).shape == (2,)):
                print ("datarange incorrect")
                x0, x1 = '', ''
            else:
                x0, x1 = datarange
            
        elif rangecol:
            N -= 1
            if rangecol in data.columns:
                print (data[rangecol])
                x0, x1 = data[rangecol].values.min(), \
                       data[rangecol].values.max()
            else:
                print ("rangecol incorrect")
                x0, x1 = '', ''
            data.drop(rangecol, 1, inplace=True)

        else:
            ldf = float(len(data))
            x0, x1 = '0', '%d'%ldf
            xrangeformat = '%d'
        if 'd' in xrangeformat: 
            x0, x1 = int(x0), int(x1)
        if 'f' in xrangeformat: 
            x0, x1 = float(x0), float(x1)
            
        data =data.values.T

    #if it is a np.ndarray
    elif isinstance(data, (list, tuple, np.ndarray)):
        N = data.shape [0]
        Ndp = data.shape[1]

        if not labels :
            labels= [''] * N
        if not datarange or not isinstance(datarange, 
                                           (list, tuple, np.ndarray)):
            x0, x1 = 0, Ndp
            xrangeformat = '%d'
        elif not len(labels) == N:
            print ("length of lables array is incorrect")
            labels= [''] * N
        else:
            x0, x1 = datarange
    else:
        print ("data type not understood")
        return -1


    #saving old rc params and setting new ones
    oldparams = pl.rcParams
    pl.rcParams.update(newparams) 

    nrows = int((N + 2)/ncols)
    if figure:
        fig = figure
        figsize = fig.get_size_inches()
    elif figsize :
        fig = pl.figure(figsize = figsize)
    else: 
        figsize = (10, nrows)
        fig = pl.figure(figsize = figsize)
    
    ax = []
    for i, data in enumerate(data):

        x2 = 0 if i%2 == 0 else 3
        ax.append(pl.subplot2grid((nrows, ncols * 2 + ncols ), 
                                  ((i/2), x2), colspan = 2))
        minhere = np.nanmin(data)
        maxhere = np.nanmax(data)

        ax[i].plot(data, 'k', alpha=alpha)
        ax[i].axis('off')
        ax[i].set_xlim(-len(data)*0.3, len(data)*1.3)
        try:
            bl, = ax[i].plot(np.where(data == minhere)[0], minhere, 'o')
        except ValueError:
            bl, = ax[i].plot(np.where(data == minhere)[0][0], minhere, 'o')

        if 'd' in minmaxformat : minhere = int(minhere)
        if 'f' in minmaxformat : minhere = float(minhere)

        ax[i].text(1.1 - minmaxoffset, 0.5, 
                   minmaxformat%(minhere), fontsize = fontsize, 
                   transform = ax[i].transAxes, ha = 'center',  
                   color=bl.get_color())
        try:
            bl, = ax[i].plot(np.where(data == maxhere)[0], maxhere, 'o')
        except ValueError:
            bl, = ax[i].plot(np.where(data == maxhere)[0][0], maxhere, 'o')
        ax[i].text(1.3 - minmaxoffset, 0.5, 
                   minmaxformat%(maxhere), fontsize = fontsize, 
                   transform = ax[i].transAxes, color=bl.get_color())
        ax[i].text(-0.1 - labeloffset, 0.5, 
                   labels[i], fontsize = fontsize, 
                   transform = ax[i].transAxes)
       
        if flipy:
            ax[i].set_ylim(ax[i].get_ylim()[1],
                           ax[i].get_ylim()[0])

        if i<2:
            ax[i].plot((0,ax[i].get_xlim()[1]), 
                    (ax[i].get_ylim()[1], ax[i].get_ylim()[1]), 'k-',)

    xrangeloc = 1.1
    if flipy : xrangeloc = 0.9
    xr = '{0:'+xrangeformat+'} - {1:'+xrangeformat+'}'
    xr = xr.replace('%','')
    ax[0].text (ax[0].get_xlim()[1]*0.5, ax[0].get_ylim()[1]*xrangeloc, 
                xr.format(x0, x1), ha = 'center',
                transform = ax[0].transData, fontsize = fontsize)
    ax[0].text (1.1 - minmaxoffset, 1.2, 'min',  ha = 'center', 
                transform = ax[0].transAxes, fontsize = fontsize)
    ax[0].text (1.3 - minmaxoffset, 1.2, 'max', 
                transform = ax[0].transAxes, fontsize = fontsize)


    ax[1].text (ax[1].get_xlim()[1]*0.5, ax[1].get_ylim()[1]*xrangeloc, 
                xr.format(x0, x1), ha = 'center',
                transform = ax[1].transData, fontsize = fontsize)
    ax[1].text (1.1 - minmaxoffset, 1.2, 'min', ha = 'center', 
                transform = ax[1].transAxes, fontsize = fontsize)
    ax[1].text (1.3 - minmaxoffset, 1.2, 'max',
                transform = ax[1].transAxes, fontsize = fontsize)
    
    pl.rcParams.update(oldparams)

    return fig



def sparkletest():
    data = np.ones((100,10))
    data = np.random.randn(10,100) +\
           np.cos( (data / (np.pi*10*np.random.rand(10))).T * np.arange(100))

    fig = pl.figure(figsize = (10,5))

    fig = sparklme(data, figure=fig)
    pl.show()
