#! /usr/bin/python

##############################################################################
'''
Best permutation of fixed, dynamic mutation schemes - comparison
Parameters in the  fixed vs. dynamic test will involve :

Sub-population Size 				: fixed:  4000
Genome-length 						: fixed:  2000
Cossover-type						: two
Fixed Mutation-probability			: 0.002
Dynamic-mutation rate				: 0.05 *  (1/Current_Best_Fitness)
Fixed-Mut Elitist size				: 10
Dyn-Mut Elitist size				: 5 
Max. # generations					: fixed: 400
Job runs per combination			: 30 

Stats to show :
- obtain results from specified folder (csv files)
- Mean/Best fitness vs. generations

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

# constants
SEED=92341
JOBS = 30
GENERATIONS = 400

CSV_COL_GEN 				= 0
CSV_COL_INIT_TIME 			= 1
CSV_COL_EVAL_TIME 			= 2
CSV_COL_MEAN_FITNESS 		= 3
CSV_COL_BEST_FITNESS 		= 4
CSV_COL_BEST_FITNESS_SOFAR 	= 5

# params
range_subpop_size 				= [3000]
range_genome_length 			= [2000]
range_crossover_type			= ['two']
fixed_mut_range_elitist_number	= [10]
dyn_mut_range_elitist_number	= [5]

# key investigation params
range_fixed_mutation_rate		= [0.002]
range_dynamic_mutation_rate		= [0.05]	

# output file path
def get_file_path(ss, gl, ct, eln, mut_type, mut_rate, j):
	fname =	"mut-"+ mut_type + str(mut_rate) + "_" + \
	"ss"+str(ss)+"_" + \
	"gl"+str(gl)+"_" + \
	"ct-"+ct+"_" + \
	 "eln"+str(eln)+"_" + \
	 "job."+str(j)+".out.stat"
		  
	fname = 'f_vs_d_stat_out/'+fname
	
	return fname

# label for files results (used in legend)
def get_label_name(ss, gl, ct, eln, mut_type, mut_rate):
	fname =	"mut-"+ mut_type + str(mut_rate) + "_" + \
	"ss"+str(ss)+"_" + \
	"gl"+str(gl)+"_" + \
	"ct-"+ct+"_" + \
	 "eln"+str(eln)
	
	return fname


# ideally 1 file contains data from 1 job run
def get_data_from_file(fname):
	generations = []
	gen_fitnesses = []
		
	try:
		# get data
		with open(fname, 'rb') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=' ')
			for row in spamreader:			
				generations.append(int(row[CSV_COL_GEN]))
				gen_fitnesses.append(int(float(row[CSV_COL_BEST_FITNESS])))
		
		result = {
					'generations' 	: generations,
					'gen_fitnesses' : gen_fitnesses			
					}		
		return result			
	
	except Exception:
		print 'WARNING! File: ' + fname + ' - Not found!'
		
		# instead of returning None, we'll return an empty list
		# to get rid of any unwanted errors while plotting
		result = {
					'generations' 	: range(0,GENERATIONS),
					'gen_fitnesses' : [0] * GENERATIONS			
					}		
		return result

# get mean values from all the jobs - mean value per generation			
def get_mean_values_from_all_jobs(data_from_all_jobs):	
	
	#result = {}
	generations = range(0, GENERATIONS)
	gen_fitnesses = []	
	matrix_fit_sums = np.zeros([1, GENERATIONS])
	
	count=0
	for each_item in data_from_all_jobs:		
		try:
			#pprint(each_item)
			
			matrix_fit_sums_t = np.matrix(each_item['data']['gen_fitnesses'])
			matrix_fit_sums = matrix_fit_sums + matrix_fit_sums_t
			count = count+1
		except Exception as e:
			pprint(each_item)
			print e.value
		
	matrix_fit_avg = matrix_fit_sums/count		
	
	result = {
				'avg_fitnesses' : matrix_fit_avg
			}	
			
	return result

# get best values from all the jobs - compare only the final generation
def get_best_job_from_all_jobs(data_from_all_jobs):
	
	ix_of_best_job = 0
	best_fitness_of_last_gen = 0
	
	ix_temp = 0
	
	print "get_best_job_from_all_jobs:: len=" + str(len(data_from_all_jobs)) 
	
	for each_item in data_from_all_jobs:
		
		print "get_best_job_from_all_jobs:: last gen fitness ( " +  str(ix_temp) + ")=" + str(each_item['data']['gen_fitnesses'][GENERATIONS-1])
		
		job_gen_size = len(each_item['data']['gen_fitnesses'])
		
		if(each_item['data']['gen_fitnesses'][job_gen_size-1] > best_fitness_of_last_gen):
			best_fitness_of_last_gen = each_item['data']['gen_fitnesses'][job_gen_size-1]
			ix_of_best_job = ix_temp
		
		ix_temp = ix_temp + 1
	
	result = {
				'best_fitnesses' : data_from_all_jobs[ix_of_best_job]['data']['gen_fitnesses']
			}
	
	print "get_best_job_from_all_jobs:: best job is : "+ str(ix_of_best_job)
	
	return result	
	
#### Dynamic Mutation rate experiment ####
def print_results_ffd_for_dynamic_mutrate(param_dynamic_mut_rate):
	
	data_from_all_jobs = []
	ret_lbls = []
	for param_subpop_size in range_subpop_size:
		for param_genome_length in range_genome_length:
			for param_crossover_type in range_crossover_type:
				for param_elitist_number in dyn_mut_range_elitist_number:
					
					Thread_SEED=92341
					data_from_all_jobs = []
					# run multiple jobs per permutation
					for j in range(0, JOBS):
						
						print "=========================================="											
						file = get_file_path(param_subpop_size, 
											param_genome_length, 
											param_crossover_type, 
											param_elitist_number,
											'DYNAMIC',
											param_dynamic_mut_rate,
											j)
						
						print "Accessing : " + file
						
						file_data = get_data_from_file(file)						
						
						# summarise all data from the job	
						temp_data_from_all_jobs = {
												'job_name' : file,
												'data'     : file_data
											}
						
						data_from_all_jobs.append(temp_data_from_all_jobs)							
						print "=========================================="
						
					##############################
					##### PLOT BEST RESULT #######
					##############################					
					fitnesses_for_curr_perm = get_best_job_from_all_jobs(data_from_all_jobs)					
					
					lbl = "DYN_MUTATION_BEST_FITNESS"		
					ret_lbls.append(lbl)			
					
					dim = np.size(fitnesses_for_curr_perm['best_fitnesses'])
					#gen_length = np.linspace(1,dim, dim)
					gen_length = range(0,dim)						
					gen_length = np.squeeze(np.asarray(gen_length))
					fits = np.squeeze(np.asarray(fitnesses_for_curr_perm['best_fitnesses']))					
									
					mut_colour = 'blue'
										
					ax.plot(gen_length, fits, 
							"-+",
							markevery=10,							
							color=mut_colour,
							label=lbl)
					print "----- > Plotting : " + lbl
					plt.hold(True)						
					
					##############################	
					##### PLOT AVERAGE RESULT ####
					##############################	
					fitnesses_for_curr_perm = get_mean_values_from_all_jobs(data_from_all_jobs)
					
					lbl = "DYN_MUTATION_AVG_FITNESS"		
					ret_lbls.append(lbl)				
					
					dim = np.size(fitnesses_for_curr_perm['avg_fitnesses'])
					#gen_length = np.linspace(1,dim, dim)
					gen_length = range(0,dim)						
					gen_length = np.squeeze(np.asarray(gen_length))
					fits = np.squeeze(np.asarray(fitnesses_for_curr_perm['avg_fitnesses']))					
					
					mut_colour = 'blue'
										
					ax.plot(gen_length, fits, 
							"-o",
							markevery=10,							
							color=mut_colour,
							label=lbl)
					print "----- > Plotting : " + lbl
					plt.hold(True)	
	
	return ret_lbls



#### Fixed Mutation rate experiment ####
def print_results_ffd_for_fixed_mutrate(param_fixed_mut_rate):
	
	generations = range(0, JOBS)
	data_from_all_jobs = []
	ret_lbls = []
	
	for param_subpop_size in range_subpop_size:
		for param_genome_length in range_genome_length:
			for param_crossover_type in range_crossover_type:
				for param_elitist_number in fixed_mut_range_elitist_number:
					
					# run multiple jobs per permutation
					for j in range(0, JOBS):
						
						print "=========================================="											
						file = get_file_path(param_subpop_size, 
											param_genome_length, 
											param_crossover_type, 
											param_elitist_number,
											'FIXED',
											param_fixed_mut_rate,
											j)
						print "Accessing : " + file
						
						file_data = get_data_from_file(file)						
						
						# summarise all data from the job	
						temp_data_from_all_jobs = {
												'job_name' : file,
												'data'     : file_data
											}
						
						data_from_all_jobs.append(temp_data_from_all_jobs)							
						print "=========================================="
						
					##############################
					##### PLOT BEST RESULT #######
					##############################					
					fitnesses_for_curr_perm = get_best_job_from_all_jobs(data_from_all_jobs)					
					
					lbl = "FIXED_MUTATION_BEST_FITNESS"		
					ret_lbls.append(lbl)			
					
					dim = np.size(fitnesses_for_curr_perm['best_fitnesses'])
					#gen_length = np.linspace(1,dim, dim)
					gen_length = range(0,dim)						
					gen_length = np.squeeze(np.asarray(gen_length))
					fits = np.squeeze(np.asarray(fitnesses_for_curr_perm['best_fitnesses']))					
					
					#pprint(gen_length)
					#pprint(fits)						
					
					mut_colour = 'red'
										
					ax.plot(gen_length, fits, 
							"-+",
							markevery=10,							
							color=mut_colour,
							label=lbl)
					print "----- > Plotting : " + lbl
					plt.hold(True)	
										
					##############################	
					##### PLOT AVERAGE RESULT ####
					##############################	
					fitnesses_for_curr_perm = get_mean_values_from_all_jobs(data_from_all_jobs)
					
					lbl = "FIXED_MUTATION_AVG_FITNESS"		
					ret_lbls.append(lbl)				
					
					dim = np.size(fitnesses_for_curr_perm['avg_fitnesses'])
					#gen_length = np.linspace(1,dim, dim)
					gen_length = range(0,dim)						
					gen_length = np.squeeze(np.asarray(gen_length))
					fits = np.squeeze(np.asarray(fitnesses_for_curr_perm['avg_fitnesses']))
					
					mut_colour = 'red'
										
					ax.plot(gen_length, fits, 
							"-o",
							markevery=10,							
							color=mut_colour,
							label=lbl)
					print "----- > Plotting : " + lbl
					plt.hold(True)	
	
	return ret_lbls

####################################
#	MAIN
####################################
fig = plt.figure()
fig.canvas.set_window_title('Fixed vs. Dynamic Mutation rates')

## Dynamic Mutation Rates ##
ax = plt.subplot(111)
lbl_fixed = print_results_ffd_for_dynamic_mutrate(range_dynamic_mutation_rate[0])
				
## Fixed Mutation Rates ##
lbl_dyn = print_results_ffd_for_fixed_mutrate(range_fixed_mutation_rate[0])

## figure specs
plt.xlabel('Generations',fontsize=18)
plt.ylabel('Fitness',fontsize=18)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
leg = plt.legend(loc='center left', bbox_to_anchor=(1, 0.5),prop={'size':14},ncol=2)
leg.draggable()
plt.grid(True)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.autoscale(enable=True, axis='both', tight=True)
plt.subplots_adjust(left=0.04, bottom=0.07, right=0.75, top=0.98,
                wspace=0.20, hspace=0.20)			
				
plt.show()
