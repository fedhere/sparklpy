from __future__ import print_function
__author__ = '__fbb__'
#test for sparkleme module
#makes some fake data and plots it as sparkle lines


import numpy as np
from scipy import stats
import matplotlib.pyplot as pl
import sparkleme 

#spark lines a la Tufte, first with synthetic 
#generating data: noisy random sine waves
data = np.ones((100,10))
data = np.random.randn(10,100) +\
       np.cos( (data / (np.pi*10*np.random.rand(10))).T * np.arange(100))

fig = pl.figure(figsize = (10,5))

sparkleme.sparklme(data, figure=fig)
pl.show()

