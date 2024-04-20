import os
import shutil


folder_path = 'C:\\Users\\994387\\Downloads\\'
lista = []
for filename in os.listdir(folder_path):
    if 'query_export_results' in filename:
        lista.append(str(filename))
        
lista = sorted(lista, key=len)
print(lista)

csvPath = folder_path + lista[-1]

import pandas as pd

import zipfile

with zipfile.ZipFile(csvPath, 'r') as zip_ref:
    zip_ref.extractall(folder_path)

"""    
erroresLotesProd = pd.read_csv('C:\\Users\\994387\\Downloads\\Material Information.csv')
print(erroresLotesProd.head())

with zipfile.ZipFile(csvPath) as myzip:
    with myzip.open('query_export_results.csv') as myfile:
        nombresErrores = pd.read_csv(myfile)

print(nombresErrores.head())
"""
