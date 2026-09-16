import math
import random

def es_noSingular(codigo): #devuelve si un codigo es no singular
    return len(codigo) == len(set(codigo))

def es_instantaneo(palabras):
    n = len(palabras)
    for i in range(n):
        for j in range(n):
            if i != j:
                if palabras[j].startswith(palabras[i]): #En Python, "cadena_larga".startswith("cadena_corta") devuelve True si la cadena corta es efectivamente el prefijo inicial de la larga.
                    return False
    return True

def es_univocamente_decodificable(palabras):
    """
    Implementa el algoritmo de Sardinas-Patterson.
 
    Idea: si una palabra A es prefijo de otra palabra B, el "resto"
    de B (lo que sobra despues de sacarle el prefijo A) queda como
    una secuencia "colgando". Si ese resto eventualmente coincide
    con una palabra codigo original, significa que se puede armar
    la misma secuencia de bits/simbolos de dos formas distintas
    a partir de los simbolos fuente -> el codigo NO es univoco.
 
    Pasos:
      1. Calculamos C1: todos los restos que salen de comparar
         las palabras originales entre si.
      2. Iteramos generando C2, C3, ... combinando los restos
         del paso anterior con las palabras originales.
      3. Cortamos si:
         - un resto coincide con una palabra original -> NO univoco
         - el conjunto de restos queda vacio -> SI univoco
         - el conjunto de restos ya aparecio antes (ciclo) -> SI univoco
    """
    
    palabras_set = set(palabras)
 

 
    # Paso 1: C1 = restos de comparar las palabras originales entre si
    c_actual = calcular_restos(palabras, palabras)
 
    historial = [c_actual]
 
    while True:
        # Condicion de NO univoco: algun resto coincide con una palabra original
        if c_actual & palabras_set:
            return False
 
        # Condicion de SI univoco: no quedan mas restos por resolver
        if not c_actual:
            return True
 
        # Generamos el siguiente conjunto de restos:
        # combinamos los restos actuales con las palabras originales
        # en ambas direcciones (resto vs palabra, y palabra vs resto)
        siguiente = calcular_restos(c_actual, palabras) | calcular_restos(palabras, c_actual)
 
        # Condicion de SI univoco: si este conjunto ya aparecio antes,
        # estamos en un ciclo que nunca va a generar una colision real
        if siguiente in historial:
            return True
 
        historial.append(siguiente)
        c_actual = siguiente

def calcular_restos(conjunto_a, conjunto_b):
    """
    Compara cada elemento de conjunto_a contra cada elemento de
    conjunto_b. Si uno es prefijo del otro (y no son iguales),
    guarda el resto (la parte que sobra) en un set nuevo.
    """
    restos = set()
    for a in conjunto_a:
        for b in conjunto_b:
            if a == b:
                continue
            if b.startswith(a):
                resto = b[len(a):]
                if resto:  # descartamos el resto vacio (a == b ya se filtro)
                    restos.add(resto)
    return restos


codigos = ["011", "0111", "01", "0", "011111", "01111"]
print(es_univocamente_decodificable(codigos))  # True