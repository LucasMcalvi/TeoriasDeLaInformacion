"""
ResolverParcial.py
==================
UN SOLO ARCHIVO PARA TODO EL PARCIAL.

1. Pegá los datos en el bloque DATOS DEL PARCIAL (abajo).
2. Corré:   python ResolverParcial.py
3. Te imprime, en orden:
     PARTE 1  RESPUESTAS PARA LOS CASILLEROS (los números, 4 decimales)
     PARTE 2  EXPLICACIÓN DE CADA RESULTADO (qué significa + frase)
     PARTE 3  TEXTOS PARA "EXPLICAR" Y "CONCLUIR" de cada ejercicio
     PARTE 4  EXTRAS por si piden algo más (Shannon-Fano, RLC, a posteriori, ...)
   Todo queda guardado también en  resultado_parcial.txt  (en la misma carpeta).

Necesita en la misma carpeta: FuncionesParcial2.py y Explicaciones.py.
ESTE ARCHIVO NO SE ENTREGA. Lo que se entrega es Parcial_Ej1.py / Parcial_Ej2.py.
"""

# ============================ DATOS DEL PARCIAL ============================
# Ejercicio 1: el mensaje de la fuente y el orden de la extensión.
MENSAJE = "GIIHGGGHGIHHIHIIGFHH"
N = 3

# Ejercicio 2: secuencias de entrada y salida del canal.
ENTRADA = "10100000101011101001111110011001"
SALIDA = "QQPQQPPQQQPQRRRQSPQSQRQSQQPSQQPP"

# Opcionales (dejar vacíos si no los piden):
CODIGO_HAMMING = []          # ej.: ["0000", "0011", "1010", "0101"] -> distancia de Hamming del código
LEVENSHTEIN = ("", "")       # ej.: ("casa", "calle")               -> distancia de Levenshtein
# ===========================================================================

from Explicaciones import *
from Explicaciones import _imprimir


def mostrar(*partes):
    """Como print: imprime en pantalla y lo anota para guardarlo en resultado_parcial.txt."""
    _imprimir(" ".join(str(p) for p in partes))


def titulo(texto):
    mostrar("\n" + "#" * 78 + "\n#  " + texto + "\n" + "#" * 78 + "\n")


def f4(x):
    return f"{x:.4f}"


def ver_matriz(m, filas, cols):
    mostrar("        " + "".join(f"{str(c):>9}" for c in cols))
    for a, fila in zip(filas, m):
        mostrar(f"   {str(a):>4} " + "".join(f"{x:9.4f}" for x in fila))


hay_ej1 = bool(MENSAJE)
hay_ej2 = bool(ENTRADA) and bool(SALIDA)
if hay_ej2 and len(ENTRADA) != len(SALIDA):
    mostrar(f"ERROR: ENTRADA tiene {len(ENTRADA)} símbolos y SALIDA {len(SALIDA)}; tienen que tener el mismo largo.")
    hay_ej2 = False
es_binaria = hay_ej2 and set(ENTRADA) <= {"0", "1"} and len(ENTRADA) % 8 == 0 and len(ENTRADA) >= 16

# =============================== CÁLCULOS ==================================
if hay_ej1:
    alfabeto, probs1 = alfabeto_y_probabilidades(MENSAJE)
    codigo = huffman(probs1)
    r1 = resumen_codigo(probs1, codigo)
    probs_ext = extension_fuente(probs1, N)
    codigo_ext = huffman(probs_ext)
    rn = resumen_codigo(probs_ext, codigo_ext)
    d1 = detalle_primer_teorema(probs1, codigo, 1)
    dn = detalle_primer_teorema(probs1, codigo_ext, N)
    tasa = tasa_compresion_codigo(MENSAJE, alfabeto, codigo)

if hay_ej2:
    A, probs2, B, matriz = canal_desde_secuencias(ENTRADA, SALIDA)
    sin_ruido, determinante = es_sin_ruido(matriz), es_determinante(matriz)
    clase = {(True, True): "Ambos", (True, False): "Sin ruido",
             (False, True): "Determinante", (False, False): "Ninguno"}[(sin_ruido, determinante)]
    h_ab, h_ba, i_ab = equivocacion(probs2, matriz), perdida(probs2, matriz), informacion_mutua(probs2, matriz)
    reducido = reducir_canal(matriz)
    if len(matriz) == 2:
        cap, p_cap = capacidad_binaria(reducido, 0.0001)
    else:
        cap, _tipo = capacidad_canal(reducido)
        p_cap = None
    pe = probabilidad_error(probs2, matriz)
    paridad = analizar_matriz_paridad(filas_de_bits(ENTRADA)) if es_binaria else None

# ===================== PARTE 1: RESPUESTAS (CASILLEROS) =====================
titulo("PARTE 1 - RESPUESTAS PARA LOS CASILLEROS")

if hay_ej1:
    mostrar("EJERCICIO 1")
    mostrar("  a) Probabilidades:")
    for s, p in zip(alfabeto, probs1):
        mostrar(f"       P({s}) = {f4(p)}")
    mostrar(f"     Entropía H(S) = {f4(r1['H'])}")
    mostrar("  b) Código óptimo (Huffman) para la fuente:")
    for s, c in zip(alfabeto, codigo):
        mostrar(f"       {s} -> {c}")
    mostrar(f"  c) Tasa de compresión = {f4(tasa)} : 1")
    mostrar(f"  d) Código óptimo para la extensión de orden {N}: {len(codigo_ext)} palabras (ver PARTE 4)")
    mostrar("  e) Código para la fuente:")
    mostrar(f"       L = {f4(r1['L'])}   η = {f4(r1['rendimiento'])}   R = {f4(r1['redundancia'])}")
    mostrar(f"     Código para la extensión de orden {N}:")
    mostrar(f"       L = {f4(rn['L'])}   η = {f4(rn['rendimiento'])}   R = {f4(rn['redundancia'])}"
          f"   (L/{N} = {f4(rn['L'] / N)} por símbolo)")
    mostrar("  f) Primer Teorema de Shannon:")
    mostrar(f"       Fuente:    {'Cumple' if d1['cumple'] else 'No cumple'}   "
          f"({f4(d1['H'])} <= {f4(d1['Ln_sobre_n'])} < {f4(d1['cota_superior'])})")
    mostrar(f"       Extensión: {'Cumple' if dn['cumple'] else 'No cumple'}   "
          f"({f4(dn['H'])} <= {f4(dn['Ln_sobre_n'])} < {f4(dn['cota_superior'])})")
    mostrar("")

if hay_ej2:
    mostrar("EJERCICIO 2")
    mostrar("  a) Probabilidades a priori:")
    for a, p in zip(A, probs2):
        mostrar(f"       P({a}) = {f4(p)}")
    mostrar("     Matriz del canal:")
    ver_matriz(matriz, A, B)
    mostrar(f"  b) Clasificación: {clase}")
    mostrar(f"  c) H(A/B) = {f4(h_ab)}   H(B/A) = {f4(h_ba)}   I(A,B) = {f4(i_ab)}")
    mostrar("  d) Canal reducido:" + ("" if len(reducido[0]) < len(matriz[0]) else " (no admite reducciones suficientes; queda igual)"))
    ver_matriz(reducido, A, [f"col{j + 1}" for j in range(len(reducido[0]))])
    if p_cap is not None:
        mostrar(f"  e) Capacidad C = {f4(cap)}   con P({A[0]}) = {f4(p_cap)}   P({A[1]}) = {f4(1 - p_cap)}")
    else:
        mostrar(f"  e) Capacidad C = {cap}")
    mostrar(f"     Probabilidad de error P_E = {f4(pe)}")
    if paridad is not None:
        if paridad["mensaje"]:
            mostrar(f"  f) Mensaje corregido: {paridad['mensaje']}   ({paridad['estado']})")
        else:
            mostrar("  f) Mensaje: NO se puede corregir (hay más de un error)")

# ================== PARTE 2: EXPLICACIÓN DE CADA RESULTADO ==================
titulo("PARTE 2 - QUÉ SIGNIFICA CADA RESULTADO (y frase para el parcial)")

if hay_ej1:
    mostrar(">>> EJERCICIO 1\n")
    explicar(alfabeto_y_probabilidades, MENSAJE)
    explicar(CalcEntropia, probs1)
    explicar(huffman, probs1)
    explicar(tasa_compresion_codigo, MENSAJE, alfabeto, codigo)
    explicar(resumen_codigo, probs1, codigo)
    explicar_extension(probs1, N)
    explicar(detalle_primer_teorema, probs1, codigo, 1)
    explicar(detalle_primer_teorema, probs1, codigo_ext, N)

if hay_ej2:
    mostrar(">>> EJERCICIO 2\n")
    explicar(canal_desde_secuencias, ENTRADA, SALIDA)
    explicar(es_sin_ruido, matriz)
    explicar(es_determinante, matriz)
    explicar(equivocacion, probs2, matriz)
    explicar(perdida, probs2, matriz)
    explicar(informacion_mutua, probs2, matriz)
    explicar(reducir_canal, matriz)
    if p_cap is not None:
        explicar(capacidad_binaria, reducido, 0.0001)
    else:
        explicar(capacidad_canal, reducido)
    explicar(probabilidad_error, probs2, matriz)
    if paridad is not None:
        explicar(analizar_matriz_paridad, filas_de_bits(ENTRADA))

# ============== PARTE 3: TEXTOS PARA "EXPLICAR" Y "CONCLUIR" ===============
titulo('PARTE 3 - TEXTOS PARA LAS PREGUNTAS "EXPLICAR" Y "CONCLUIR"')

if hay_ej1:
    explicacion_ej1(MENSAJE, N)
    mostrar("")
    conclusiones_ej1(MENSAJE, N)
    mostrar("\n")
if hay_ej2:
    explicacion_ej2(ENTRADA, SALIDA)
    mostrar("")
    conclusiones_ej2(ENTRADA, SALIDA)

# ===================== PARTE 4: EXTRAS (por si los piden) ===================
titulo("PARTE 4 - EXTRAS POR SI PIDEN ALGO MÁS")

if hay_ej1:
    mostrar("Código de Huffman de la extensión de orden", N, "(bloque -> palabra):")
    simbolos_ext = [""]
    for _ in range(N):
        simbolos_ext = [e + s for e in simbolos_ext for s in alfabeto]
    for s, p, c in zip(simbolos_ext, probs_ext, codigo_ext):
        mostrar(f"   {s}  P = {p:.6f}  ->  {c}")
    mostrar("")
    explicar(shannon_fano, probs1)
    explicar(rlc_comprimir, MENSAJE)

if hay_ej2:
    nombres_canal(A, B)
    explicar(probabilidades_salida, probs2, matriz)
    explicar(probabilidades_a_posteriori, probs2, matriz)
    explicar(entropias_a_posteriori, probs2, matriz)
    explicar(entropia_afin, probs2, matriz)
    explicar(analisis_canal, probs2, matriz)
    explicar(probabilidad_error, probs2, matriz, a_posteriori=True)
    explicar(es_uniforme, matriz)

if len(CODIGO_HAMMING) >= 2:
    explicar(analizar_codigo_hamming, CODIGO_HAMMING)
if LEVENSHTEIN[0] or LEVENSHTEIN[1]:
    explicar(distancia_levenshtein, LEVENSHTEIN[0], LEVENSHTEIN[1])

guardar_registro("resultado_parcial.txt")
mostrar("\n(Todo esto quedó guardado en resultado_parcial.txt)")
