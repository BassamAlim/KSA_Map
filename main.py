import json

with open('Cities.json', encoding='utf-8') as file:
    cities = json.load(file)

name = cities[0]['name']
print(name)
