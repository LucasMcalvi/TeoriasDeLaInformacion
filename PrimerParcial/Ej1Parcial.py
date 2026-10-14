"""
import math
import random
import Formulas
import FormulasCodificacion
import muestraPasoAPasoFunciones as pasos

mensaje = "-+-+*//++///*/-////+---////-+/+--+-+/-/+-+/-+*++//"

alfabeto, prob = Formulas.GeneraAlfabetoYProb(mensaje)
alfabeto, matriz = Formulas.generaalfabetoyTransicion(mensaje)
noNula = Formulas.tieneMemoriaNoNula(matriz, 0.001)
print(noNula)
vector = Formulas.generaVectorEstacionario(matriz, 4)
entropia = Formulas.calculaEntropiaMarkovOrden1(matriz,vector)

print(alfabeto,"\n", prob,"\n", matriz,"\n", noNula,"\n", entropia,"\n")
print(vector)

print(pasos._mostrar_matriz(matriz, alfabeto, True))
print(pasos.generaalfabetoyTransicion(mensaje, True))
"""