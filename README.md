Name: Indraneel Dey BSc in Data Science and Programming
Roll number: 21f3002696 
AI: Search Methods for Problem Solving
Programming Assignment Report

This report is about the explanation of an algorithm used to find an optimal tour of the Travelling Salesman Problem (TSP) within time constraints. The algorithm used has the following steps:

1. Generation of initial population:

At first, Nearest Neighbor Heuristic is used to generate a sub-optimal but decent tour for the given distances. This is done n times, once for each city (taking the city as the starting city). Hence, this step generates a population of n tours, where n is the number of cities.

Upon the creation of every Nearest Neighbor tour in this step, it is checked whether it is a shorter route than the previous best, and if so, it is updated as the current best tour and printed to standard output.

2. Genetic Algorithm on the population:

Now that we have an initial population of n tours, Genetic Algorithm is applied to the population to make it fitter. The hyperparameters used for the Genetic Algorithm are 20 generations and 0.2 probability of mutation.

First of all, selection is done with Roulette Wheel Selection. Probabilities are assigned to the tours in the population, proportional to the inverse of their length. So shorter (better) tours get higher probabilities. Then n tours are selected with replacement from the population based on these probabilities. So the best tours have the most number of clones in the selcted population, and the worst tours appear the least.

Next, recombination is done with Order Crossover. Order Crossover is the simplest among the crossover algorithms and computationally takes the shortest time, so it was preferred over other algorithms like Cycle Crossover. Two random ‘parents’ are chosen from the selected population (so shorter tours have higher probability of being chosen) and Order Crossover is applied on them to generate two ‘children’.

Finally, the children are mutated with a certain probability (0.2 in this case). Mutation is done with 2-Edge-Exchange. Four of the cities in the tour are chosen at random and exchanged to generate a new, mutated tour. Due to this, this algorithm can be applied on a minimum of 4 cities. This mutation is done to produce variety in the population.

Now, the two children are added to the population and the worst two tours of the population are removed. That is, the children are added to the population only if they are
better than at least the two worst tours. So the size of the population is maintained at n but the average fitness of the population increases, assuming at least one of the two children is fitter than the worst.

This entire process of selection-recombination-mutation is repeated for the number of ‘generations’ (iterations) so the population keeps becoming progressively fitter.
Upon creation of the fitter population after the completion of the Genetic Algorithm, it is checked whether the best tour in this population is better than the previous best, and if so, it is updated as the current best tour and printed to standard output.

3. Iterated Simulated Annealing on the population:

Now that we have a fit population of n tours, Iterated Simulated Annealing is applied to it, i.e., Simulated Annealing is applied to every member of this population to make it even better, shorter. 2-Opt-Swap is performed on the tour with two random cities to generate a neighbor, and this neighbor is moved to probabilistically depending on the difference in lengths of the tours and temperature.

The temperature and cooling rate hyperparameters are initialized as 1000 and 0.003. Simulated Annealing is carried out on each tour in the population for 10000 iterations.
After each tour has been updated to a better one through Simulated Annealing, it is checked if it is better than the previous best, and if so, it is updated as the current best tour and printed to the standard output.

4. Repeat:

The second and third steps are repeated.

On the new population created after Iterated Simulated Annealing, apply Genetic Algorithm again and update the current best tour. Then on this fitter population apply Iterated Simulated Annealing again and keep updating the current best tour. Keep repeating for an infinite number of iterations.

This way, the population will progressively keep getting fitter and better, and the current best tour will continue getting shorter. The total algorithm will give some preliminary ‘best’ tours and keep searching for new ones as time goes on, as it keeps iterating the cycle of Genetic Algorithm and Iterated Simulated Annealing.

The results will be checked of the best tour given after the time limit is up so there is no point in generating a sub-optimal solution before then and being satisfied with it. So, this algorithm keeps searching for better solutions eternally, just like a Chess Engine keeps searching for better moves the longer it is run.

The entire program is written in Python 3. The only libraries used are random for random number generation in Genetic Algorithm and Simulated Annealing, and sys for reading standard input and printing standard output. 8 functions are made for:

1. computing the length of a tour
2. Nearest Neighbor Heuristic
3. Roulette Wheel Selection
4. Order Crossover
5. Two Edge Exchange
6. mutating a tour which internally calls Two Edge Exchange
7. Genetic Algorithm which internally calls Roulette Wheel Selection, Order Crossover and mutating tours
8. Simulated Annealing

The shell script run.sh is executed in a linux environment. It contains the command for running the Python program.

This program can be further improved with hyperparameter tuning of generations and mutation probability in Genetic Algorithm and temperature, cooling rate and number of iterations of Simulated Annealing. This can be done through Reinforcement Learning where the program solves a number of TSPs to learn the best hyperparameters.
