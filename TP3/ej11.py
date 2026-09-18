import math
import random

def entropia_fuente(palabras, probabilidades):

    #calcula la entropia de la fuente a partir de una lista de  palabras codigo de una codificacion y sus probabilidades

    set_palabras = set("".join(palabras))
    base = len(set_palabras)

    return sum([p*math.log(1/p, base) for p in probabilidades if p>0])

def get_longitudMedia(palabras, probabilidades):

    #calcula la longitud media del codigo

    return sum([p*len(palabra) for palabra, p in zip (palabras, probabilidades)])