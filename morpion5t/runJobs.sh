#!/bin/sh

SEED=92341
CROSS_P=0.1
for job in `seq 1 10`;
do
	echo ::Job - $job
	SEED=$(($SEED+17))
	CROSS_P = $((CROSS_P * $job ))
	
	echo ::SEED - $SEED
	echo ::CROSS_P - $CROSS_P
	
	java ec.Evolve -file morpion5t_v3.params \
				-p seed.0=${SEED} \
				-p pop.subpop.0.species.crossover-prob=${CROSS_P} \
				-p stat.file=job.$job.out.stat

done
