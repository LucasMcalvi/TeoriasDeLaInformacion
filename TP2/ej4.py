import math
import random

alfabeto = ["x","y","z"]
probabilidades = [0.5, 0.1, 0.4]

def CalcInformacion (probabilidades): #dado una lista de probabilidades, devuelve una lista con informacion
    return [math.log2(1/p) for p in probabilidades]

infoxsimbolo = CalcInformacion(probabilidades)