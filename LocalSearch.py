import json
import math
import random
import threading
import time
import tkinter as tk
from enum import Enum
from random import randint

from tkintermapview import TkinterMapView

import process
from models import Chromosome


class Algorithms(Enum):
    Empty = 'Nothing'
    HC = 'Hill Climbing'
    SA = 'Simulated Annealing'
    GA = 'Genetic Algorithms'


processor = process
showed = False
fuel = 15.0
algorithm = Algorithms.Empty

with open('Cities.json', encoding='utf-8') as file:
    data = json.load(file)


def hill_climbing(cities):
    start_time = time.time()
    global algorithm
    algorithm = Algorithms.HC
    counter = 0

    sequence = list(cities)
    random.shuffle(cities)
    while counter < 10:
        print(formulate_route(cities))
        current_cost = calc_cost(cities)

        tries = 0
        while tries < 10:
            ss = find_swap(len(cities))
            swapped = list(cities)
            swap(swapped, ss[0], ss[1])
            new_cost = calc_cost(swapped)
            if new_cost < current_cost:
                print('Swap benefit: ' + str(current_cost - new_cost))
                cities = swapped
                current_cost = new_cost
                break
            tries += 1
        visualize('Current:', cities, current_cost)

        if str(counter) == state_et.get("1.0", "end-1c"):
            display_state(cities, current_cost)

        counter += 1

    print('Time: ' + str(time.time() - start_time))
    cities.append(cities[0])  # To return to start city
    return sequence, cities, calc_cost(cities)


def simulated_annealing(cities):
    start_time = time.time()
    global algorithm
    algorithm = Algorithms.SA
    counter = 0

    sequence = list(cities)
    iterations = 0
    random.shuffle(cities)
    best_sol = list(cities)
    best_sol_cost = calc_cost(cities)
    temperature = 3000
    while temperature > 500:
        iterations += 1
        print(formulate_route(cities))
        current_cost = calc_cost(cities)

        tries = 0
        while tries < 10:
            ss = find_swap(len(cities))
            swapped = list(cities)
            swap(swapped, ss[0], ss[1])
            new_cost = calc_cost(swapped)

            diff = current_cost - new_cost
            prob = get_prob(current_cost, new_cost, temperature)
            if diff > 0 or (diff > -200 and prob > 0.5):
                print('Swap benefit: ' + str(current_cost - new_cost))
                cities = swapped
                current_cost = new_cost
                break

            tries += 1

        visualize('Current:', cities, current_cost)

        if current_cost < best_sol_cost:
            best_sol = cities
            best_sol_cost = current_cost

        if str(counter) == state_et.get("1.0", "end-1c"):
            display_state(cities, current_cost)

        temperature = cooldown(temperature)
        counter += 1

    print('Time: ' + str(time.time() - start_time))
    best_sol.append(best_sol[0])
    return sequence, best_sol, best_sol_cost


def find_swap(length):
    while True:
        r1 = randint(0, length - 1)
        r2 = randint(0, length - 1)
        if r1 != r2:
            return r1, r2


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
        solution, sol_cost = get_best(solution, sol_cost, population)  # Python Stuff
        visualize('Current:', population[0].gnome, population[0].fitness)

        if str(gen) == state_et.get("1.0", "end-1c"):
            display_state(cities, calc_cost(cities))

        new_population = []
        for i in range(POP_SIZE):
            parent = population[i]

            while True:
                new_g = mutate(parent.gnome)
                new_gnome = Chromosome(new_g, calc_cost(new_g))

                if new_gnome.fitness <= population[i].fitness:
                    new_population.append(new_gnome)
                    break
                else:  # Accepting the rejected children at a possible probability above threshold.
                    prob = get_prob(population[i].fitness, new_gnome.fitness, temperature)
                    if prob > 0.5:
                        new_population.append(new_gnome)
                        break

        temperature = cooldown(temperature)
        population = new_population
        gen += 1

    solution, sol_cost = get_best(solution, sol_cost, population)
    display_gen(gen, population)

    solution.append(solution[0])
    return sequence, solution, sol_cost


# Function to return a mutated GNOME.
# Mutated GNOME is a string with a random interchange of two genes to create variation in species
def mutate(gnome):
    gnome = list(gnome)
    while True:
        r1 = randint(1, v - 1)
        r2 = randint(1, v - 1)
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
    return cost + processor.a_star(route[len(route) - 1], route[0])[1].distance  # To return to the start city


def formulate_route(route):
    string = str()
    for element in route:
        string += data[element]['name'] + ' ← '
    return string[:-3]


root = tk.Tk()
map_widget = TkinterMapView(root, width=1100, corner_radius=0, max_zoom=22)
state_label = tk.Label(root, text='Show state after:')
state_et = tk.Text(root, foreground='black')
state_tv = tk.Text(root, foreground='blue', wrap=tk.WORD)
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

    hc_button = tk.Button(root, text="HC", command=bg_hc)
    sa_button = tk.Button(root, text="SA", command=bg_sa)
    ga_button = tk.Button(root, text="GA", command=bg_ga)

    map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga")
    map_widget.set_position(23.8859, 45.0792)  # KSA
    map_widget.set_zoom(6)

    state_et.tag_configure("center", justify='center')
    state_tv.tag_configure("center", justify='center')
    result_tv.tag_configure("center", justify='center')

    scrollbar.place(x=0, y=0, height=420)
    checklist.place(x=10, y=0, width=200, height=420)
    state_label.place(x=0, y=425, width=100, height=20)
    state_et.place(x=100, y=425, width=50, height=20)
    hc_button.place(x=5, y=450, width=60, height=50)
    sa_button.place(x=70, y=450, width=60, height=50)
    ga_button.place(x=135, y=450, width=60, height=50)
    state_tv.place(x=5, y=505, width=210, height=90)
    result_tv.place(x=5, y=600, width=210, height=40)
    map_widget.place(relx=0.60, rely=0.5, anchor='center', height=650)

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


def bg_hc():
    thread = threading.Thread(target=HC)
    thread.start()


def bg_sa():
    thread = threading.Thread(target=SA)
    thread.start()


def bg_ga():
    thread = threading.Thread(target=GA)
    thread.start()


def HC():
    global showed
    clear_paths()
    route = get_selected()
    result = hill_climbing(route)
    display_results(result)
    visualize('Final result:', result[1], result[2])
    showed = True


def SA():
    global showed
    clear_paths()
    route = get_selected()
    result = simulated_annealing(route)
    display_results(result)
    visualize('Final result:', result[1], result[2])
    showed = True


def GA():
    global showed
    clear_paths()
    route = get_selected()
    result = genetic(route)
    display_results(result)
    visualize('Final result:', result[1], result[2])
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
    print('\nSequence: ')
    display_sequence(result[0])
    print('Result: ')
    print("Path: ")
    print(formulate_route(result[1]))
    print("Distance: " + str(result[2]))
    print("Cost: " + str(round(2.18 * int(result[2] / fuel))) + "\n")
    show_on_tv('Final result:', result[2])


def show_on_tv(what, cost):
    result_tv.delete('1.0', tk.END)
    result_tv.insert("1.0", what +
                     '\nDistance: ' + str(cost) + ' km\nCost: ' + str(round(2.18 * int(cost / fuel))) + " SR")
    result_tv.tag_add("center", "1.0", "end")


def display_state(path, cost):
    path_str = formulate_route(path)
    cost_str = str(cost) + ' km, ' + str(round(2.18 * int(cost / fuel))) + " SR"

    print('\n///////////////////////////////////////////////////////////////////////////////////')
    print("Selected iteration path: " + path_str)
    print('Selected iteration cost: ' + cost_str)
    print('///////////////////////////////////////////////////////////////////////////////////\n')

    state_tv.delete('1.0', tk.END)
    state_tv.insert("1.0", 'Path: ' + path_str + '\nCost: ' + cost_str)
    state_tv.tag_add("center", "1.0", "end")


def visualize(what, route, cost):
    clear_paths()
    positions = []
    for i in range(0, len(route)):
        positions.append(markers[route[i]].position)
    show_on_tv(what, cost)
    path = map_widget.set_path(positions)
    paths.append(path)


start()
