from sys import stdin, stdout
import random

def fitness(tour, distances):
    return sum(distances[tour[i]][tour[i + 1]] for i in range(len(tour) - 1)) + distances[tour[-1]][tour[0]]

def nearest_neighbor_tsp(distances, s):
    num_cities = len(distances)
    unvisited = set(range(num_cities))
    tour = []
    current_city = s

    while unvisited:
        unvisited.remove(current_city)
        tour.append(current_city)
        if unvisited:
            nearest_neighbor = min(unvisited, key=lambda city: distances[current_city][city])
        current_city = nearest_neighbor
    return tour

def roulette_wheel_selection(population, fitness_values):
    inverted_fitness = [1 / fit for fit in fitness_values]
    total_fitness = sum(inverted_fitness)
    selection_probabilities = [fit / total_fitness for fit in inverted_fitness]
    selected_population = random.choices(population, selection_probabilities, k=len(population))
    return selected_population

def order_crossover(parent1, parent2):
    n = len(parent1)
    start, end = sorted(random.sample(range(n), 2))
    segment1, segment2 = parent1[start:end + 1], parent2[start:end + 1]
    child1, child2 = [-1] * n, [-1] * n
    child1[start: end + 1], child2[start: end + 1] = segment2, segment1

    current_idx = end + 1
    for city in parent1:
        if city not in segment2:
            child1[current_idx % n] = city
            current_idx += 1

    current_idx = end + 1
    for city in parent2:
        if city not in segment1:
            child2[current_idx % n] = city
            current_idx += 1

    return child1, child2

def two_edge_exchange(tour):
    i, j, k, l = random.sample(range(len(tour)), 4)
    tour[i], tour[j], tour[k], tour[l] = tour[k], tour[l], tour[i], tour[j]
    return tour

def mutate_tour(tour, mutation_prob):
    if random.random() < mutation_prob:
        return two_edge_exchange(tour)
    else:
        return tour

def genetic_algorithm_tsp(population, distances, generations=20, mutation_prob=0.2):
    for i in range(generations):
        fitness_values = [fitness(tour, distances) for tour in population]
        selected_population = roulette_wheel_selection(population, fitness_values)

        parent_indices = random.sample(range(len(selected_population)), 2)
        parent1, parent2 = selected_population[parent_indices[0]], selected_population[parent_indices[1]]

        child1, child2 = order_crossover(parent1, parent2)

        child1, child2 = mutate_tour(child1, mutation_prob), mutate_tour(child2, mutation_prob)

        population.append(child1)
        population.append(child2)
        population.remove(max(population, key=lambda x:fitness(x, distances)))
        population.remove(max(population, key=lambda x:fitness(x, distances)))

    return population

def simulated_annealing(tour, distances, temperature=1000, cooling_rate=0.003, num_iterations=10000):
    current_tour = tour.copy()
    best_tour = tour.copy()
    current_fitness = fitness(current_tour, distances)
    best_fitness = current_fitness

    for i in range(num_iterations):
        new_tour = current_tour[:]
        a, b = random.sample(range(len(new_tour)), 2)
        new_tour[min(a, b): max(a, b) + 1] = new_tour[min(a, b): max(a, b) + 1][::-1]
        new_fitness = fitness(new_tour, distances)
        if new_fitness < current_fitness:
            current_tour = new_tour
            current_fitness = new_fitness
            if new_fitness < best_fitness:
                best_tour = new_tour
                best_fitness = new_fitness
        else:
            acceptance_prob = 1 / (1 + 2.71 ** min((new_fitness - current_fitness) / temperature, 9))
            if random.random() < acceptance_prob:
                current_tour = new_tour
                current_fitness = new_fitness
        temperature *= 1 - cooling_rate

    return best_tour

if __name__ == "__main__":
    # Read the inputs
    method = stdin.readline()
    num_cities = int(stdin.readline())
    for _ in range(num_cities):
        coordinates = list(map(float, stdin.readline().split()))
    distances = [list(map(float, stdin.readline().split())) for _ in range(num_cities)]

    # Nearest Neighbor Heuristic to generate initial population
    current_solution = nearest_neighbor_tsp(distances, 0)
    stdout.write(' '.join(map(str, current_solution)))
    stdout.write('\n')
    prev_solution = current_solution.copy()

    tours = [current_solution]
    best_tour = current_solution
    best_fitness = fitness(current_solution, distances)
    for i in range(1, len(distances)):
        tour = nearest_neighbor_tsp(distances, i)
        tours.append(tour)
        if fitness(tour, distances) < best_fitness:
            best_tour = tour
            best_fitness = fitness(tour, distances)
            stdout.write(' '.join(map(str, best_tour)))
            stdout.write('\n')
    prev_solution = best_tour.copy()

    # Eternally keep searching for best solution, until external termination
    while True:
        # Genetic Algorithm on the population to make it fitter
        population = genetic_algorithm_tsp(tours, distances)
        current_solution = min(population, key=lambda x: fitness(x, distances))
        if fitness(current_solution, distances) < fitness(prev_solution, distances):
            stdout.write(' '.join(map(str, current_solution)))
            stdout.write('\n')
            prev_solution = current_solution.copy()

        tours = []
        best_fitness = fitness(prev_solution, distances)
        # Simulated Annealing on each member of fit population
        for route in population:
            path = simulated_annealing(route, distances)
            tours.append(path)
            if fitness(path, distances) < best_fitness:
                best_fitness = fitness(path, distances)
                stdout.write(' '.join(map(str, path)))
                stdout.write('\n')
                prev_solution = path.copy()