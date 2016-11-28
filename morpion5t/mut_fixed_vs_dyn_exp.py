#! /usr/bin/python

##############################################################################
'''
Parameters in the  fixed vs. dynamic test will involve :

Sub-population Size 				: fixed:  4000
Genome-length 						: fixed:  2000
Cossover-type						: two
Fixed Mutation-probability			: 0.002
Dynamic-mutation rate				: 0.05 *  (1/Current_Best_Fitness)
Fixed-Mut Elitist size				: 
Max. # generations					: fixed: 400
Job runs per combination			: 30 

'''
##############################################################################

import os
import thread

SEED=92341
JOBS = 30

range_subpop_size 				= [3000]
range_genome_length 			= [2000]
range_crossover_type			= ['two']
fixed_mut_range_elitist_number	= [10]
dyn_mut_range_elitist_number	= [5]

# key investigation params
range_fixed_mutation_rate		= [0.002]
range_dynamic_mutation_rate		= [0.05]	# these are the initial mut_rates, they will decrease dynamically

# get the output file path for a given permutation
def get_file_path(ss, gl, ct, eln, mut_type, mut_rate, j):
	fname =	"mut-"+ mut_type + str(mut_rate) + "_" + \
	"ss"+str(ss)+"_" + \
	"gl"+str(gl)+"_" + \
	"ct-"+ct+"_" + \
	 "eln"+str(eln)+"_" + \
	 "job."+str(j)+".out.stat"
		  
	fname = 'f_vs_d_stat_out/'+fname
	
	return fname


#### Dynamic Mutation rate experiment ####
def run_ffd_for_dynamic_mutrate(param_dynamic_mut_rate):
	for param_subpop_size in range_subpop_size:
		for param_genome_length in range_genome_length:
			for param_crossover_type in range_crossover_type:
				for param_elitist_number in dyn_mut_range_elitist_number:
					
					Thread_SEED=92341
					# run multiple jobs per permutation
					for j in range(0, JOBS):
						
						print "=========================================="
						print "Job - "+str(j)
						print "param_subpop_size :: "+ str(param_subpop_size)
						print "param_genome_length :: "+ str(param_genome_length)
						print "param_crossover_type :: "+ param_crossover_type
						print "param_elitist_number :: "+ str(param_elitist_number)					
						print "=========================================="
						
						file = get_file_path(param_subpop_size, 
											param_genome_length, 
											param_crossover_type, 
											param_elitist_number,
											'DYNAMIC',
											param_dynamic_mut_rate,
											j)
						
						cmd_string = "java ec.Evolve -file morpion5t_v3.params" + \
									" -p pop.subpop.0.size="+ str(param_subpop_size) + \
									" -p pop.subpop.0.species.genome-size="+ str(param_genome_length) + \
									" -p pop.subpop.0.species.crossover-type="+ param_crossover_type + \
									" -p breed.elite.0="+ str(param_elitist_number) + \
									" -p pop.subpop.0.species.mutation-prob="+str(param_dynamic_mut_rate) + \
									" -p seed.0="+str(Thread_SEED+1000) + \
									" -p seed.1="+str(Thread_SEED+2000) + \
									" -p seed.2="+str(Thread_SEED+3000) + \
									" -p seed.3="+str(Thread_SEED+4000) + \
									" -p seed.4="+str(Thread_SEED+5000) + \
									" -p seed.5="+str(Thread_SEED+6000) + \
									" -p seed.6="+str(Thread_SEED+7000) + \
									" -p seed.7="+str(Thread_SEED+8000) + \
									" -p seed.8="+str(Thread_SEED+9000) + \
									" -p seed.9="+str(Thread_SEED+10000) + \
									" -p seed.10="+str(Thread_SEED+11000) + \
									" -p seed.11="+str(Thread_SEED+12000) + \
									" -p seed.12="+str(Thread_SEED+13000) + \
									" -p seed.13="+str(Thread_SEED+14000) + \
									" -p seed.14="+str(Thread_SEED+15000) + \
									" -p seed.15="+str(Thread_SEED+16000) + \
									" -p seed.16="+str(Thread_SEED+17000) + \
									" -p seed.17="+str(Thread_SEED+18000) + \
									" -p seed.18="+str(Thread_SEED+19000) + \
									" -p seed.19="+str(Thread_SEED+20000) + \
									" -p seed.20="+str(Thread_SEED+21000) + \
									" -p seed.21="+str(Thread_SEED+22000) + \
									" -p seed.22="+str(Thread_SEED+23000) + \
									" -p seed.23="+str(Thread_SEED+24000) + \
									" -p seed.24="+str(Thread_SEED+25000) + \
									" -p seed.25="+str(Thread_SEED+26000) + \
									" -p seed.26="+str(Thread_SEED+27000) + \
									" -p seed.27="+str(Thread_SEED+28000) + \
									" -p seed.28="+str(Thread_SEED+29000) + \
									" -p seed.29="+str(Thread_SEED+30000) + \
									" -p seed.30="+str(Thread_SEED+31000) + \
									" -p seed.31="+str(Thread_SEED+32000) + \
									" -p seed.32="+str(Thread_SEED+33000) + \
									" -p seed.33="+str(Thread_SEED+34000) + \
									" -p seed.34="+str(Thread_SEED+35000) + \
									" -p seed.35="+str(Thread_SEED+36000) + \
									" -p stat.file="+file
						
						Thread_SEED = Thread_SEED + 17
						
						os.system(cmd_string)


#### Fixed Mutation rate experiment ####
def run_ffd_for_fixed_mutrate(param_fixed_mut_rate):
	for param_subpop_size in range_subpop_size:
		for param_genome_length in range_genome_length:
			for param_crossover_type in range_crossover_type:
				for param_elitist_number in fixed_mut_range_elitist_number:
					
					Thread_SEED=92341
					# run multiple jobs per permutation
					for j in range(0, JOBS):
						
						print "=========================================="
						print "Job - "+str(j)
						print "param_subpop_size :: "+ str(param_subpop_size)
						print "param_genome_length :: "+ str(param_genome_length)
						print "param_crossover_type :: "+ param_crossover_type
						print "param_elitist_number :: "+ str(param_elitist_number)					
						print "=========================================="
						
						file = get_file_path(param_subpop_size, 
											param_genome_length, 
											param_crossover_type, 
											param_elitist_number,
											'FIXED',
											param_fixed_mut_rate,
											j)
						
						cmd_string = "java ec.Evolve -file morpion5t_v3.params" + \
									" -p pop.subpop.0.size="+ str(param_subpop_size) + \
									" -p pop.subpop.0.species.genome-size="+ str(param_genome_length) + \
									" -p pop.subpop.0.species.crossover-type="+ param_crossover_type + \
									" -p breed.elite.0="+ str(param_elitist_number) + \
									" -p pop.subpop.0.species.mutation-prob="+str(param_fixed_mut_rate) + \
									" -p seed.0="+str(Thread_SEED+1000) + \
									" -p seed.1="+str(Thread_SEED+2000) + \
									" -p seed.2="+str(Thread_SEED+3000) + \
									" -p seed.3="+str(Thread_SEED+4000) + \
									" -p seed.4="+str(Thread_SEED+5000) + \
									" -p seed.5="+str(Thread_SEED+6000) + \
									" -p seed.6="+str(Thread_SEED+7000) + \
									" -p seed.7="+str(Thread_SEED+8000) + \
									" -p seed.8="+str(Thread_SEED+9000) + \
									" -p seed.9="+str(Thread_SEED+10000) + \
									" -p seed.10="+str(Thread_SEED+11000) + \
									" -p seed.11="+str(Thread_SEED+12000) + \
									" -p seed.12="+str(Thread_SEED+13000) + \
									" -p seed.13="+str(Thread_SEED+14000) + \
									" -p seed.14="+str(Thread_SEED+15000) + \
									" -p seed.15="+str(Thread_SEED+16000) + \
									" -p seed.16="+str(Thread_SEED+17000) + \
									" -p seed.17="+str(Thread_SEED+18000) + \
									" -p seed.18="+str(Thread_SEED+19000) + \
									" -p seed.19="+str(Thread_SEED+20000) + \
									" -p seed.20="+str(Thread_SEED+21000) + \
									" -p seed.21="+str(Thread_SEED+22000) + \
									" -p seed.22="+str(Thread_SEED+23000) + \
									" -p seed.23="+str(Thread_SEED+24000) + \
									" -p seed.24="+str(Thread_SEED+25000) + \
									" -p seed.25="+str(Thread_SEED+26000) + \
									" -p seed.26="+str(Thread_SEED+27000) + \
									" -p seed.27="+str(Thread_SEED+28000) + \
									" -p seed.28="+str(Thread_SEED+29000) + \
									" -p seed.29="+str(Thread_SEED+30000) + \
									" -p seed.30="+str(Thread_SEED+31000) + \
									" -p seed.31="+str(Thread_SEED+32000) + \
									" -p seed.32="+str(Thread_SEED+33000) + \
									" -p seed.33="+str(Thread_SEED+34000) + \
									" -p seed.34="+str(Thread_SEED+35000) + \
									" -p seed.35="+str(Thread_SEED+36000) + \
									" -p stat.file="+file
						
						Thread_SEED = Thread_SEED + 17
						
						os.system(cmd_string)
						




# Create two threads as follows
try:    
	#run_ffd_for_dynamic_mutrate( range_dynamic_mutation_rate[0] )
	run_ffd_for_fixed_mutrate( range_fixed_mutation_rate[0] )
except Exception, e:
   print "Error: unable to start prog : "+str(e) 

while 1:
   pass







'''
for j in range(1, jobs):
	print "Job - "+str(j)
	cmd_string = "java ec.Evolve -file morpion5t_v3.params" + \
				" -p seed.0="+str(SEED) + \
				" -p breed.elite-fraction.0="+str(ELITIST_R +(0.0495*j)) + \
				" -p stat.file=job."+str(j)+".out.stat"
	
	SEED = SEED + 17
	
	os.system(cmd_string)
	
'''
	
