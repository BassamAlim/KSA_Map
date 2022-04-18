import json
import tkinter as tk
from tkinter import RIGHT, LEFT

from tkintermapview import TkinterMapView

with open('Cities.json', encoding='utf-8') as file:
    cities = json.load(file)


def visualize(route):
    # create tkinter window
    root_tk = tk.Tk()

    root_tk.geometry('1250x800')
    root_tk.title("KSA MapView")
    root_tk.state('zoomed')

    scrollbar = tk.Scrollbar(root_tk)
    scrollbar.pack(side=tk.LEFT, fill=tk.Y)

    checklist = tk.Text(root_tk, width=20)
    checklist.pack(side=tk.LEFT)

    vars = []
    for city in cities:
        var = tk.IntVar()
        vars.append(var)
        checkbutton = tk.Checkbutton(checklist, text=city['name'], variable=var)
        checklist.window_create("end", window=checkbutton)
        checklist.insert("end", "\n")

    checklist.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=checklist.yview)

    # disable the widget so users can't insert text into it
    checklist.configure(state="disabled")

    run_button = tk.Button(root_tk, text="RUN", command=run)
    run_button.place(x=1000, y=2000)

    # create map widget
    map_widget = TkinterMapView(root_tk, width=1100, height=650, corner_radius=0)
    map_widget.place(relx=0.6, rely=0.5, anchor=tk.CENTER)
    map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google normal

    # set current widget position and zoom
    map_widget.set_position(23.8859, 45.0792)  # KSA
    map_widget.set_zoom(6)

    # set current widget position by address
    # map_widget.set_address("Saudi Arabia")

    # set marker position by address
    # marker_1 = map_widget.set_address("Riyadh", marker=True)
    # marker_1.set_text("الرياض")  # set new text

    # set markers
    markers = []
    positions = []
    for i in range(0, len(route)):
        city = cities[route[i]]
        marker = map_widget.set_marker(city['x'], city['y'], text=city['name'])
        markers.append(marker)
        positions.append(marker.position)

    # marker_1.delete()

    # set path
    path_1 = map_widget.set_path(positions)
    # path_1.add_position(...)
    # path_1.remove_position(...)
    # path_1.delete()

    run_button.pack(side=LEFT, padx=10, pady=30)
    root_tk.mainloop()


def run():
    pass

visualize([0, 2, 22, 45, 103])
