#! /usr/bin/python
##############################################################################
'''
Parameters for the speed test :

Sub-population Size	: 			[10, 100, 1000, 5000]
Genome Length	: 				[100, 500, 1000, 2000]
Max. # generations	: 			400
Elitist size	: 				5
Crossover-type	:  				two
Dynamic-mutation-rate : 		[0.05] * (1/Current_Best_Fitness)
Job runs : 						1

- checking evaluation time  and initialisation time
- bar graphs 
'''
##############################################################################

import csv
import sys
from pprint import pprint
import math
import os

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import scipy.stats
from matplotlib.colors import ListedColormap, NoNorm
from matplotlib import mlab
from itertools import cycle # for automatic markers

import matplotlib.cm as cm
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Rectangle


# constants
SEED=92341
JOBS = 1
GENERATIONS = 400

# csv col numbers
CSV_COL_GEN 				= 0
CSV_COL_INIT_TIME 			= 1
CSV_COL_EVAL_TIME 			= 2
CSV_COL_MEAN_FITNESS 		= 3
CSV_COL_BEST_FITNESS 		= 4
CSV_COL_BEST_FITNESS_SOFAR 	= 5

STAT_FOLDER = 'speedtest_output/'

# key investigation params
range_subpop_size 				= [10, 100, 1000, 5000]
range_genome_length 			= [100, 500, 1000, 2000]

PERMUTATIONS = len(range_subpop_size)*len(range_genome_length)

# output file path
def get_file_path(ss, gl):
	fname =	"speedtest_" + \
	"ss"+str(ss)+"_" + \
	"gl"+str(gl) + \
	".out.stat"
		  
	fname = 'speed_stats_output/'+fname	
	return fname

# label for files results (used in legend)
def get_label_name(ss, gl, pn):
	fname =	"ss"+str(ss)+"-" + \
	"gl"+str(gl)
	
	return fname

# ideally 1 file contains data from 1 job run
def get_data_from_file(fname):
	generations = []
	gen_fitnesses = []
	eval_time = []
	init_time = []	
	row_count = 0
		
	try:
		# get data
		with open(fname, 'rb') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=' ')
			for row in spamreader:				
				generations.append(int(row[CSV_COL_GEN]))
				gen_fitnesses.append(int(float(row[CSV_COL_BEST_FITNESS])))
				eval_time.append(int(row[CSV_COL_EVAL_TIME]))
				init_time.append(int(row[CSV_COL_INIT_TIME]))
				
				row_count= row_count+1
		
		result = {
					'generations' 	: generations,
					'gen_fitnesses' : gen_fitnesses,
					'init_time'		: init_time,
					'avg_init_time'	: sum(init_time)/len(init_time),
					'eval_time'		: eval_time,
					'avg_eval_time'	: sum(eval_time)/len(eval_time)
					}
		
		return result			
	
	except Exception:
		print 'WARNING! File: ' + fname + ' - Not found!'		
		# instead of returning None, we'll return an empty list
		# to get rid of any unwanted errors while plotting
		result = {
					'generations' 	: range(0,GENERATIONS),
					'gen_fitnesses' : [0] * GENERATIONS,
					'init_time'		: [0] * GENERATIONS,
					'avg_init_time' : 0,
					'eval_time'		: [0] * GENERATIONS,
					'avg_eval_time'	: 0
					}
		
		return result

# plot average speed results (per permutation)
# average values of all generations
# draw overlapping bar plot
def plot_avg_eval_init_speeds():
	
	permutations = range(0, PERMUTATIONS)	
	
	xlabels = []
	for i in range(0, PERMUTATIONS):
		xlabels.append('P'+str(i))	
	
	avg_eval_time_per_perm = []
	avg_init_time_per_perm = []
	list_of_labels = []
	
	pn = 0
	for param_subpop_size in range_subpop_size:
		for param_genome_length in range_genome_length:
			
			file = get_file_path(param_subpop_size, 
								param_genome_length
								)
			
			print "=========================================="
			print "Accessing : " + file					
			permutation_data = get_data_from_file(file)			
			print "=========================================="			
						
			lbl = get_label_name(param_subpop_size, 
									param_genome_length,
									pn
								)					
			lbl ="P"+str(pn)+" : "+lbl
			avg_eval_time_per_perm.append(permutation_data['avg_eval_time'])
			avg_init_time_per_perm.append(permutation_data['avg_init_time'])
			list_of_labels.append(lbl)
			
			pn+=1	
	
	ind = np.arange(np.size(permutations))
	
	width = 0.35       # the width of the bars: can also be len(x) sequence	
	ax = plt.subplot(111)
	
	ax.set_yscale("log")
	
	plt.xticks(ind+width/2., xlabels )
	p1 = plt.bar(ind, avg_init_time_per_perm,   width, color='r', alpha=0.8)
	
	plt.ylabel("Time (ms)\n(Logarithmic Scale)", multialignment='center',fontsize=18)
	plt.xticks(ind+width/2., xlabels )
	plt.xlabel("Permutations",fontsize=18)	
	p2 = plt.bar(ind, avg_eval_time_per_perm,   width, color='y', bottom=avg_init_time_per_perm, alpha=0.8)
	plt.grid(True)
	
	leg1 = fig.legend([p1,p2], ['Init. time', 'Eval. time'], 'upper center', ncol=2,prop={'size':14})
	leg1.draggable()
	
	perm_labels = '\n'
	for i in range(0, PERMUTATIONS):
		perm_labels = perm_labels + '\n '+ xlabels[i] + ' : ' + list_of_labels[i] + ' '	
	perm_labels = perm_labels+'\n'
	
	box = ax.get_position()
	ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])
	dummyRec= Rectangle((0, 0),0, 0, fc="w", fill=False, edgecolor='none', linewidth=0)
	#leg2 = plt.legend([dummyRec], [perm_labels], 'center left', bbox_to_anchor=(1, 0.5))
	#leg2.draggable()	
	ax.text(1.02, 0.85, perm_labels, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=dict(facecolor='white'))
	
	plt.tick_params(axis='both', which='major', labelsize=16)
	plt.autoscale(enable=True, axis='both', tight=True)
	
	
# plot fitness per generation (per permutation)
def plot_fitness_per_gens():
	
	permutations = range(0, PERMUTATIONS)	
	
	fitness_values = []
	list_of_labels = []
	
	lines = ["-o", "-s", "-D", "-*" ]
	#lines = ["-.", "-x", "-+", "-*" ]
	linecycler = cycle(lines)
	pn = 0
	for param_subpop_size in range_subpop_size:
		for param_genome_length in range_genome_length:
			
			fitness_values = []
			
			file = get_file_path(param_subpop_size, 
								param_genome_length
								)
			
			print "=========================================="
			print "Accessing : " + file					
			permutation_data = get_data_from_file(file)			
			print "=========================================="
									
			lbl = get_label_name(param_subpop_size, 
									param_genome_length,
									pn
								)					

			lbl ="P"+str(pn)+" : "+lbl
			gen_length = range(0,np.size(permutation_data['gen_fitnesses']))			
			gen_length = np.squeeze(np.asarray(gen_length))
			fits = np.squeeze(np.asarray(permutation_data['gen_fitnesses']))			
			
			# red, yellow, gree, blue colours per subpop size group
			if(param_subpop_size==range_subpop_size[0]):
				line_col = 'r'
			elif(param_subpop_size==range_subpop_size[1]):
				line_col = 'g'
			elif(param_subpop_size==range_subpop_size[2]):
				line_col = 'b'
			elif(param_subpop_size==range_subpop_size[3]):
				line_col = 'y'
			
			plt.plot(gen_length, fits, 
								next(linecycler),markevery=10,
								color=line_col,
								label=lbl,alpha=0.8)
			print "----- > Plotting : " + lbl
			plt.hold(True)
			pn+=1
			
			
####################################
#	MAIN
####################################

# init and eval times subplots
fig = plt.figure()
plot_avg_eval_init_speeds()

# fitness values subplots
fig = plt.figure()
ax = plt.subplot(111)
plot_fitness_per_gens()
plt.xlabel('Generations',fontsize=18)
plt.ylabel('Best fitness',fontsize=18)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
leg = plt.legend(loc='center left', bbox_to_anchor=(1, 0.5),prop={'size':16})
leg.draggable()
plt.grid(True)
plt.autoscale(enable=True, axis='both', tight=True)
plt.subplots_adjust(left=0.04, bottom=0.07, right=0.75, top=0.98,
                wspace=0.20, hspace=0.20)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.show()