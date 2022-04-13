import json
import math
import time
from enum import Enum
from random import randint

import IGUI
import process
from models import Chromosome

processor = process


class Algorithms(Enum):
    Empty = 'nothing'
    HC = 'Hill Climbing'
    SA = 'Simulated Annealing'
    GA = 'Genetic Algorithms'


algorithm = Algorithms.Empty

with open('Cities.json', encoding='utf-8') as file:
    data = json.load(file)


def hill_climbing(cities):
    global algorithm
    algorithm = Algorithms.HC
    start_time = time.time()
    while True:
        formulate_route(cities)
        current_cost = calc_cost(cities)
        result = find_best_swap(cities, current_cost, 0)
        if result == -1:
            break
        else:
            swap(cities, result, result+1)
            print('swap: ' + str(current_cost - calc_cost(cities)))
    print('Time: ' + str(time.time() - start_time))
    return cities


def simulated_annealing(cities):
    global algorithm
    algorithm = Algorithms.SA
    start_time = time.time()
    iterations = 0
    best_sol = list(cities)
    best_sol_cost = calc_cost(cities)
    temperature = 3000
    couter = 0
    while temperature > 500:
        iterations += 1
        formulate_route(cities)
        current_cost = calc_cost(cities)
        result = find_best_swap(cities, current_cost, temperature)
        if result == -1:
            break
        else:
            swap(cities, result, result+1)
            new_cost = calc_cost(cities)
            print('swap: ' + str(current_cost - new_cost))
            if new_cost < best_sol_cost:
                best_sol = list(cities)
                best_sol_cost = new_cost
        temperature = cooldown(temperature)
        couter += 1
    print('Time: ' + str(time.time() - start_time))
    print("C" + str(couter))
    return best_sol


def schedule(t):
    return 20 - t


def find_best_swap(ls, current_cost, tmp=0):
    best_swap = -1
    s_best_swap = -1
    best_cost = current_cost
    s_best_cost = -1
    for i in range(0, len(ls) - 1):  # range: upper is exclusive
        swapped = list(ls)
        swap(swapped, i, i+1)
        new_cost = calc_cost(swapped)
        print('current cost: ' + str(current_cost) + ', new cost: ' + str(new_cost))
        diff = best_cost - new_cost
        if algorithm == Algorithms.HC:
            if diff > 0:
                best_swap = i
                best_cost = new_cost
        elif algorithm == Algorithms.SA:
            prob = get_prob(best_cost, new_cost, tmp)
            if diff > 0:
                best_swap = i
                best_cost = new_cost
            elif s_best_cost == -1 or (new_cost < s_best_cost and prob > 0.5):
                s_best_swap = i
                s_best_cost = new_cost
    if best_swap != -1:
        return best_swap
    else:
        return s_best_swap


v = -1
POP_SIZE = 10
problem = []


def genetic(cities):
    global algorithm, v, problem
    algorithm = Algorithms.GA
    v = len(cities)
    problem = list(cities)
    solution = list(cities)
    sol_cost = calc_cost(cities)

    # Generation Number
    gen = 1
    # Number of Gene Iterations
    gen_thres = 8
    population = []
    # Populating the GNOME pool.
    for i in range(POP_SIZE):
        gnome = create_gnome()
        population.append(Chromosome(gnome, calc_cost(gnome)))

    temperature = 3000
    # Iteration to perform population crossing and gene mutation.
    while temperature > 500 and gen <= gen_thres:
        population.sort()
        display_gen(gen, population)
        solution, sol_cost = get_best(solution, sol_cost, population)    # Python Stuff
        print("\nCurrent temp: ", temperature)

        new_population = []
        for i in range(POP_SIZE):
            old_pop = population[i]
            while True:
                new_g = mutate(old_pop.gnome)
                new_gnome = Chromosome(new_g, calc_cost(new_g))

                if new_gnome.fitness <= population[i].fitness:
                    new_population.append(new_gnome)
                    break
                else:    # Accepting the rejected children at a possible probability above threshold.
                    prob = get_prob(population[i].fitness, new_gnome.fitness, temperature)
                    if prob > 0.5:
                        new_population.append(new_gnome)
                        break

        temperature = cooldown(temperature)
        population = new_population
        gen += 1

    solution = get_best(solution, sol_cost, population)[0]
    display_gen(gen, population)
    return solution


# Function to return a mutated GNOME.
# Mutated GNOME is a string with a random interchange of two genes to create variation in species
def mutate(gnome):
    gnome = list(gnome)
    while True:
        r1 = randint(1, v-1)
        r2 = randint(1, v-1)
        if r1 != r:
            swap(gnome, r1, r2)
            break
    return gnome


# Function to return a valid GNOME string required to create the population
def create_gnome():
    gnome = []
    while True:
        if len(gnome) == v:
            break
        temp = randint(0, v-1)
        if not gnome.__contains__(problem[temp]):
            gnome.append(problem[temp])
    return gnome


# Function to return the updated value of the cooling element.
def cooldown(temp):
    return 90 * temp / 100


def get_best(old, old_cost, pop):
    best = list(old)
    best_cost = old_cost
    for i in range(len(pop)):
        if pop[i].fitness < best_cost:
            best = pop[i].gnome
            best_cost = pop[i].fitness
    return best, best_cost


def display_gen(gen, population):
    print("Generation", gen)
    print("GNOME \t\t\t\t\t FITNESS VALUE")
    for i in range(POP_SIZE):
        print(population[i].gnome, population[i].fitness)


def get_prob(old, new, tmp):
    return math.exp((old - new) / tmp)


def swap(ls, i1, i2):
    ls[i1], ls[i2] = ls[i2], ls[i1]  # swap


def calc_cost(route):
    cost = 0
    for i in range(0, len(route) - 1):
        a_star_solution = processor.a_star(route[i], route[i + 1])[1]
        cost += a_star_solution.distance
    return cost


def formulate_route(route):
    string = str()
    for element in route:
        string += data[element]['name'] + ' ← '
    print(string[:-3])


r = [53, 93, 28, 149, 0, 85, 49]    # HC: 5327  ,  SA: 4279  ,  GA: 3179
b = [149, 49, 53, 0, 28, 93, 85]    # 3179
sol = genetic(r)
print('Best Cost: ' + str(calc_cost(sol)))
IGUI.visualize(sol)
