# sparklpy

[![DOI](https://zenodo.org/badge/10115/fedhere/sparklpy.svg)](https://zenodo.org/badge/latestdoi/10115/fedhere/sparklpy)


##module to create Tufte-style spark line plots

(acknowledgement - the author thaks MTA for their service: this code was written almost entirely during NYC subway trips)


this is a pure module (a single .py and a single function really) that creates a sparkline plot a-la' Tufte.

It eats time series in the form of 2d numpy.ndarrays, or dataframes

You can control a number of settings including the figure layout (number of columns and rows) the colors that mark the minimum and maximum, the label format and size. 

It will temporarely overwrite your rc.param, but no panic: it will reset them to your default before exiting the function.

The resulting plot will look something like this:

![alt text](https://github.com/fedhere/sparklpy/blob/master/sparklines_example.png)


The upon calling it, with argument a nd.numpy array (shape = (n_observations, n_timestamps) or a dataframe (all columns must be nuerical values) the function returns a pylab figure object, which you can display (pl.show() ) or save (pl.savefig() ).

install the package "sparkleme" as

`python setup.py install `.

or just save the sparkleme directory somwhere in your python path and call the module sparkleme.
Either way import as

`import sparkleme `

and call, for example,  as  

```

fig = sparkleme.sparkleme(data)

fig.show()

```

To test that the module works run 

`sparkleme.sparkletest()`

or you can use the sparkletest.ipynb Jupyter notebook.

