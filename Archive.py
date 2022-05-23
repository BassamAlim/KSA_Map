# def setup_table():
#     for i in range(153):
#         table.append(list())
#
#     counter = 0
#     for i in range(153):
#         print(str(counter))
#         for j in range(153):
#             table[i].append(processor.a_star(i, j)[1].distance)
#         counter += 1
#
#     with open("table.json", "w") as f:
#         f.write(json.dumps(table))
