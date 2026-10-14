"""
import math
import random
import Formulas
import FormulasCodificacion
import muestraPasoAPasoFunciones as pasos
import examen1
import examen3


mensaje = ";;,;,;:,,,.;,,.,,,::,;;;,:;.,,;:,,,:..;,;;.,;,,.:;"

alfabeto, prob = Formulas.GeneraAlfabetoYProb(mensaje)
alfabeto, matriz = Formulas.generaalfabetoyTransicion(mensaje)
memoriaNoNula = Formulas.tieneMemoriaNoNula(matriz, 0.01)
if not memoriaNoNula:
    entropia = Formulas.CalcEntropia(prob)
    alfext2, probext2 = Formulas.DevuelveExtyFdp(alfabeto, prob, 2)
    entrext2 = 2 * entropia
else:
    vector = Formulas.generaVectorEstacionario(matriz, len(alfabeto))
    entropia = Formulas.calculaEntropiaMarkovOrden1(matriz, vector)

print("Alfabeto: ", alfabeto)
print("Probabilidades ",  prob)
examen1.imprimirMatriz(alfabeto, matriz)
print(matriz)
print("Memoria no nula: " ,memoriaNoNula)
print("Entropia: " , entropia)
if memoriaNoNula:
    print("Vector estacionario: " ,vector)
else:
    print(Formulas.obtenerDatosSimbolo(alfext2, probext2, [",;", ":."]))
    print("H^2 = ", entrext2)
    print(Formulas.CalcEntropia(probext2))

"""