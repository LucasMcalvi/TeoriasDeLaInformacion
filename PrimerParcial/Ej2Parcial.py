"""
import math
import random
import Formulas
import FormulasCodificacion
import muestraPasoAPasoFunciones as pasos

codigo = ["/+", "*", "+-", "-", "*/"]
prob = [0.15, 0.25, 0.05, 0.45, 0.10]

alfCodigo = FormulasCodificacion.get_alfabetoCodigo(codigo)
print(alfCodigo)
entropiaFuente = FormulasCodificacion.entropia_fuente(codigo, prob)
longmedia = FormulasCodificacion.get_longitudMedia(codigo, prob)
kraft = FormulasCodificacion.calcular_kraft(codigo)
clasificacion = FormulasCodificacion.clasifica(codigo)
compacto = FormulasCodificacion.es_compacto(codigo, prob)
sardinas = FormulasCodificacion.es_univocamente_decodificable(codigo, mostrar=True)
sard = pasos.es_univocamente_decodificable(codigo, True)
"""