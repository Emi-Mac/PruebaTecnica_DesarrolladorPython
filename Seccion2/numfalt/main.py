from fastapi import FastAPI, HTTPException      #Importamos la clase principal para crear API (FastAPI) y HTTPException para devolver errores de comunicación
from numfalt.number_set import NumberSet    #Aquí importamos la clase que cree y que se llama number_Set

app = FastAPI()     #Con esto creamos una instancia web

number_set = NumberSet()    #Creamos una instancia de la clase que creamos anteriormente

@app.post("/extract/{num}")     #Creamos un endpoint, la ruta dinámica para la extración del número
def extract_number(num: int):   #Esta es la función que ejecutará la ruta
    try:
        number_set.Extract(num)     #Llamamos al método Extract de la clase que creamos y eliminamos el valor solicitado
        missing = number_set.encontrarFaltante()    #Calculamos el número faltante con el método encontrarFaltante
        return {
            "mensaje": f"Número {num} extraído correctamente",
            "numero_faltante_calculado": missing        #Imprimimos mensajes de confirmación y el número calculado faltante en formato JSON
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))     #Estamos usando un bloque Try para imprimir el error
                                                                #ya sea de conexión o de validación especificados en
                                                                #la clase que se creó.

#Para cumplir con que la aplicación debe de poder ejecutarse con un argumento introducido por el usuario, hacemos lo siguiente:

if __name__ == "__main__":      #Aquí indicamos que solo se ejecute el bloque si es ejecutado directo en terminal
    import sys      #Importamos sys para que nos de información del sistema y además acceder a argumentos de la terminal

    if len(sys.argv) != 2:      #sys.argv es una lista que contiene los argumentos de la terminal, esta condicional
                                #nos indica que debe ser de la forma python main.py {número}, si se da menos o más argumentos
                                #entonces nos despliega un mensaje y se acaba la ejecución.
        print("Uso: python main.py <numero>")       
        exit(1)

    try:       #Nuevamente usamos un bloque Try para manejar los errores y mensajes de errores
        num = int(sys.argv[1])   #Convertimos el segundo argumento, que es el número que se desea extraer a entero
        number_set = NumberSet()    #Creamos una instancia de la clase que creamos anteriormente
        number_set.Extract(num)     #Extraemos el número que el usuario indica en el argumento
        print(f"Se extrajo el número: {num}")
        print(f"El número calculado faltante es: {number_set.encontrarFaltante()}")

    except ValueError as e:
        print(f"Error: {e}")
