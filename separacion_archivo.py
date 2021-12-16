#!/usr/bin/env python
import pandas as pd
import csv

archivocsv = "/home/raimundoosf/Escritorio/Proyecto2U2/drugsComTest_raw.csv"

"""convercion de lista a archivo csv"""
def convert_to_csv(data_name, data):

    # se definen las columnas del archvio csv
    columns = ["uniqueID", "drugName", "condition", "review", "date", "usefulCount"]
    
    # crea lista
    rows = []
    # se agregan lineas/filas a lista
    for index in range(0, len(data)):
        rows.append([data[index]["uniqueID"], data[index]["drugName"], data[index]["condition"],
                    data[index]["review"], data[index]["date"], data[index]["usefulCount"]])

    # se abre/crea archivo csv    
    with open(f'{data_name}.csv', 'w') as f:
        # usando csv.writer method desde CSV package
        write = csv.writer(f)

        write.writerow(columns)
        write.writerows(rows)


"""separacion de archivo scv por año"""
def separete_files():

    # se crea dataframe
    df = pd.read_csv(archivocsv)

    # se crea lista para simplificar algoritmia 
    data = ['data_2008', 'data_2009', 'data_2010', 'data_2011', 'data_2012',
            'data_2013', 'data_2014', 'data_2015', 'data_2016', 'data_2017']
    
    # se hace copia de lista
    data_aux = data[:]

    # crean listas dentro de copia de lista
    for index in range(0,len(data_aux)):
        data_aux[index] = []

    # abre ciclo
    for index in range(0,len(df.index)):
        # 'line' corresponde a linea especifica de 'dt'
        line = df.iloc[index]
        # abre ciclo interno
        for sub_index in range(0, len(data)):
            # si linea contiene ultimos dos caracteres de elemento en 'data'
            if line.str.contains(f'-{data[sub_index][-2:]}').any():
                # se identifica año respectivo de 'line'
                # se agrega 'line' a lista de año respectivo
                data_aux[sub_index].append(line)
                # se acaba ciclo interno
                break
            # no hay asociacion de año determinado en 'data' con 'line'
            else:
                # se continua a siguiente ciclo interno para evetual asociacion
                continue
    
    # abre ciclo for para convertir cada lista 'data_aux[]' a archivo csv
    for index in range(0,len(data)):
        # se llama a funcion
        convert_to_csv(data[index], data_aux[index])
    
if __name__ == "__main__":
    # Llama
    separete_files()
