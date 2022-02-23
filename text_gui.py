import tkinter.ttk
from tkinter import *
import json
import process

root = Tk()
# Adjust size
root.geometry("200x200")


def begin():
    process.Process(start_drop.current(), dest_drop.current())


with open('Cities.json', encoding='utf-8') as file:
    cities = json.load(file)


items = []
for city in cities:
    items.append(city['name'])

# Create Start City Dropdown menu
var1 = StringVar()
start_drop = tkinter.ttk.Combobox(root, textvariable=var1)
start_drop['values'] = items
start_drop['state'] = 'readonly'
start_drop.pack()

# Create Destination City Dropdown menu
var2 = StringVar()
dest_drop = tkinter.ttk.Combobox(root, textvariable=var2)
dest_drop['values'] = items
dest_drop['state'] = 'readonly'
dest_drop.pack()

# Create button, it will change label text
Button(root, text="click Me", command=begin).pack()

# Execute tkinter
root.mainloop()
