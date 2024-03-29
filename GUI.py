import json
import random
import threading
import time
import tkinter as tk
from tkinter import CENTER, BOTH, VERTICAL, HORIZONTAL, DISABLED, NORMAL, NW, LEFT, RIGHT, X, Y
from tkinter.ttk import Progressbar

from tkintermapview import TkinterMapView

import processor
from Algorithms import Algorithms


algorithm = Algorithms.Empty
RANDOM_SELECTION_SIZE = 20
showed = False
stop = False
running = False

with open('Cities.json', encoding='utf-8') as file:
    data = json.load(file)
with open('table.json', encoding='utf-8') as file:
    table = json.load(file)


def on_search(name, index, op):
    for widgets in frame.winfo_children():
        widgets.destroy()
    pop = []
    text = entry.get()
    for i in range(0, len(data)):
        city = data[i]
        if len(text) < 1 or city['name'].__contains__(text):
            pop.append(city)

    populate(pop)


def random_selection():
    rand = list(range(len(selected)))
    random.shuffle(rand)
    count = 0
    i = 0
    while count < RANDOM_SELECTION_SIZE and i < len(rand):
        if selected[rand[i]].get() == 0:
            selected[rand[i]].set(1)
            mark(rand[i])
            count += 1
        i += 1
    populate(data)


def clear_selection():
    for s in selected:
        s.set(0)
    clear_paths()
    clear_markers()
    populate(data)


def run():
    global running, stop
    if running:
        stop = True
    else:
        stop = False
        threading.Thread(target=runner).start()
        running = True


# colors
bg ='#7E899C'
primary ='#C6CFDC'
surface ='#E1E7EF'
accent ='#14213d'
active ='#D18E21'

root = tk.Tk()

chosen_algo = tk.StringVar()
chosen_algo.set(Algorithms.Empty.value)

entry = tk.StringVar()
entry.trace('w', callback=on_search)

map_widget = TkinterMapView(root, width=1000, corner_radius=0)
edit = tk.Entry(root, textvariable=entry)

canvas = tk.Canvas(root, background=primary)
frame = tk.Frame(canvas, background=primary)
scrollbar = tk.Scrollbar(canvas, orient=VERTICAL, command=canvas.yview)

btns_frame = tk.Frame(root, background=primary)
clear_btn = tk.Button(btns_frame, text="Clear", background=surface, command=clear_selection, font=(None, 12))
random_btn = tk.Button(btns_frame, text="Random", background=surface, command=random_selection, font=(None, 12))

algo_list = tk.OptionMenu(root, chosen_algo, *[option.value for option in Algorithms])
run_btn = tk.Button(root, width=15, height=1, text="Run", command=run, background=accent, foreground='white',
                    font=("Times New Roman", 18))

speed_frame = tk.Frame(root, background=primary)
speed_label = tk.Label(speed_frame, text="Speed", background=primary)
speed_bar = tk.Scale(speed_frame, from_=1, to=100, orient=tk.HORIZONTAL, background=primary)

progress = Progressbar(root, orient=HORIZONTAL, length=100, mode='determinate')

result_tv = tk.Text(root, height=4, background=surface, foreground='blue', wrap=tk.WORD)

markers = []
added_markers = []
selected = []
paths = []

cf = str()


def start():
    init_arrays()

    root.geometry('1250x800')
    root.title("KSA MapView")
    root.state('zoomed')

    map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga")
    map_widget.set_position(23.5859, 44.7)  # KSA
    map_widget.set_zoom(6)

    put()
    config()

    populate(data)

    edit.focus_set()

    root.mainloop()


def init_arrays():
    for _ in data:
        var = tk.IntVar()
        selected.append(var)
        markers.append(None)


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
    global cf
    root.configure(background=bg)
    canvas.configure(yscrollcommand=scrollbar.set)
    cf = canvas.create_window((0, 0), window=frame, anchor=NW)
    canvas.bind('<Configure>', on_frame_configure)
    algo_list.config(background=surface, font=('Times new roman', 12))
    result_tv.tag_configure(CENTER, justify=CENTER)
    speed_bar.set(100)


def put():
    map_widget.pack(side=RIGHT, fill=Y)
    edit.pack(fill=X, padx=8, pady=(8, 2), ipady=2)
    canvas.pack(fill=BOTH, expand=True, padx=8)
    scrollbar.pack(side=LEFT, fill=Y)
    frame.pack(side=RIGHT, fill=BOTH)
    btns_frame.pack(fill=X, padx=(8, 8), pady=(2, 5))
    random_btn.pack(side=LEFT, fill=X, expand=True)
    clear_btn.pack(side=RIGHT, fill=X, expand=True)
    algo_list.pack(fill=X, padx=8, pady=5)
    run_btn.pack(fill=X, padx=8, pady=5)
    speed_frame.pack(fill=X, padx=(8, 8), pady=(2, 5))
    speed_label.pack(side=LEFT, anchor=tk.W)
    speed_bar.pack(side=RIGHT, fill=X, expand=True, padx=8, pady=5)
    progress.pack(fill=X, padx=8, pady=5)
    result_tv.pack(fill=X, padx=8, pady=8)


def runner():
    route = get_selected()
    if len(route) < 2:
        show_on_tv('Please choose some cities', 0, 0, massage=True)
        return
    elif chosen_algo.get() == Algorithms.Empty.value:
        show_on_tv('Please choose an Algorithm', 0, 0, massage=True)
        return

    global showed, algorithm, running
    algorithm = Algorithms(chosen_algo.get())
    set_controls_mode(DISABLED)
    fun = function_finder.get(chosen_algo.get())
    clear_paths()

    result = fun(route, visualize, lambda: stop)
    running = False
    if result.route is None or len(result.route) == 0:
        clear_paths()
        clear_markers()
        visualize(None, result.distance, 0, 'Final result:', result.run_time)
        show_on_tv('{} Cancelled'.format(algorithm.value), 0, 0, massage=True)
    else:
        visualize(result.route, result.distance, 100, 'Final result:', result.run_time)
    set_controls_mode(NORMAL)
    showed = True


def visualize(route, cost, perc, title='Current',  run_time=0):
    if route is not None:
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
        show_on_tv(title, cost, run_time)
        path = map_widget.set_path(positions)
        paths.append(path)
    progress['value'] = perc
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
    while len(paths) != 0:
        paths.pop().delete()


def get_selected():
    s = []
    for i in range(0, len(data)):
        if selected[i].get():
            s.append(i)
    return s


def set_controls_mode(mode):
    if mode == DISABLED:
        if algorithm == Algorithms.HC or algorithm == Algorithms.SA or algorithm == Algorithms.GA:
            run_btn['text'] = 'Accept Current Best'
        else:
            run_btn['text'] = 'Cancel'
    elif mode == NORMAL:
        run_btn['text'] = 'Run'
    algo_list['state'] = mode
    clear_btn['state'] = mode
    random_btn['state'] = mode


def show_on_tv(what, cost, run_time, massage=False):
    result_tv.delete('1.0', tk.END)
    if massage:
        result_tv.insert("1.0", what)
    elif run_time != 0:
        result_tv.insert("1.0", "{} \'s {}\nDistance: {} km\nRunning Time: {} seconds"
                         .format(algorithm.value, what, cost, round(run_time, 3)))
    else:
        result_tv.insert("1.0", "{}\'s {}\nDistance: {} km".format(algorithm.value, what, cost))
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
