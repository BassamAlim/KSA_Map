import json
import xlrd
import pandas as pd
import openpyxl

"""with open('Cities.json', encoding='utf-8') as file:
    cities = json.load(file)

name = cities[0]['name']
print(name)"""""


loc = "neighbors.xlsx"

"""wb = xlrd.open_workbook_xls(loc)
sheet = wb.sheet_by_index(0)
print(sheet.cell_value(0, 0))"""""

data = pd.read_excel(loc)
#df = pd.DataFrame(data, )
#print(df)
print(data.loc[0, 0])
