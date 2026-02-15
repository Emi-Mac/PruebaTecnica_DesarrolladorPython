#Aquí vamos a iniciar el pipeline, primero extraeremos los datos del dataset usando la librería pandas
import pandas as pd

#Creamos una función que extraerá los datos del dataset que se adjuntó
def extract(path):
    df = pd.read_csv(path)  #Leemos con pandas el archivo csv y guardamos los datos en un dataframe
    print("Datos extraídos correctamente")  #Imprimimos que se han extraído los datos correctamente
    return df   #Ahora tenemos listos los datos para su manipulación
