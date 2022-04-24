import json
import math
import random
import time
import tkinter as tk
from enum import Enum
from random import randint

from tkintermapview import TkinterMapView

import process
from models import Chromosome

processor = process

showed = False


class Algorithms(Enum):
    Empty = 'Nothing'
    HC = 'Hill Climbing'
    SA = 'Simulated Annealing'
    GA = 'Genetic Algorithms'


algorithm = Algorithms.Empty

with open('Cities.json', encoding='utf-8') as file:
    data = json.load(file)


def hill_climbing(cities):
    global algorithm
    algorithm = Algorithms.HC
    sequence = list(cities)
    start_time = time.time()
    random.shuffle(cities)
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
    return sequence, cities, calc_cost(cities)


def simulated_annealing(cities):
    global algorithm
    algorithm = Algorithms.SA
    sequence = list(cities)
    start_time = time.time()
    iterations = 0
    random.shuffle(cities)
    best_sol = list(cities)
    best_sol_cost = calc_cost(cities)
    temperature = 3000
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
    print('Time: ' + str(time.time() - start_time))
    return sequence, best_sol, best_sol_cost


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
    sequence = list(cities)
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
        gnome = list(cities)
        random.shuffle(cities)
        population.append(Chromosome(gnome, calc_cost(gnome)))

    temperature = 3000
    # Iteration to perform population crossing and gene mutation.
    while temperature > 500 and gen <= gen_thres:
        population.sort()
        display_gen(gen, population)
        solution, sol_cost = get_best(solution, sol_cost, population)    # Python Stuff

        new_population = []
        for i in range(POP_SIZE):
            parent = population[i]

            while True:
                new_g = mutate(parent.gnome)
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

    solution, sol_cost = get_best(solution, sol_cost, population)
    display_gen(gen, population)
    return sequence, solution, sol_cost


# Function to return a mutated GNOME.
# Mutated GNOME is a string with a random interchange of two genes to create variation in species
def mutate(gnome):
    gnome = list(gnome)
    while True:
        r1 = randint(1, v-1)
        r2 = randint(1, v-1)
        if r1 != r2:
            swap(gnome, r1, r2)
            break
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






root = tk.Tk()
map_widget = TkinterMapView(root, width=1100, corner_radius=0, max_zoom=22)
result_tv = tk.Text(root, foreground='blue')
markers = []
selected = []
paths = []


def start():
    root.geometry('1250x800')
    root.title("KSA MapView")
    root.state('zoomed')

    scrollbar = tk.Scrollbar(root)
    checklist = tk.Text(root, width=20)
    for i in range(0, len(data)):
        markers.append(None)
        city = data[i]
        var = tk.IntVar()
        selected.append(var)
        checkbutton = tk.Checkbutton(checklist, text=city['name'], variable=var, command=pin)
        checklist.window_create("end", window=checkbutton)
        checklist.insert("end", "\n")
    checklist.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=checklist.yview)
    checklist.configure(state="disabled")

    hc_button = tk.Button(root, text="HC", command=HC)
    sa_button = tk.Button(root, text="SA", command=SA)
    ga_button = tk.Button(root, text="GA", command=GA)

    map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga")
    map_widget.set_position(23.8859, 45.0792)  # KSA
    map_widget.set_zoom(6)

    scrollbar.place(x=0, y=0, height=650)
    checklist.place(x=10, y=0, height=550)
    hc_button.place(x=5, y=555, width=50, height=50)
    sa_button.place(x=60, y=555, width=50, height=50)
    ga_button.place(x=115, y=555, width=50, height=50)
    result_tv.place(x=5, y=610, width=170, height=30)
    map_widget.place(relx=0.57, rely=0.5, anchor='center', height=650)

    root.mainloop()


def get_selected():
    s = []
    for i in range(0, len(data)):
        if selected[i].get():
            s.append(i)
    return s


def pin():
    global showed
    if showed:
        clear_paths()
        clear_markers()
        showed = False

    for i in range(0, len(data)):
        if selected[i].get():
            if markers[i] is None:
                mark(i)
        else:
            if markers[i] is not None:
                markers[i].delete()
                selected[i].set(0)
            markers[i] = None


def mark(cid):
    marker = map_widget.set_marker(data[cid]['x'], data[cid]['y'], text=data[cid]['name'])
    markers[cid] = marker
    return marker


def clear_paths():
    for i in range(0, len(paths)):
        paths.pop().delete()


def clear_markers():
    for i in range(0, len(markers)):
        if markers[i] is not None:
            markers[i].delete()
            selected[i].set(0)


def HC():
    global showed
    clear_paths()
    route = get_selected()
    result = hill_climbing(route)
    result_tv.delete('1.0', tk.END)
    result_tv.insert(tk.END, 'HC:' + str(result[2]) + 'km')
    display_results(result)
    visualize(result[1])
    showed = True


def SA():
    global showed
    clear_paths()
    route = get_selected()
    result = simulated_annealing(route)
    result_tv.delete('1.0', tk.END)
    result_tv.insert(tk.END, 'SA:' + str(result[2]) + 'km')
    display_results(result)
    visualize(result[1])
    showed = True


def GA():
    global showed
    clear_paths()
    route = get_selected()
    result = genetic(route)
    result_tv.delete('1.0', tk.END)
    result_tv.insert(tk.END, 'GA:' + str(result[2]) + 'km')
    display_results(result)
    visualize(result[1])
    showed = True


def display_sequence(route):
    string = str()
    string += '('
    for element in route:
        string += data[element]['name'] + ', '
    string = string[:-2]
    string += ')'
    print(string)


def display_results(result):
    fuel = 15.0
    print('\nSequence: ')
    display_sequence(result[0])
    print('Result: ')
    print("Path: ")
    formulate_route(result[1])
    print("Distance: " + str(result[2]))
    print("Cost: " + str(round(2.18 * int(result[2] / fuel))) + "\n")


def visualize(route):
    positions = []
    for i in range(0, len(route)):
        positions.append(markers[route[i]].position)
    path = map_widget.set_path(positions)
    paths.append(path)


start()
