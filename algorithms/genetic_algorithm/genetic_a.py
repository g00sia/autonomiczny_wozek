import random
import math
from copy import deepcopy


def manhattan_distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


def fitness(solution, packages, forklift_position):
    total_distance = 0
    current_position = forklift_position

    for package_index in solution:
        package_position = packages[package_index]
        total_distance += manhattan_distance(current_position, package_position)
        current_position = package_position

    return total_distance


def initial_population(pop_size, num_packages):
    population = []
    for _ in range(pop_size):
        individual = list(range(num_packages))
        random.shuffle(individual)
        population.append(individual)
    return population

def selection(population, fitnesses, num_parents):
    selected_parents = random.choices(population, weights=fitnesses, k=num_parents)
    return selected_parents


def crossover(parent1, parent2):
    cut = random.randint(0, len(parent1) - 1)
    child1 = parent1[:cut] + [item for item in parent2 if item not in parent1[:cut]]
    child2 = parent2[:cut] + [item for item in parent1 if item not in parent2[:cut]]
    return child1, child2


def mutate(individual, mutation_rate):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            swap_index = random.randint(0, len(individual) - 1)
            individual[i], individual[swap_index] = individual[swap_index], individual[i]

def genetic_algorithm(packages, forklift_position, pop_size=100, num_generations=100, mutation_rate=0.01):
    num_packages = len(packages)
    population = initial_population(pop_size, num_packages)
    
    for generation in range(num_generations):
        fitnesses = [1 / fitness(individual, packages, forklift_position) for individual in population]
        new_population = []
        
        while len(new_population) < pop_size:
            parents = selection(population, fitnesses, 2)
            child1, child2 = crossover(parents[0], parents[1])
            mutate(child1, mutation_rate)
            mutate(child2, mutation_rate)
            new_population.append(child1)
            new_population.append(child2)
        
        population = new_population


    best_solution = min(population, key=lambda individual: fitness(individual, packages, forklift_position))
    return best_solution



