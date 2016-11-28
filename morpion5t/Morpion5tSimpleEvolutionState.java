package ec.app.morpion5t;
import ec.vector.*;
import ec.*;
import ec.util.*;
import ec.simple.*;

import ec.app.morpion5t.GameMemory;

/*
 * Morpion5tMutatorPipeline.java
 */

/**
 OurMutatorPipeline is a BreedingPipeline which negates the sign of genes.
 The individuals must be IntegerVectorIndividuals.  Because we're lazy,
 we'll use the individual's species' mutation-probability parameter to tell
 us whether or not to mutate a given gene.
 
 <p><b>Typical Number of Individuals Produced Per <tt>produce(...)</tt> call</b><br>
 (however many its source produces)

 <p><b>Number of Sources</b><br>
 1
*/
public class Morpion5tSimpleEvolutionState extends SimpleEvolutionState{
	
	 public void startFresh(){
		 int jobNum = ((Integer)(job[0])).intValue();
		 parameters.set(new ec.util.Parameter("pop.subpop.0.species.genome-size"), "" + ((jobNum * 100)+500));
		 
		 super.startFresh();
	 }
 }
		
		
		