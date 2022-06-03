import json
import random
import threading
import time
import tkinter as tk
from tkinter import CENTER, BOTH, VERTICAL, DISABLED, NORMAL, NW, LEFT, RIGHT, TOP, BOTTOM, X, Y

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


def on_search(name, index, op):
    for widgets in frame.winfo_children():
        widgets.destroy()

    text = entry.get()
    pop = []
    for i in range(0, len(data)):
        city = data[i]
        if len(text) < 1 or city['name'].__contains__(text):
            pop.append(city)

    populate(pop)


def clear_selection():
    for s in selected:
        s.set(0)
    clear_markers()
    clear_paths()
    populate(data)


def random_selection():
    rand = list(range(len(selected)))
    random.shuffle(rand)
    for i in range(15):
        selected[rand[i]].set(1)
        mark(rand[i])
    populate(data)


def run():
    threading.Thread(target=runner).start()


bg = '#7E899C'
primary = '#C6CFDC'
surface = '#E1E7EF'
accent = '#14213d'

root = tk.Tk()

chosen_algo = tk.StringVar()
chosen_algo.set(Algorithms.Empty.value)
entry = tk.StringVar()
entry.trace('w', callback=on_search)

map_widget = TkinterMapView(root, width=1000, corner_radius=0, max_zoom=22)
edit = tk.Entry(root, textvariable=entry)
canvas = tk.Canvas(root, background=primary)
frame = tk.Frame(canvas, background=primary)
scrollbar = tk.Scrollbar(canvas, orient=VERTICAL, command=canvas.yview)
clear_btn = tk.Button(root, text="clear", background=surface, command=clear_selection, font=(None, 12))
random_btn = tk.Button(root, text="Random", background=surface, command=random_selection, font=(None, 12))
algo_list = tk.OptionMenu(root, chosen_algo, *[option.value for option in Algorithms])
run_btn = tk.Button(root, height=1, text="Run", command=run, background=accent, foreground='white',
                    font=("Times New Roman", 20))
speed_label = tk.Label(root, text="Speed", background=bg)
speed_bar = tk.Scale(root, from_=1, to=100, orient=tk.HORIZONTAL, background=surface)
result_tv = tk.Text(root, height=5, background=surface, foreground='blue', wrap=tk.WORD)

markers = []
added_markers = []
selected = []
paths = []

cf = str()


def init_arrays():
    for _ in data:
        var = tk.IntVar()
        selected.append(var)
        markers.append(None)


def start():
    init_arrays()

    root.geometry('1250x800')
    root.title("KSA MapView")
    root.state('zoomed')

    map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga")
    map_widget.set_position(23.5859, 44.7)  # KSA
    map_widget.set_zoom(6)

    config()
    put()

    global cf
    cf = canvas.create_window((0, 0), window=frame, anchor=NW)
    canvas.bind('<Configure>', on_frame_configure)

    populate(data)

    edit.focus_set()

    root.mainloop()


def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas_width = event.width
    canvas.itemconfig(cf, width=canvas_width)


def populate(population):
    for p in population:
        checkbutton = tk.Checkbutton(frame, text=p['name'], variable=selected[p['cid']], command=pin,
                                     font=("Times New Roman", 13), background=primary)
        checkbutton.pack(fill=BOTH)


def config():
    root.configure(background=bg)
    canvas.configure(yscrollcommand=scrollbar.set)
    algo_list.config(background=surface, font=('Times new roman', 12))
    result_tv.tag_configure(CENTER, justify=CENTER)
    speed_bar.set(90)


def put():
    map_widget.pack(side=RIGHT, fill=Y)
    edit.pack(side=TOP, fill=X, padx=8, pady=(8, 2), ipady=2)
    canvas.pack(side=TOP, fill=BOTH, expand=True, padx=8)
    scrollbar.pack(side=LEFT, fill=Y)
    frame.pack(side=RIGHT, fill=BOTH)
    result_tv.pack(side=BOTTOM, fill=X, padx=8, pady=8)
    speed_bar.pack(side=BOTTOM, fill=X, padx=8, pady=5)
    speed_label.pack(side=BOTTOM, anchor=tk.W)
    run_btn.pack(side=BOTTOM, fill=X, padx=8, pady=5)
    algo_list.pack(side=BOTTOM, fill=X, padx=8, pady=5)
    clear_btn.pack(side=RIGHT, fill=X, expand=True, padx=(2, 8), pady=(2, 5))
    random_btn.pack(side=LEFT, fill=X, expand=True, padx=(8, 2), pady=(2, 5))


def runner():
    if chosen_algo.get() == Algorithms.Empty.value:
        print('Please choose an algorithm')
        return

    global showed, algorithm
    algorithm = Algorithms(chosen_algo.get())
    set_controls_mode(DISABLED)
    fun = function_finder.get(chosen_algo.get())
    clear_paths()

    route = get_selected()
    result = fun(route, visualize)
    print("Path: " + formulate_route(result.route))
    visualize('Final result:', result.route, result.distance, result.run_time)

    set_controls_mode(NORMAL)
    showed = True


def visualize(what, route, cost, run_time=0):
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
    show_on_tv(what, cost, run_time)
    path = map_widget.set_path(positions)
    paths.append(path)
    time.sleep(0.5 - speed_bar.get() / 200)  # Delay


def pin():
    global showed
    if showed:
        clear_paths()
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


def set_controls_mode(mode):
    run_btn['state'] = mode
    algo_list['state'] = mode
    clear_btn['state'] = mode
    random_btn['state'] = mode


def show_on_tv(what, cost, run_time):
    result_tv.delete('1.0', tk.END)

    if run_time != 0:
        result_tv.insert("1.0", str(algorithm.value) + '\'s ' + what +
                         '\nDistance: ' + str(cost) + ' km' +
                         '\nCost: ' + str(round(2.18 * int(cost / fuel))) + ' SR' +
                         '\nRunning Time ' + str(round(run_time, 3)))
    else:
        result_tv.insert("1.0", str(algorithm.value) + '\'s ' + what +
                         '\nDistance: ' + str(cost) + ' km' +
                         '\nCost: ' + str(round(2.18 * int(cost / fuel))) + ' SR')

    result_tv.tag_add("center", "1.0", "end")


def formulate_route(route):
    string = str()
    for element in route:
        string += data[element]['name'] + ' ← '
    return string[:-3]


function_finder = {
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
