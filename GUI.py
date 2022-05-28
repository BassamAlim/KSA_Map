import json
import threading
import tkinter as tk
from tkinter import CENTER, TOP, BOTTOM, LEFT, RIGHT, X, Y, BOTH, VERTICAL, DISABLED, NORMAL

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
    text = entry.get()
    for widgets in frame.winfo_children():
        widgets.destroy()

    for i in range(0, len(data)):
        city = data[i]
        if city['name'].__contains__(text):
            checkbutton = tk.Checkbutton(frame, text=city['name'], variable=selected[city['cid']], command=pin,
                                         font=("Times New Roman", 13), background=primary, foreground='black')
            checkbutton.grid(row=i, column=1)


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

canvas = tk.Canvas(root, borderwidth=0)
frame = tk.Frame(canvas)
scrollbar = tk.Scrollbar(root, background=bg, orient=VERTICAL, command=canvas.yview)
edit = tk.Entry(root, textvariable=entry)
result_tv = tk.Text(root, foreground='blue', wrap=tk.WORD, background=surface)
map_widget = TkinterMapView(root, width=1100, corner_radius=0, max_zoom=22)
algor_list = tk.OptionMenu(root, chosen_algo, *[option.value for option in Algorithms])
run_btn = tk.Button(root, text="Run", command=run, background=accent, foreground='white', font=("Times New Roman", 20))

markers = []
added_markers = []
selected = []
paths = []
cbs = []



def start():
    root.geometry('1250x800')
    root.title("KSA MapView")
    root.state('zoomed')

    map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga")
    map_widget.set_position(23.8859, 45.0792)  # KSA
    map_widget.set_zoom(6)

    put()

    config()

    canvas.create_window((4, 4), window=frame, anchor="nw")
    frame.bind("<Configure>", lambda event, gCanvas=canvas: onFrameConfigure(gCanvas))
    populate(frame)

    edit.focus_set()

    root.mainloop()


def onFrameConfigure(canvas_to):
    canvas_to.configure(scrollregion=canvas_to.bbox("all"))


def populate(frame_to):
    for i in range(0, len(data)):
        city = data[i]
        var = tk.IntVar()
        selected.append(var)
        markers.append(None)
        checkbutton = tk.Checkbutton(frame_to, text=city['name'], variable=var, command=pin,
                                     font=("Times New Roman", 13), background=primary, foreground='black')
        checkbutton.grid(row=i, column=1)
        cbs.append(checkbutton)


def config():
    root.configure(background=bg)
    canvas.configure(yscrollcommand=scrollbar.set)
    result_tv.tag_configure(CENTER, justify=CENTER)


def put():
    map_widget.pack(side=RIGHT, fill=Y)
    scrollbar.pack(side=LEFT, anchor='nw', fill=Y)
    edit.pack(side=TOP, fill=X)
    canvas.pack(fill=BOTH, expand=True)
    frame.pack(fill=BOTH, expand=True)
    run_btn.pack(side=BOTTOM, fill=X)
    algor_list.pack(side=BOTTOM, fill=X)
    result_tv.pack(side=TOP, fill=X)


def runner():
    global showed, algorithm
    algorithm = Algorithms(chosen_algo.get())
    run_btn['state'] = DISABLED
    fun = function_finder.get(chosen_algo.get())
    clear_paths()
    route = get_selected()
    result = fun(route, visualize)
    display_results(result)
    visualize('Final result:', result.route, result.distance)
    run_btn['state'] = NORMAL
    showed = True


def visualize(what, route, cost):
    if len(route) < 2:
        return

    print(formulate_route(route))

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
    # time.sleep(0.05)  # Delay


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
    print("Path: " + formulate_route(result.route))
    print("Distance: " + str(result.distance))
    print("Cost: " + str(round(2.18 * int(result.distance / fuel))) + "\n")
    show_on_tv('Final result:', result.distance)


def show_on_tv(what, cost):
    result_tv.delete('1.0', tk.END)
    result_tv.insert("1.0", str(algorithm.value) + '\'s ' + what +
                     '\nDistance: ' + str(cost) + ' km\nCost: ' + str(round(2.18 * int(cost / fuel))) + " SR")
    result_tv.tag_add("center", "1.0", "end")


def formulate_route(route):
    string = str()
    for element in route:
        string += data[element]['name'] + ' ← '
    return string[:-3]


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
