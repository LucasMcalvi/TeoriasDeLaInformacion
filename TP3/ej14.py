import math
import random
import ej6

def es_compacto(palabras, probabilidades):

    #Devuelve True si es compacto o False si no lo es

    if (ej6.es_univocamente_decodificable(palabras)):
        base = len(set("".join(palabras)))

        for palabra, p in zip(palabras, probabilidades):
            if not len(palabra) <= math.ceil(math.log(1/p, base)):
                return False

        return True
    else:
        return False