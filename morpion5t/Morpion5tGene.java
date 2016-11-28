package ec.app.morpion5t;

import java.io.DataOutput;
import java.io.IOException;

import ec.*;
import ec.vector.*;
import ec.util.*;

/************************************************************************
Morpion5tGene
Custom Genome representation
e.g. (x1, y1), (x2, y2)
*************************************************************************/
public class Morpion5tGene extends Gene {
	int x1;
	int y1;
	int x2;
	int y2;
	
	private static final int GENE_MAX = 26;
	private static final int GENE_MIN = 15;
	
	int GridMAX = 23;
	int GridMIN	= 19;
	
	/* Reset - called during initialisation */
	public void reset(EvolutionState state, int thread) {
		
		double d;		
		
		// get the grid boundaries from gamememory static class
		d = state.random[thread].nextDouble();
		x1 = (int)(d * (GameMemory.bounds_max - GameMemory.bounds_min)) + GameMemory.bounds_min;
		d = state.random[thread].nextDouble();
		y1 = (int)(d * (GameMemory.bounds_max - GameMemory.bounds_min)) + GameMemory.bounds_min;
		
		// determine line direction (|-\/)
		// 0 - South
		// 1 - East
		// 2 - South_East
		// 3 - South_West
		d = state.random[thread].nextDouble();
		int dir = (int)(d * (3 - 0)) + 0;
		
		 switch (dir) {
		 
		 	// South
		 	case 0:
		 		x2 = x1;
		 		y2 = y1 - 5;
		 		break;

		 	// East 
		 	case 1:
		 		x2 = x1 + 5;
		 		y2 = y1;
		 		break;

		 	// South_East		 		
		 	case 2:
		 		x2 = x1 + 5;
		 		y2 = y1 - 5;
		 		break;
		 		
		 	// South_West	
		 	case 3:
		 		x2 = x1 - 5;
		 		y2 = y1 - 5;
		 		break;
		 	
		 	// wrong !	
		 	default :
		 		state.output.fatal("Whoa!  Wrong Gene-(dir)!!!",null);
		 		break;
		 }
	}
	
	/* Mutate method - same as reset - for now ! */
	public void mutate(EvolutionState state, int thread) {
		
		double d;	
		
		// get the grid boundaries from gamememory static class
		d = state.random[thread].nextDouble();
		x1 = (int)(d * (GameMemory.bounds_max - GameMemory.bounds_min)) + GameMemory.bounds_min;
		d = state.random[thread].nextDouble();
		y1 = (int)(d * (GameMemory.bounds_max - GameMemory.bounds_min)) + GameMemory.bounds_min;
		
		// determine line direction (|-\/)
		// 0 - South
		// 1 - East
		// 2 - South_East
		// 3 - South_West
		d = state.random[thread].nextDouble();
		int dir = (int)(d * (3 - 0)) + 0;
		
		 switch (dir) {
		 
		 	// South
		 	case 0:
		 		x2 = x1;
		 		y2 = y1 - 5;
		 		break;

		 	// East 
		 	case 1:
		 		x2 = x1 + 5;
		 		y2 = y1;
		 		break;

		 	// South_East		 		
		 	case 2:
		 		x2 = x1 + 5;
		 		y2 = y1 - 5;
		 		break;
		 		
		 	// South_West	
		 	case 3:
		 		x2 = x1 - 5;
		 		y2 = y1 - 5;
		 		break;
		 	
		 	// wrong !	
		 	default :
		 		state.output.fatal("Whoa!  Wrong Gene-(dir)!!!",null);
		 		break;
		 }
	}
	
	/* hashCode - for genome comparisons */
	public int hashCode() {
		String s = Integer.toString(x1) + Integer.toString(y1) + Integer.toString(x2) + Integer.toString(y2);
		return Integer.parseInt(s);
	}
	
	/* equals - used to compare one genome with another */
	public boolean equals(Object other) {
		return (other != null && 
				other instanceof Morpion5tGene &&
				((Morpion5tGene)other).x1 == x1 && 
				((Morpion5tGene)other).y1 == y1 &&
				((Morpion5tGene)other).x2 == x2 &&
				((Morpion5tGene)other).y2 == y2			
				);
	}
	
	/* human readable genome string */ 
	public String printGeneToStringForHumans() { 
		return (Integer.toString(x1) + " " +
				Integer.toString(y1) + " " +
				Integer.toString(x2) + " " +
				Integer.toString(y2));
	}	
	
	/* used to pass into Msol.exe */
	public String printGeneToString() {
		return (Integer.toString(x1) + " " +
				Integer.toString(y1) + " " +
				Integer.toString(x2) + " " +
				Integer.toString(y2));
	}	
	
}
