# morpion5t_ecj
A weak attempt at Morpion5t game solving, using Genetic Algorithms (GA), using the ECJ framework.

Morpion Solitaire : http://www.morpionsolitaire.com/
ECJ (Evolutionary computing framework in Java) : http://cs.gmu.edu/~eclab/projects/ecj/docs/


So far the best score obtained : 55

* GA structure
- a genome : is 2 (x,y) pairs (i.e. 4 integers)
- fitness : score of the linuxLiteMSolitaire.exe program
- elitism used
- tournament selection
- one-point/two-point crossover
- adaptive mutation (dynamic mut.rate based on fitness)
