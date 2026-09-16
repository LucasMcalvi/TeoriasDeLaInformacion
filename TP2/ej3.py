import math
import random

def Equiprobables (cant): #dada la cantidad de sucesos equiprobables calcula la entropia
    return math.log2(cant)

probabilidades = [1/9, 1/6, 1/9, 1/9, 1/6, 1/3]

def CalcEntropia (probabilidades): #dado un vector de probabilidades, calcula la entropia
    return sum([p*math.log2(1/p) for p in probabilidades])