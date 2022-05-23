import json
import threading
import time
import tkinter as tk

from tkintermapview import TkinterMapView

import processor
from Algorithms import Algorithms

algorithm = Algorithms.Empty
processor = processor
fuel = 15.0
showed = False

with open('Cities.json', encoding='utf-8') as file:
    data = json.load(file)

with open('table.json', encoding='utf-8') as file:
    table = json.load(file)


def formulate_route(route):
    string = str()
    for element in route:
        string += data[element]['name'] + ' ← '
    return string[:-3]


def on_search(text):
    pass


# ////////////////////////////////////////////   GUI   //////////////////////////////////////////////////////

bg = '#7E899C'
primary = '#C6CFDC'
surface = '#E1E7EF'
accent = '#14213d'

root = tk.Tk()
root.configure(background=bg)
chosen_algo = tk.StringVar()
entry = tk.StringVar()
entry.trace('w', callback=on_search(entry.get()))

scrollbar = tk.Scrollbar(root, background=bg)
frame = tk.Frame(root)

edit = tk.Entry(root, textvariable=entry)
checklist = tk.Text(root, width=20, background=primary)
result_tv = tk.Text(root, foreground='blue', wrap=tk.WORD, background=surface)
map_widget = TkinterMapView(root, width=1100, corner_radius=0, max_zoom=22)
algor_list = tk.OptionMenu(root, chosen_algo, *[option.value for option in Algorithms])
markers = []
added_markers = []
selected = []
paths = []


chosen_algo.set(Algorithms.Empty.value)


def start():
    root.geometry('1250x800')
    root.title("KSA MapView")
    root.state('zoomed')

    for i in range(0, len(data)):
        city = data[i]
        var = tk.IntVar()
        selected.append(var)
        markers.append(None)
        checkbutton = tk.Checkbutton(checklist, text=city['name'], variable=var, command=pin,
                                     font=("Times New Roman", 13), background=primary, foreground='black')
        checklist.window_create("end", window=checkbutton)
        checklist.insert("end", "\n")
        checklist.get()
    scrollbar.config(command=checklist.yview)
    checklist.config(yscrollcommand=scrollbar.set)
    checklist.configure(state="disabled")

    run_btn = tk.Button(root, text="Run", command=run, background=accent, foreground='white',
                        font=("Times New Roman", 20))

    map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga")
    map_widget.set_position(23.8859, 45.0792)  # KSA
    map_widget.set_zoom(6)

    result_tv.tag_configure("center", justify='center')

    scrollbar.place(x=0, y=35, height=400)
    edit.place(x=15, y=5, width=180, height=25)
    checklist.place(x=10, y=35, width=200, height=400)
    algor_list.place(x=5, y=450, width=200, height=30)
    run_btn.place(x=5, y=500, width=200, height=50)
    result_tv.place(x=5, y=570, width=210, height=70)
    map_widget.place(relx=0.60, rely=0.5, anchor='center', height=650)

    edit.focus_set()

    root.mainloop()


def run():
    threading.Thread(target=runner).start()


def runner():
    global showed, algorithm
    algorithm = Algorithms(chosen_algo.get())
    fun = function_finder.get(chosen_algo.get())
    clear_paths()
    route = get_selected()
    result = fun(route, visualize)
    display_results(result)
    visualize('Final result:', result.route, result.distance)
    showed = True


def visualize(what, route, cost):
    if len(route) < 2:
        return

    clear_paths()
    positions = []
    for i in range(0, len(route)):
        while len(added_markers) > 0:
            remove_marker(added_markers.pop())

        if markers[route[i]] is None:
            mark(route[i])
            added_markers.append(route[i])

        positions.append(markers[route[i]].position)
    show_on_tv(what, cost)
    path = map_widget.set_path(positions)
    paths.append(path)
    time.sleep(0.05)  # Delay


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


def remove_marker(cid):
    markers[cid].delete()
    selected[cid].set(0)


def clear_markers():
    for i in range(0, len(markers)):
        if markers[i] is not None:
            markers[i].delete()
            selected[i].set(0)


def clear_paths():
    for i in range(0, len(paths)):
        paths.pop().delete()


def get_selected():
    s = []
    for i in range(0, len(data)):
        if selected[i].get():
            s.append(i)
    return s


def display_results(result):
    print('\nSequence: ')
    print('Result: ')
    print("Path: ")
    print(formulate_route(result.route))
    print("Distance: " + str(result.distance))
    print("Cost: " + str(round(2.18 * int(result.distance / fuel))) + "\n")
    show_on_tv('Final result:', result.distance)


def show_on_tv(what, cost):
    result_tv.delete('1.0', tk.END)
    result_tv.insert("1.0", str(algorithm.value) + '\'s ' + what +
                     '\nDistance: ' + str(cost) + ' km\nCost: ' + str(round(2.18 * int(cost / fuel))) + " SR")
    result_tv.tag_add("center", "1.0", "end")


def no_choice():
    print('Please choose an algorithm')


function_finder = {
    'Pick an Algorithm': no_choice,
    'Breadth First Search': processor.bfs,
    'Uniform Cost Search': processor.ucs,
    'Iterative Deepening Search': processor.ids,
    'Greedy': processor.greedy,
    'A*': processor.a_star,
    'Hill Climbing': processor.hill_climbing,
    'Simulated Annealing': processor.simulated_annealing,
    'Genetic Algorithm': processor.genetic
}

start()
