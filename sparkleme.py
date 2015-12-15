from __future__ import print_function
import numpy as np
import pandas as pd
import matplotlib.pyplot as pl

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

newparams = {
  "lines.linewidth": 2.0,
  "axes.edgecolor": "#aaaaaa",
  "patch.linewidth": 1.0,
  "legend.fancybox": 'false',
  "axes.color_cycle": kelly_colors_hex,
  "axes.facecolor": "#ffffff",
  "axes.labelsize": "large",
  "axes.grid": 'false',
  "patch.edgecolor": "#555555",
  "axes.titlesize": "x-large",
  "svg.embed_char_paths": "path",
}


def sparklme(data, labels = None, datarange = None, rangecol = None, colors = None, figsize = None, axis = None, ncols = None, alpha=0.3, fontsize=15, minmaxformat = '%.1f', xrangeformat = '%.1f', labeloffset = 0, minmaxoffset = 0):

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
        newparams["axes.color_cycle"]= newcolors


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
                y0, y1 = '', ''
            else:
                y0, y1 = datarange
            
        elif rangecol:
            N -= 1
            if rangecol in data.columns:
                y0, y1 = data[rangecol].values.min(), \
                       data[rangecol].values.max()
            else:
                print ("rangecol incorrect")
                y0, y1 = '', ''
            data.drop(rangecol, 1, inplace=True)

        else:
            y0, y1 = '', ''    
        if 'd' in xrangeformat: 
            y0, y1 = int(y0), int(y1)
        if 'f' in xrangeformat: 
            y0, y1 = float(y0), float(y1)
        
        data =data.values.T

    #if it is a np.ndarray
    elif isinstance(data, (list, tuple, np.ndarray)):
        N = len(data) 

        if not labels :
            labels= [''] * N
        if not datarange or not isinstance(datarange, 
                                           (list, tuple, np.ndarray)):
            y0, y1 = 0, N
        elif not len(labels) == N:
            print ("length of lables array is incorrect")
            labels= [''] * N
        else:
            y0, y1 = datarange
    else:
        print ("data type not understood")
        return -1


    #saving old rc params and setting new ones
    oldparams = pl.rcParams
    pl.rcParams.update(newparams) 

    nrows = int((N + 2)/ncols)

    if figsize :
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
            bl, = ax[i].plot(np.where(data == maxhere)[0], maxhere, 'o')
        except ValueError:
            bl, = ax[i].plot(np.where(data == maxhere)[0][0], maxhere, 'o')
        color_cycle = ax[i]._get_lines.color_cycle

        if 'd' in minmaxformat : minhere = int(minhere)
        if 'f' in minmaxformat : minhere = float(minhere)

        ax[i].text(1.1 - minmaxoffset, 0.5, 
                   minmaxformat%(minhere), fontsize = fontsize, 
                   transform = ax[i].transAxes, ha = 'center',  
                   color=bl.get_color())
        try:
            bl, = ax[i].plot(np.where(data == minhere)[0], minhere, 'o')
        except ValueError:
            bl, = ax[i].plot(np.where(data == minhere)[0][0], minhere, 'o')
        ax[i].text(1.3 - minmaxoffset, 0.5, 
                   minmaxformat%(maxhere), fontsize = fontsize, 
                   transform = ax[i].transAxes, color=bl.get_color())
        ax[i].text(-0.1 - labeloffset, 0.5, 
                   labels[i], fontsize = fontsize, 
                   transform = ax[i].transAxes)
       

        if i<2:
            ax[i].plot((0,ax[i].get_xlim()[1]), 
                    (ax[i].get_ylim()[1], ax[i].get_ylim()[1]), 'k-',)

    ax[0].text (ax[0].get_xlim()[1]*0.5, ax[0].get_ylim()[1]*1.1, 
                '{0:1} - {1:2}'.format(y0, y1), ha = 'center',
                transform = ax[0].transData, fontsize = fontsize)
    ax[0].text (1.1 - minmaxoffset, 1.2, 'min', 
                transform = ax[0].transAxes, fontsize = fontsize)
    ax[0].text (1.3 - minmaxoffset, 1.2, 'max', 
                transform = ax[0].transAxes, fontsize = fontsize)
    xr = '{0:'+xrangeformat+'} - {1:'+xrangeformat+'}'
    xr = xr.replace('%','')

    ax[1].text (ax[1].get_xlim()[1]*0.5, ax[1].get_ylim()[1]*1.1, 
                '{0:1} - {1:2}'.format(y0, y1), ha = 'center',
                transform = ax[1].transData, fontsize = fontsize)
    ax[1].text (1.1 - minmaxoffset, 1.2, 'min',
                transform = ax[1].transAxes, fontsize = fontsize)
    ax[1].text (1.3 - minmaxoffset, 1.2, 'max',
                transform = ax[1].transAxes, fontsize = fontsize)
    
    pl.rcParams.update(oldparams)


    return fig
