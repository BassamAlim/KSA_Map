import json
import tkinter as tk
from tkinter import LEFT

from tkintermapview import TkinterMapView

import LocalSearch

with open('Cities.json', encoding='utf-8') as file:
    cities = json.load(file)

root = tk.Tk()
map_widget = TkinterMapView(root, width=1100, height=650, corner_radius=0, max_zoom=22)
markers = []
selected = []


def start():
    root.geometry('1250x800')
    root.title("KSA MapView")
    root.state('zoomed')

    scrollbar = tk.Scrollbar(root)
    scrollbar.pack(side=tk.LEFT, fill=tk.Y)
    checklist = tk.Text(root, width=20)
    checklist.pack(side=tk.LEFT, anchor='nw')
    for i in range(0, len(cities)):
        city = cities[i]
        var = tk.IntVar()
        selected.append(var)
        checkbutton = tk.Checkbutton(checklist, text=city['name'], variable=var)
        checklist.window_create("end", window=checkbutton)
        checklist.insert("end", "\n")
    checklist.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=checklist.yview)
    # disable the widget so users can't insert text into it
    checklist.configure(state="disabled")

    hc_button = tk.Button(root, text="HC", command=hill_climbing)
    hc_button.pack(side=LEFT, padx=0, pady=0, anchor='sw')
    sa_button = tk.Button(root, text="SA", command=simulated_annealing)
    sa_button.pack(side=LEFT, padx=0, pady=0, anchor='sw')
    ga_button = tk.Button(root, text="GA", command=genetic)
    ga_button.pack(side=LEFT, padx=0, pady=0, anchor='sw')

    map_widget.place(relx=0.6, rely=0.5, anchor=tk.CENTER)
    map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga")
    # set current widget position and zoom
    map_widget.set_position(23.8859, 45.0792)  # KSA
    map_widget.set_zoom(6)

    map_widget.pack(fill='both', expand=True)
    checklist.pack(fill='y')
    root.mainloop()


def get_selected():
    s = []
    for i in range(0, len(cities)):
        if selected[i].get():
            s.append(i)
    return s


def pin(cid):
    pass


def hill_climbing():
    route = get_selected()
    result = LocalSearch.hill_climbing(route)
    visualize(result)


def simulated_annealing():
    route = get_selected()
    result = LocalSearch.simulated_annealing(route)
    visualize(result)


def genetic():
    route = get_selected()
    result = LocalSearch.genetic(route)
    visualize(result)


def visualize(route):
    positions = []
    for i in range(0, len(route)):
        city = cities[route[i]]
        marker = map_widget.set_marker(city['x'], city['y'], text=city['name'])
        markers.append(marker)
        positions.append(marker.position)
    path_1 = map_widget.set_path(positions)


start()
