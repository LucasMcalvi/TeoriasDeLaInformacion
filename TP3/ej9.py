import math
import random


def get_alfabetoCodigo(palabras):
    """
    Obtiene el alfabeto codigo utilizado por las palabras recibidas.
    Recibe una lista de palabras codigo y devuelve una cadena con sus
    caracteres sin repetir y ordenados. Agrega los caracteres a un set,
    los ordena con sorted() y los une con join().
    """

    #update(palabra) agrega al conjunto cada carácter de la palabra, sin repetirlos. Luego sorted() los ordena y join() los une en una cadena.

    alfabeto = set()

    for palabra in palabras:
        alfabeto.update(palabra)

    return "".join(sorted(alfabeto))


def get_longitudes(palabras):
    """
    Calcula la longitud de cada palabra codigo.
    Recibe una lista de palabras codigo y devuelve una lista de enteros.
    Usa una comprension de listas para aplicar len() a cada palabra.
    """
    return [len(palabra) for palabra in palabras]


def calcular_kraft(palabras):
    """
    Calcula la sumatoria de la inecuacion de Kraft.
    Recibe una lista de palabras codigo y devuelve el valor de la suma.
    Obtiene la base r del alfabeto y suma r elevado a la longitud negativa
    de cada palabra.
    """
    alfabeto = get_alfabetoCodigo(palabras)
    L = get_longitudes(palabras)
    r = len(alfabeto)

    if r == 0:
        return 0

    return sum(r ** -longitud for longitud in L)
