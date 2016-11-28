package ec.app.morpion5t;

import java.util.*;

/************************************************************************
GameMemory
Class used to keep track of previous best fitness values
Based on the current fitness value the grid bouundaries are scaled 
(i.e. solution space scaled down)
*************************************************************************/
public class GameMemory {
	
		// these used to keep track of the bounds
		public static int ind_min=0;
		public static int ind_max=30;
		
		public static int bounds_min =15;
		public static int bounds_max =26;		
		
		// previous best fitness
		public static int prevBestFitness=0;
		
		// how long has it been since the last best fitness update
		public static int gensSinceLastBestfitness=0;
		private static int currentGen = 0;
		
		// constants
		public static int FITNESS_BOUNDARY = 30;		
		
		// set bounds if current fitness of individual is better
		public static void setBounds(int fitness, String str_result_genome, int gen){
			if(fitness > prevBestFitness){
				
				prevBestFitness = fitness;
				
				int[] result_genome=_cleanupResults(str_result_genome);
				
				Arrays.sort(result_genome); 
				// new values
				ind_min = result_genome[0];
				ind_max = result_genome[result_genome.length-1];
				
				// increase the bounds based on a specified 'good' fitness level
				// increase by an offset of +1
				// thus allowing incremental exploration
				if(fitness >= FITNESS_BOUNDARY){					
					bounds_min--;
					bounds_max++;					
				}
				
				// keep within legal bounds of grid
				if(bounds_max > 40)
					bounds_max = 40;
				if(bounds_min < 0)
					bounds_min = 0;
				
				System.out.println("GameMemory:: "+
									bounds_min+","+bounds_max+", fit:"+
									fitness+",GensSinceLastBestFit:"+gensSinceLastBestfitness);
				gensSinceLastBestfitness=0;
				currentGen=gen;
				
			}else{
				if(gen>currentGen){
					gensSinceLastBestfitness++;
					currentGen=gen;
				}
			}
		}
				
		// helper function
		private static int[] _cleanupResults(String results){
			String split_res[] = results.split(" ");
			
			int i;
			int[] results_genome=new int[split_res.length];
			for(i=0;i<split_res.length-1;i++){
				results_genome[i]=Integer.parseInt(split_res[i]);
			}
			
			return results_genome;
		}
	
}