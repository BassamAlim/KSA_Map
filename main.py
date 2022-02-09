import json


with open('Cities.json', encoding='utf-8') as file:
    text = json.load(file)


name = text[0]['name']
print(name)


def goal_test():
    return True





