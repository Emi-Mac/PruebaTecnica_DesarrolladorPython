class NumberSet:
    def __init__(self):
        #Aquí defino el conjunto original, que deben ser los primeros 100 numeros naturales
        self.set_original = set(range(1, 101))  #Pongo range(1,101) ya que el range va a tomar del 1-100
        self.set_actual = self.set_original.copy()  #Inicialmente definimos al set actual como una copia del original

    #Creamos el método extract
    def Extract(self, num: int):
        #Primero hay que verificar que cumpla el número proporcionado por el usuario con los requisitos
        if num < 1 or num > 100:   #Verificamos que el número sea un natural entre 1-100
            raise ValueError("El número debe ser un natural menor o igual a 100")
        
        if num not in self.set_actual:  #Aquí se verifica que el número no haya sido extraído anteriormente
            raise ValueError("El número ya ha sido extraído")
        
        self.set_actual.remove(num)   #Si se cumple con los requisitos, entonces se quita el número del conjunto actual

    #Creamos un método para calcular el número faltante
    def encontrarFaltante(self):
        sumacien = 5050
        sumafaltante = sum(self.set_actual)
        return sumacien - sumafaltante