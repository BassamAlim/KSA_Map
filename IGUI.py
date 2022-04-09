import json
import tkinter
from tkintermapview import TkinterMapView


with open('Cities.json', encoding='utf-8') as file:
    cities = json.load(file)


def visualize(route):
    # create tkinter window
    root_tk = tkinter.Tk()

    root_tk.geometry(f"{1250}x{800}")
    root_tk.title("KSA MapView")
    root_tk.state('zoomed')

    # create map widget
    map_widget = TkinterMapView(root_tk, width=1300, height=650, corner_radius=0)
    map_widget.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
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

    root_tk.mainloop()


r = [0, 20, 43, 101]
visualize(r)
