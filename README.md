# sparklpy

##module to create Tufte-style spark line plots

this is a module (a single function really) that creates a sparkline plot a-la' Tufte.

It eats time series in the form of 2d numpy.ndarrays, or dataframes

You can control a number of settings including the figure layout (number of columns and rows) the colors that mark the minimum and maximum, the label format and size. 

It will temporarely overwrite your rc.param, but no panic: it will reset them to your default before exiting the function.

The resulting plot will look something like this:

![alt text](https://github.com/fedhere/sparklpy/blob/master/sparklines_example.png)
