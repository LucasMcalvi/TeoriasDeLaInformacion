import math
import ej2
import ej3

cadena = "ABDAACAABACADAABDAADABDAAABDCDCDCDC"
alfabeto, probabilidades = ej2.GeneraAlfabetoYProb(cadena) #devuelve array alfabeto y probabilidades
print("Probabilidades: ", probabilidades)
print("Entropia: ", ej3.CalcEntropia (probabilidades)) #devuelve entropia
