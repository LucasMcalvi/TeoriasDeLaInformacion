"""
import math
import random
import Formulas
import FormulasCodificacion
import muestraPasoAPasoFunciones as pasos
import examen1
import examen3

cadena = ["/+", "*", "+-", "-", "*/"]
prob = [0.15, 0.25, 0.05, 0.45, 0.10]

alfcod = FormulasCodificacion.get_alfabetoCodigo(cadena)
entropia = FormulasCodificacion.entropia_fuente(cadena, prob)
longmedia = FormulasCodificacion.get_longitudMedia(cadena, prob)
kraft = FormulasCodificacion.calcular_kraft(cadena)
clasifiacion = FormulasCodificacion.clasifica(cadena)
compacto = FormulasCodificacion.es_compacto(cadena, prob)
sardinas = FormulasCodificacion.es_univocamente_decodificable(cadena, True)

print("Cadena: ", cadena)
print("Alfabeto codigo: ", alfcod)
print("entropia: ", entropia)
print("Longitud media: ", longmedia)
print("Kraft: ", kraft)
print("Clasificacion: ", clasifiacion)
print("Compacto: ", compacto)
"""