"""
Ejemplo de uso de Explicaciones.py con los datos del parcial 2025.
ESTE ARCHIVO NO SE ENTREGA: es para leer las interpretaciones mientras
escribís las respuestas. Lo que se entrega es Parcial_Ej1.py / Parcial_Ej2.py.

Necesita en la misma carpeta: FuncionesParcial2.py y Explicaciones.py.

Para el parcial: cambiá MENSAJE, N, ENTRADA y SALIDA y corrélo.
"""
from Explicaciones import *

# ========================= EJERCICIO 1 =========================
MENSAJE = "GIIHGGGHGIHHIHIIGFHH"
N = 3

alfabeto, probs = explicar(alfabeto_y_probabilidades, MENSAJE)
explicar(CalcEntropia, probs)
codigo = explicar(huffman, probs)
explicar(tasa_compresion_codigo, MENSAJE, alfabeto, codigo)
explicar(resumen_codigo, probs, codigo)                  # L, η, R de la fuente
explicar(cumple_primer_teorema, probs, codigo, 1)        # Shannon para la fuente
ext = explicar_extension(probs, N)                       # L, η, R de la extensión
explicar(cumple_primer_teorema, probs, ext["codigo"], N) # Shannon para la extensión

explicacion_ej1(MENSAJE, N)     # -> pregunta "Explicar cómo se obtuvieron los resultados"
print()
conclusiones_ej1(MENSAJE, N)    # -> pregunta "Analizar los resultados y concluir"
print("\n" * 3)

# ========================= EJERCICIO 2 =========================
ENTRADA = "10100000101011101001111110011001"
SALIDA = "QQPQQPPQQQPQRRRQSPQSQRQSQQPSQQPP"

A, probs, B, matriz = explicar(canal_desde_secuencias, ENTRADA, SALIDA)
explicar(es_sin_ruido, matriz)
explicar(es_determinante, matriz)
explicar(equivocacion, probs, matriz)
explicar(perdida, probs, matriz)
explicar(informacion_mutua, probs, matriz)
reducido = explicar(reducir_canal, matriz)
explicar(capacidad_binaria, reducido, 0.0001)
explicar(probabilidad_error, probs, matriz)
explicar(analizar_matriz_paridad, filas_de_bits(ENTRADA))

explicacion_ej2(ENTRADA, SALIDA)
print()
conclusiones_ej2(ENTRADA, SALIDA)

# Otras que también se pueden explicar (ver la lista completa con ayuda()):
#   explicar(analizar_codigo_hamming, ["0000", "0011", "1010", "0101"])
#   explicar(distancia_levenshtein, "casa", "calle")
#   explicar(shannon_fano, probs)
#   explicar(rlc_comprimir, "AAAABBBCCDAA")
#   explicar(entropias_a_posteriori, probs, matriz)
#   explicar(canal_serie, matriz1, matriz2)
