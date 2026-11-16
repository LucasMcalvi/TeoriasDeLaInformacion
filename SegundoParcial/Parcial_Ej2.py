"""
Parcial - Ejercicio 2 (canal a partir de secuencias + paridad cruzada)
=====================================================================
Plantilla: en el parcial SOLO hay que cambiar ENTRADA y SALIDA.
Archivo AUTOCONTENIDO (no importa nada propio; solo math). Antes necesitaba: Formulas.py, Func_clase4.py y Func_clase6.py.
"""
import math

_TOL = 1e-9

# ======================================================================
# FUNCIONES (copiadas de Formulas, FormulasCodificacion y Func_claseN
# para que este archivo funcione solo, sin importar módulos propios)
# ======================================================================


# --- CalcEntropia (de Formulas.py)
def CalcEntropia(probs):
    return sum((p * math.log2(1 / p) for p in probs if p > 0))


# --- GeneraAlfabetoYProb (de Formulas.py)
def GeneraAlfabetoYProb(mensaje):
    alf = sorted(set(mensaje))
    return (alf, [mensaje.count(c) / len(mensaje) for c in alf])


# --- filas_de_bits (de Func_clase4.py)
def filas_de_bits(cadena, ancho=8):
    cadena = cadena.strip()
    if len(cadena) % ancho:
        raise ValueError(f'La cadena tiene {len(cadena)} bits, que no es múltiplo de {ancho}.')
    return [cadena[i:i + ancho] for i in range(0, len(cadena), ancho)]


# --- analizar_matriz_paridad (de Func_clase4.py)
def analizar_matriz_paridad(filas):
    filas = [str(f) for f in filas]
    if not filas:
        raise ValueError('La matriz está vacía.')
    if any((len(f) != 8 or set(f) - {'0', '1'} for f in filas)):
        raise ValueError("Cada fila debe ser un string de 8 bits ('0'/'1').")
    bits = [[int(b) for b in f] for f in filas]
    filas_err = [i for i, fila in enumerate(bits) if sum(fila) % 2]
    cols_err = [j for j in range(8) if sum((fila[j] for fila in bits)) % 2]
    resultado = {'estado': None, 'filas_con_error': [i + 1 for i in filas_err], 'columnas_con_error': [j + 1 for j in cols_err], 'posicion_error': None, 'matriz_corregida': None, 'mensaje': ''}
    if not filas_err and (not cols_err):
        resultado['estado'] = 'sin_errores'
        corregida = filas
    elif len(filas_err) == 1 and len(cols_err) == 1:
        i, j = (filas_err[0], cols_err[0])
        bits[i][j] ^= 1
        corregida = [''.join(map(str, fila)) for fila in bits]
        resultado['estado'] = 'corregido'
        resultado['posicion_error'] = (i + 1, j + 1)
    else:
        resultado['estado'] = 'no_corregible'
        return resultado
    resultado['matriz_corregida'] = corregida
    resultado['mensaje'] = ''.join((chr(int(f[:7], 2)) for f in corregida[1:]))
    return resultado


# --- _validar_matriz (de Func_clase6.py)
def _validar_matriz(matriz):
    if not matriz or not matriz[0]:
        raise ValueError('La matriz del canal está vacía.')
    s = len(matriz[0])
    for i, fila in enumerate(matriz):
        if len(fila) != s:
            raise ValueError('Todas las filas de la matriz deben tener la misma cantidad de columnas.')
        if any((p < -1e-09 or p > 1 + 1e-09 for p in fila)):
            raise ValueError(f'La fila {i} tiene valores fuera de [0, 1].')
        if abs(sum(fila) - 1) > 1e-06:
            raise ValueError(f'La fila {i} suma {sum(fila)}; cada fila debe sumar 1.')


# --- _validar_canal (de Func_clase6.py)
def _validar_canal(probs, matriz):
    _validar_matriz(matriz)
    if len(probs) != len(matriz):
        raise ValueError('Debe haber una probabilidad a priori por cada fila de la matriz.')
    if any((p < 0 for p in probs)) or abs(sum(probs) - 1) > 1e-06:
        raise ValueError('Las probabilidades a priori deben ser no negativas y sumar 1.')


# --- _columna (de Func_clase6.py)
def _columna(matriz, j):
    return [fila[j] for fila in matriz]


# --- canal_desde_secuencias (de Func_clase6.py)
def canal_desde_secuencias(entrada, salida):
    if len(entrada) != len(salida):
        raise ValueError('Las secuencias de entrada y salida deben tener la misma longitud.')
    if not entrada:
        raise ValueError('Las secuencias están vacías.')
    alfabeto_a, probs = GeneraAlfabetoYProb(entrada)
    alfabeto_b = sorted(set(salida))
    matriz = []
    for a in alfabeto_a:
        salidas_de_a = [b for x, b in zip(entrada, salida) if x == a]
        matriz.append([salidas_de_a.count(b) / len(salidas_de_a) for b in alfabeto_b])
    return (alfabeto_a, probs, alfabeto_b, matriz)


# --- probabilidades_salida (de Func_clase6.py)
def probabilidades_salida(probs, matriz):
    _validar_canal(probs, matriz)
    s = len(matriz[0])
    return [sum((probs[i] * matriz[i][j] for i in range(len(probs)))) for j in range(s)]


# --- probabilidades_simultaneas (de Func_clase6.py)
def probabilidades_simultaneas(probs, matriz):
    _validar_canal(probs, matriz)
    return [[probs[i] * p for p in fila] for i, fila in enumerate(matriz)]


# --- probabilidades_a_posteriori (de Func_clase6.py)
def probabilidades_a_posteriori(probs, matriz):
    conjunta = probabilidades_simultaneas(probs, matriz)
    salida = probabilidades_salida(probs, matriz)
    return [[conjunta[i][j] / salida[j] if salida[j] > 0 else 0.0 for j in range(len(salida))] for i in range(len(probs))]


# --- equivocacion (de Func_clase6.py)
def equivocacion(probs, matriz):
    conjunta = probabilidades_simultaneas(probs, matriz)
    post = probabilidades_a_posteriori(probs, matriz)
    return sum((conjunta[i][j] * math.log2(1 / post[i][j]) for i in range(len(probs)) for j in range(len(matriz[0])) if conjunta[i][j] > 0))


# --- perdida (de Func_clase6.py)
def perdida(probs, matriz):
    conjunta = probabilidades_simultaneas(probs, matriz)
    return sum((conjunta[i][j] * math.log2(1 / matriz[i][j]) for i in range(len(probs)) for j in range(len(matriz[0])) if conjunta[i][j] > 0))


# --- informacion_mutua (de Func_clase6.py)
def informacion_mutua(probs, matriz):
    conjunta = probabilidades_simultaneas(probs, matriz)
    salida = probabilidades_salida(probs, matriz)
    return sum((conjunta[i][j] * math.log2(conjunta[i][j] / (probs[i] * salida[j])) for i in range(len(probs)) for j in range(len(salida)) if conjunta[i][j] > 0))


# --- es_sin_ruido (de Func_clase6.py)
def es_sin_ruido(matriz):
    _validar_matriz(matriz)
    return all((sum((1 for p in _columna(matriz, j) if p > _TOL)) == 1 for j in range(len(matriz[0]))))


# --- es_determinante (de Func_clase6.py)
def es_determinante(matriz):
    _validar_matriz(matriz)
    return all((sum((1 for p in fila if p > _TOL)) == 1 for fila in matriz))


# --- canal_serie (de Func_clase6.py)
def canal_serie(matriz1, matriz2):
    _validar_matriz(matriz1)
    _validar_matriz(matriz2)
    if len(matriz1[0]) != len(matriz2):
        raise ValueError('Las salidas del primer canal deben ser las entradas del segundo.')
    t = len(matriz2[0])
    return [[sum((fila[k] * matriz2[k][j] for k in range(len(fila)))) for j in range(t)] for fila in matriz1]


# --- es_reduccion_suficiente (de Func_clase6.py)
def es_reduccion_suficiente(matriz, j, k):
    _validar_matriz(matriz)
    s = len(matriz[0])
    if not (0 <= j < s and 0 <= k < s) or j == k:
        raise ValueError('Los índices deben ser dos columnas distintas de la matriz.')
    cj, ck = (_columna(matriz, j), _columna(matriz, k))
    sj, sk = (sum(cj), sum(ck))
    return all((abs(x * sk - y * sj) < 1e-09 for x, y in zip(cj, ck)))


# --- matriz_determinante_reduccion (de Func_clase6.py)
def matriz_determinante_reduccion(matriz, j, k):
    _validar_matriz(matriz)
    s = len(matriz[0])
    if not (0 <= j < s and 0 <= k < s) or j == k:
        raise ValueError('Los índices deben ser dos columnas distintas de la matriz.')
    menor, mayor = (min(j, k), max(j, k))
    determinante = []
    for b in range(s):
        destino = menor if b == mayor else b if b < mayor else b - 1
        determinante.append([1.0 if c == destino else 0.0 for c in range(s - 1)])
    return determinante


# --- reducir_canal (de Func_clase6.py)
def reducir_canal(matriz, pasos=False):
    _validar_matriz(matriz)
    actual = [list(fila) for fila in matriz]
    historial = [actual]
    hubo_cambio = True
    while hubo_cambio and len(actual[0]) > 1:
        hubo_cambio = False
        s = len(actual[0])
        for j in range(s):
            for k in range(j + 1, s):
                if es_reduccion_suficiente(actual, j, k):
                    actual = canal_serie(actual, matriz_determinante_reduccion(actual, j, k))
                    historial.append(actual)
                    hubo_cambio = True
                    break
            if hubo_cambio:
                break
    return historial if pasos else actual


# --- _es_permutacion (de Func_clase6.py)
def _es_permutacion(a, b):
    return all((abs(x - y) < 1e-09 for x, y in zip(sorted(a), sorted(b))))


# --- es_uniforme (de Func_clase6.py)
def es_uniforme(matriz):
    _validar_matriz(matriz)
    filas_ok = all((_es_permutacion(fila, matriz[0]) for fila in matriz))
    columnas = [_columna(matriz, j) for j in range(len(matriz[0]))]
    columnas_ok = all((len(c) == len(columnas[0]) and _es_permutacion(c, columnas[0]) for c in columnas))
    return filas_ok and columnas_ok


# --- capacidad_canal (de Func_clase6.py)
def capacidad_canal(matriz):
    if es_determinante(matriz):
        usadas = sum((1 for j in range(len(matriz[0])) if any((p > _TOL for p in _columna(matriz, j)))))
        return (math.log2(usadas), 'determinante')
    if es_sin_ruido(matriz):
        return (math.log2(len(matriz)), 'sin ruido')
    if es_uniforme(matriz):
        return (math.log2(len(matriz[0])) - CalcEntropia(matriz[0]), 'uniforme')
    return (None, 'sin fórmula directa')


# --- capacidad_binaria (de Func_clase6.py)
def capacidad_binaria(matriz, paso):
    _validar_matriz(matriz)
    if len(matriz) != 2:
        raise ValueError('El canal debe tener exactamente 2 entradas.')
    if not 0 < paso <= 1:
        raise ValueError('El paso debe estar entre 0 y 1.')
    cantidad = int(1 / paso + 1e-09)
    mejor_c, mejor_p = (-1.0, 0.0)
    for i in range(cantidad + 1):
        p = min(i * paso, 1.0)
        c = informacion_mutua([p, 1 - p], matriz)
        if c > mejor_c + 1e-12:
            mejor_c, mejor_p = (c, p)
    return (mejor_c, mejor_p)


# --- probabilidad_error (de Func_clase6.py)
def probabilidad_error(probs, matriz, a_posteriori=False):
    conjunta = probabilidades_simultaneas(probs, matriz)
    aciertos = 0.0
    for j in range(len(matriz[0])):
        criterio = _columna(conjunta, j) if a_posteriori else _columna(matriz, j)
        elegida = criterio.index(max(criterio))
        aciertos += conjunta[elegida][j]
    return 1 - aciertos


# ======================================================================
# RESOLUCIÓN
# ======================================================================

# ------------------------- DATOS DEL PARCIAL -------------------------
ENTRADA = "10100000101011101001111110011001"   # parcial 2025
SALIDA = "QQPQQPPQQQPQRRRQSPQSQRQSQQPSQQPP"
# ---------------------------------------------------------------------


def ver(matriz):
    for fila in matriz:
        print("   " + "  ".join(f"{p:.4f}" for p in fila))


# 1) Probabilidades a priori y matriz del canal
alf_a, probs, alf_b, matriz = canal_desde_secuencias(ENTRADA, SALIDA)
for a, p in zip(alf_a, probs):
    print(f"P({a}) = {p:.4f}")
print("Matriz del canal (filas:", alf_a, " columnas:", alf_b, ")")
ver(matriz)

# 2) Clasificación
sin_ruido, determinante = es_sin_ruido(matriz), es_determinante(matriz)
clase = {(True, True): "Ambos", (True, False): "Sin ruido",
         (False, True): "Determinante", (False, False): "Ninguno"}[(sin_ruido, determinante)]
print("Clasificación del canal:", clase)

# 3) Equivocación, pérdida e información mutua
print(f"H(A/B) = {equivocacion(probs, matriz):.4f}")
print(f"H(B/A) = {perdida(probs, matriz):.4f}")
print(f"I(A,B) = {informacion_mutua(probs, matriz):.4f}")

# 4) Reducciones suficientes
pasos = reducir_canal(matriz, pasos=True)
for k, m in enumerate(pasos[1:], 1):
    print(f"Reducción {k}:")
    ver(m)
if len(pasos) == 1:
    print("El canal no admite reducciones suficientes (no hay columnas proporcionales).")
reducido = pasos[-1]
print(f"I(A,B) del canal reducido = {informacion_mutua(probs, reducido):.4f} (tiene que ser igual)")

# 5) Capacidad y probabilidad de error
if len(reducido) == 2:   # entrada binaria: se busca la P(0) que maximiza I(A,B)
    c, p = capacidad_binaria(reducido, 0.0001)
    print(f"C(A,B) = {c:.4f}   con P({alf_a[0]}) = {p:.4f}  P({alf_a[1]}) = {1 - p:.4f}")
else:
    c, tipo = capacidad_canal(reducido)
    print(f"C(A,B) = {c} ({tipo})")
print(f"P_E = {probabilidad_error(probs, matriz):.4f}  (máxima posibilidad)")
print(f"P_E = {probabilidad_error(probs, matriz, a_posteriori=True):.4f}  (máxima prob. a posteriori)")

# 6) Detectar / corregir errores en la entrada (ASCII + paridad VRC, LRC y cruzada)
res = analizar_matriz_paridad(filas_de_bits(ENTRADA))
print("Paridad:", res["estado"], "| filas con error:", res["filas_con_error"],
      "| columnas con error:", res["columnas_con_error"], "| bit corregido (fila, col):",
      res["posicion_error"])
print("Mensaje corregido:", res["mensaje"] if res["mensaje"] else "(no se puede corregir)")