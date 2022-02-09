import json

x = '{"name":"john", "age":"30", "city":"New York"}'

y = json.loads(x)

print(y["age"])
