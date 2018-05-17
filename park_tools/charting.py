import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

plt.style.use('seaborn-muted')

def ecdf(x,normed=False):

	'''Input array to explore empirical cumulative distribution function (ECDF)

	x: numpy array or pandas Series; required
	normed: boolean; centers mean at 0 and scales data accordingly

	returns: x array (sorted), y array for plotting'''

	if normed:
		x = (x - np.mean(x)) / np.std(x)
	
	y = np.arange(1,len(x)+1) / len(x)

	x = np.sort(x)

	return x,y