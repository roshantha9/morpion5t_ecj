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
Fixed-Mut Elitist size				: 
Max. # generations					: fixed: 400
Job runs per combination			: 30 

Stats to show :
- box and whisker plots - for each generation 
- for both fixed + dynamic schemes on same plot
- statistical significance results :
(Mann-whitney U (p-val) , Wilcoxon signed-rank (p-val) , Effect size, Kirmogorov smirnoff
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

range_subpop_size 				= [3000]
range_genome_length 			= [2000]
range_crossover_type			= ['two']
fixed_mut_range_elitist_number	= [10]
dyn_mut_range_elitist_number	= [5]


# key investigation params
range_fixed_mutation_rate		= [0.002]
range_dynamic_mutation_rate		= [0.05]	

# plot step size (no room to plot all !
STEP = 20

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
	
	
#### Dynamic Mutation rate experiment ####
def get_results_ffd_for_dynamic_mutrate(param_dynamic_mut_rate):
	
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
	
	return data_from_all_jobs


#### Fixed Mutation rate experiment ####
def get_results_ffd_for_fixed_mutrate(param_fixed_mut_rate):
	
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
	
	return data_from_all_jobs
						
					
# mutation distributions (per generation)
def get_mut_distributions(data_from_all_jobs):
	dist_per_gen = []
	gen_list = []

	## initialise
	for i in range(0,GENERATIONS/STEP):
		dist_per_gen.append([])
	
	# initialise generations label list
	for i in range(STEP,GENERATIONS+STEP, STEP):
		gen_list.append(str(i))
	
	for each_job in data_from_all_jobs:		
		g=0
		ix=0
		for each_gen in range(0,GENERATIONS):			
			if((g % STEP) == 0):
				dist_per_gen[ix].append(each_job['data']['gen_fitnesses'][each_gen])				
				ix=ix+1
			g=g+1
	
	result = {
				'dist_per_gen' : dist_per_gen,
				'labels' : gen_list 
			}
	
	return result

# statistical significance testing
# tabular format
def stat_significance_tests(dyn_results, fixed_results):
	
	print "stat_significance_tests"
	print "========================"
	print "Generation , Mann-whitney U (p-val) , Wilcoxon signed-rank (p-val) , Effect size , median diff , ks_val , comment"	
	
	gen = 0
	for dyn_each_gen, fix_each_gen in zip(dyn_results, fixed_results):
		# comparing averages #
		EffectSize =  abs(np.mean(dyn_each_gen) - np.mean(fix_each_gen))
		
		# test for significance #
		if(np.median(dyn_each_gen) != np.median(fix_each_gen)):
			median_diff = ', -- medians diff --'
		else:
			median_diff = ", -- medians same --"
		
		MannWhitneyU_pval =  round(scipy.stats.mannwhitneyu(np.array(dyn_each_gen), np.array(fix_each_gen))[1],3)
		WilcoxonSignedRank_pval = round(scipy.stats.wilcoxon(np.array(dyn_each_gen), np.array(fix_each_gen))[1],3)
		ks_2samp_pval = round(scipy.stats.ks_2samp(np.array(dyn_each_gen), np.array(fix_each_gen))[1],3)
		
		comment = ',  -- distributions significantly differ' if (WilcoxonSignedRank_pval<0.05) else "" +  ', -- distributions are same'
		
		print str(gen) + ",\t" +  str(MannWhitneyU_pval) + ",\t" + str(WilcoxonSignedRank_pval) + ",\t" + str(EffectSize) + ",\t" + (median_diff) + "\t,"+str(ks_2samp_pval)+comment
		gen=gen+1


####################################
#	MAIN
####################################

fig = plt.figure()
fig.canvas.set_window_title('Fixed vs. Dynamic Mutation rates box plots')
ax = plt.subplot(111)

## Dynamic Mutation Rates ##
dyn_results = get_results_ffd_for_dynamic_mutrate(range_dynamic_mutation_rate[0])
dyn_results = get_mut_distributions(dyn_results)	

## Fixed Mutation Rates ##
fixed_results = get_results_ffd_for_fixed_mutrate(range_fixed_mutation_rate[0])
fixed_results = get_mut_distributions(fixed_results)	

boxpos_dyn=range(1,len(dyn_results['dist_per_gen'])*2,2)
boxpos_fixed=range(2,(len(dyn_results['dist_per_gen'])*2)+2,2)

# plot box plots
bp=plt.boxplot(dyn_results['dist_per_gen'], whis=1, positions=boxpos_dyn)
plt.setp(bp['boxes'], color='blue', linewidth=1)
plt.setp(bp['caps'], color='blue')
plt.setp(bp['whiskers'], color='blue')
plt.setp(bp['fliers'], color='blue')
plt.setp(bp['medians'], color='blue')

bp=plt.boxplot(fixed_results['dist_per_gen'], whis=1, positions=boxpos_fixed)
plt.setp(bp['boxes'], color='red', linewidth=1)
plt.setp(bp['caps'], color='red')
plt.setp(bp['whiskers'], color='red')
plt.setp(bp['fliers'], color='red')
plt.setp(bp['medians'], color='red')

## figure specs
plt.xlabel('Generations',fontsize=18)
plt.ylabel('Fitness',fontsize=18)
#plt.setxticks(range(1,len(dyn_results['labels'])+1), dyn_results['labels'])
ax.set_xticklabels(dyn_results['labels'])

xticks = range(1,(len(dyn_results['labels'])*2),2)
xticks = [x+0.5 for x in xticks]

ax.set_xticks(xticks)
plt.xlim(0,(len(dyn_results['labels'])*2)+1)
plt.ylim(2,52)
ax.yaxis.grid(True)
plt.tick_params(axis='both', which='major', labelsize=16)

hB, = plt.plot([1,1],'b-')
hR, = plt.plot([1,1],'r-')
leg = plt.legend((hB, hR),('Dynamic mutation-rate', 'Fixed mutation-rate'))
leg.draggable()
hB.set_visible(False)
hR.set_visible(False)

## print stat-significance testing results ##
stat_significance_tests(fixed_results['dist_per_gen'], dyn_results['dist_per_gen'])

plt.show()
