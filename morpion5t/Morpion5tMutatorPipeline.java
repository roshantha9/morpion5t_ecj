package ec.app.morpion5t;
import ec.vector.*;
import ec.*;
import ec.util.*;

import ec.app.morpion5t.GameMemory;

/************************************************************************
Morpion5tMutatorPipeline
Custom mutator pipeline class
- dynamic mutation rate
OR
- fixed mutation rate

Initial mutation rate defined in parameter file
*************************************************************************/
public class Morpion5tMutatorPipeline extends BreedingPipeline{
	
	 //used only for our default base
    public static final String P_MORPION5TMUTATION = "morpion5t-mutation";

    // We have to specify a default base, even though we never use it
    public Parameter defaultBase() { return VectorDefaults.base().push(P_MORPION5TMUTATION); }
	
	public static final int NUM_SOURCES = 1;

    // Return 1 -- we only use one source
    public int numSources() { return NUM_SOURCES; }
	
    /*
    Create a most _max_ and at least _min_ individuals,
    drawn from our source and mutated, and stick them into slots in inds[]
    starting with the slot inds[start].  
    produce(...) returns the number of individuals actually put into inds[]
    */
    public int produce(final int min, 
		       final int max, 
		       final int start,
		       final int subpopulation,
		       final Individual[] inds,
		       final EvolutionState state,
		       final int thread)
        {
		
    	// grab individuals from our source and stick 'em right into inds.
        int n = sources[0].produce(min,max,start,subpopulation,inds,state,thread);
		
		// should we bother?
		if (!state.random[thread].nextBoolean(likelihood))
			// DON'T produce children from source -- we already did
			return reproduce(n, start, subpopulation, inds, state, thread, false);
			
		// clone the individuals if necessary 
        if (!(sources[0] instanceof BreedingPipeline))
            for(int q=start;q<n+start;q++)
                inds[q] = (Individual)(inds[q].clone());
				
		// Check to make sure that the individuals are IntegerVectorIndividuals and
        // grab their species.
        if (!(inds[start] instanceof GeneVectorIndividual)) {
            // uh oh, wrong kind of individual
            state.output.fatal("Morpion5tMutatorPipeline didn't get an " +
            "IntegerVectorIndividual.  The offending individual is " +
            "in subpopulation " + subpopulation + " and it's:" + inds[start]);
        }
        
        GeneVectorSpecies species = (GeneVectorSpecies)(inds[start].species);        
        
		// Mutate the gene - using the custom mutation method in the Custom Gene class
        for(int q=start;q<n+start;q++){
        	GeneVectorIndividual i = (GeneVectorIndividual)inds[q];
            for(int x=0;x<i.genome.length;x++){
      
            	/** Uncomment dynamic/fixed mutation rate option as necessary **/
            	
            	/*
            	// dynamic probability
        		if (state.random[thread].nextBoolean( (species.mutationProbability(x) * 1/(GameMemory.prevBestFitness)) )){	                  
                	i.genome[x].mutate(state, thread);       
                }
                */
            	
            	// fixed probability
            	if (state.random[thread].nextBoolean( species.mutationProbability(x))){	                  
                	i.genome[x].mutate(state, thread);       
                }
            }
            // it's a "new" individual, so it's no longer been evaluated
            i.evaluated=false;
        }   
        return n;
        }
 }	
		