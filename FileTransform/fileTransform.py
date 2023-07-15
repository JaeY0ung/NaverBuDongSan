import pandas as pd
import csv

def csv_to_excel(area):
    csvReader = pd.read_csv(f"./csv/{area}.csv")
    xlsxWriter = pd.ExcelWriter(f'./excel/data_sheet.xlsx')
    csvReader.to_excel(xlsxWriter, sheet_name=area, index = False)
    xlsxWriter.close()

def load_csv(csvfile):
    data = []
    with open(csvfile, newline="") as file:
        csvReader = csv.DictReader(file)
        for row in csvReader:
            data.append(row)
    return data
