#Definimos una función que aceptará como argumento un dataframe, en este caso será el extraído del dataset
import pandas as pd
def transform(df):
    df = df.dropna(subset=['id'])  #Eliminamos renglones que no tengan ID
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce') #Convertimos a numérico
    df = df[df['amount'].abs() < 1e9]  #Eliminamos montos grandes
    
    df.columns = df.columns.str.lower() #Para evitar problemas y errores, convertimos los nombres de las columnas a minusculas

    df['created_at'] = pd.to_datetime(df['created_at']) #Aquí convertimos el tiempo en texto originalmente a objeto datetime
    df['paid_at'] = pd.to_datetime(df['paid_at'], errors='coerce') #Lo mismo, pero aquí como a veces no hay valores,
    #entonces debemos de agregar un errors="coerce" para evitar errores y convertirlos en NaT

    df['amount'] = df['amount'].astype(float)   #Convierte los numeros de texto a flotante

    df['status'] = df['status'].str.lower() #Lo mismo aquí, convertimos los datos de la columna status a minusculas todas

    print("Transformación completada")

    return df   #Ya tenemos un dataframe mas limpio y listo para subir a la base de datos
