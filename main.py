import json


with open('Cities.json', encoding='utf-8') as file:
    text = json.load(file)

print(text[0])
