package ec.app.morpion5t;

import java.io.BufferedReader;
import java.io.InputStreamReader;

import ec.*;
import ec.simple.*;
import ec.util.*;
import ec.vector.*;

import ec.app.morpion5t.GameMemory;

/************************************************************************
MorpionEval
Fitness evaluation class
- fitness score is taken from the morpionSol.exe program output (last line)
*************************************************************************/
public class MorpionEval extends Problem implements SimpleProblemForm{
    
	/* define the problem */
	public void evaluate(final EvolutionState state,
                         final Individual ind,
                         final int subpopulation,
                         final int threadnum)
        {
        if (ind.evaluated) return;

        if (!(ind instanceof GeneVectorIndividual)){
            state.output.fatal("Whoa!  It's not a GeneVectorIndividual!!!",null);
        }
        
        GeneVectorIndividual ind2 = (GeneVectorIndividual)ind;        		
		int rawfitness = 0;
		rawfitness = getFitnessFromMSol(ind2.genome, state.generation);
		
        // validity checking of raw fitness
		if(rawfitness <0){
        	state.output.fatal("Whoa!  Fitness Score returned negative !!",null);
        }		
        if (!(ind2.fitness instanceof SimpleFitness))
            state.output.fatal("Whoa!  It's not a SimpleFitness!!!",null);
        
        ((SimpleFitness)ind2.fitness).setFitness(state,
                
        		(float)rawfitness, // fitness is not normalised              
                false // ideal ? there is no defined ideal scenario
                );
        ind2.evaluated = true;
        }
    
    /* helper function to get a fitness score from the morpionSol.exe */ 
    public int getFitnessFromMSol(Gene[] genome, int gen){    	
    	
		String[] cmd = new String[ genome.length + 1 ]; 
		// assumes the executable to be in the current directory
		cmd[0] = "./linuxLiteMsolitare.exe"; 
		
		int output_score;
		String arg = "";		
		
		// form the command line string
		for (int i = 0; i < genome.length; i++) {
			arg = genome[i].printGeneToString() + " ";
			cmd[i+1] = arg;
			//System.out.print(arg);
		}
		
		// execute the .exe with the proper command line arguments
		// and parse the output
		try {
			Process p = Runtime.getRuntime().exec(cmd);
			BufferedReader in = new BufferedReader(new InputStreamReader(p.getInputStream()));			
			String cmdOutput = "";
			String score = "";
			String result_lines="";
			while ( (cmdOutput = in.readLine()) != null){				
				result_lines = result_lines + " " + cmdOutput;				
				score = cmdOutput;
				//System.out.println(cmdOutput);
			}
			
			result_lines = result_lines.trim();
			
			// update GameMemory
			// grid bounds are updated accordingly within this class
			GameMemory.setBounds(Integer.parseInt(score), result_lines, gen);
			//GameMemory.setBounds2(Integer.parseInt(score));
			
			// return final fitness val
			return Integer.parseInt(score);
			
		} catch (java.io.IOException e) {
			// put code here to raise an appropriate exeception						
			System.out.println("help!");
			e.printStackTrace();
			return -1;				
		}	
    }
}