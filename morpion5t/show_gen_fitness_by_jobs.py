import csv
import sys
from pprint import pprint
import math

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import scipy.stats
from matplotlib.colors import ListedColormap, NoNorm
from matplotlib import mlab
from itertools import cycle # for automatic markers

import time
from itertools import cycle # for automatic markers

import matplotlib.cm as cm
from matplotlib.font_manager import FontProperties

COL_GEN = 0
COL_BEST_FIT = 2

jobs = 21	# eg: job.1.out
colors = iter(cm.rainbow(np.linspace(0, 1, jobs)))

# show plot
plt.close('all')

fig = plt.figure(0)
fig.canvas.set_window_title("Best fitness per generation") 


lines = ["-*","-.","-o","-x","-H","-+"]
linecycler = cycle(lines)

for j in range(1,jobs):
	fname = "job."+str(j)+".out.stat"
	generations = []
	gen_fitnesses = []
	
	print "Plotting - "+fname
	
	# get data
	with open(fname, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=' ')
		for row in spamreader:
			#print row[COL_GEN]
			#print row[COL_BEST_FIT]
			
			
			generations.append(int(row[COL_GEN]))
			gen_fitnesses.append(int(float(row[COL_BEST_FIT])))			

	plt.plot(generations, gen_fitnesses, next(linecycler),color=next(colors), label='el_r='+str(0.01+(j * 0.0495)))
	plt.hold(True)
	
plt.xlabel('Generations')
plt.ylabel('Best-fitness')

fontP = FontProperties()
fontP.set_size('small')
plt.legend(loc='center left', bbox_to_anchor=(0.5, 0.5))    
#plt.legend()

plt.grid()

plt.show()
    