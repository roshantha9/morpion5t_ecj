#! /usr/bin/python

import os

SEED=92341
CROSS_P=0.1

SUBPOPSIZE=400

ELITIST_R = 0.01

TOURNAMENT_SIZE = 


jobs = 9

for j in range(1, jobs):
	print "Job - "+str(j)
	cmd_string = "java ec.Evolve -file morpion5t_v3.params" + \
				" -p seed.0="+str(SEED) + \
				" -p select.tournament.size=" + str(j)
				" -p breed.elite-fraction.0="+str(ELITIST_R +(0.0495*j)) + \
				" -p stat.file=job."+str(j)+".out.stat"
	
	SEED = SEED + 17
	
	os.system(cmd_string)
	