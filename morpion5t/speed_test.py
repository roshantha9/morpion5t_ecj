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
'''
##############################################################################

import os
import thread

SEED=92341
JOBS = 1

# key investigation params
range_subpop_size 				= [10, 100, 1000, 5000]
range_genome_length 			= [100, 500, 1000, 2000]

# get the output file path for a given permutation
def get_file_path(ss, gl):
	fname =	"speedtest_" + \
	"ss"+str(ss)+"_" + \
	"gl"+str(gl) + \
	".out.stat"
		  
	fname = 'speed_stats_output/'+fname
	
	return fname


#### Speed test experiment ####
def run_speed_test():
	for param_subpop_size in range_subpop_size:
		for param_genome_length in range_genome_length:
								
			#Thread_SEED=92341
			# run multiple jobs per permutation					
				
			print "=========================================="
			print "param_subpop_size :: "+ str(param_subpop_size)
			print "param_genome_length :: "+ str(param_genome_length)
			print "=========================================="

			file = get_file_path(param_subpop_size, 
								param_genome_length
								)

			cmd_string = "java ec.Evolve -file morpion5t_speedtest.params" + \
						" -p pop.subpop.0.size="+ str(param_subpop_size) + \
						" -p pop.subpop.0.species.genome-size="+ str(param_genome_length) + \
						" -p stat.file="+file

			os.system(cmd_string)


# Create two threads as follows
try:
	run_speed_test()  
  
except Exception, e:
	print "Error: unable to start : "+str(e) 

while 1:
	pass
