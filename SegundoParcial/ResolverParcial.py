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
     PARTE 5  OTROS DATOS: probabilidades, un código dado, una matriz de canal,
              canales en serie, Hamming, Levenshtein, paridad, RLC (si los completás)
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

# -------- OTROS DATOS: completá SOLO lo que te den (lo vacío se saltea) --------
# Fuente dada por sus PROBABILIDADES (en vez de un mensaje):
PROBS = []                   # ej.: [0.5, 0.2, 0.3]
N_PROBS = 2                  # orden de la extensión para esa fuente

# Un CÓDIGO ya armado para evaluar (sobre PROBS; si PROBS está vacío, sobre el MENSAJE).
# Si tiene q**n palabras se toma como código de la extensión de orden n.
CODIGO = []                  # ej.: ["11", "010", "00"]
CADENA_A_DECODIFICAR = ""    # ej.: "ABACBAACAB..." -> se decodifica con CODIGO

# Canal dado por su MATRIZ (en vez de secuencias). Filas = entradas, columnas = salidas.
MATRIZ = []                  # ej.: [[0.6, 0.4], [0.2, 0.8]]
PRIORI = []                  # ej.: [0.5, 0.5]   (vacío = entradas equiprobables)
MATRIZ2 = []                 # segundo canal, para CANALES EN SERIE (MATRIZ y después MATRIZ2)

# Control de errores y compresión:
CODIGO_HAMMING = []          # ej.: ["0000", "0011", "1010", "0101"] -> distancia de Hamming del código
LEVENSHTEIN = ("", "")       # ej.: ("casa", "calle")               -> distancia de Levenshtein
TEXTO_PARIDAD = ""           # ej.: "HOLA" -> se protege con paridad vertical, longitudinal y cruzada
BITS_PARIDAD = ""            # tira de bits, o lista de filas de 8 bits, para detectar/corregir
RLC = ""                     # ej.: "AAAABBBCCDAA" -> Run Length Coding
# ===========================================================================

from Explicaciones import *
from Explicaciones import _imprimir
from FuncionesParcial2 import clasifica, calcular_kraft, es_instantaneo


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

# ================ PARTE 5: OTROS DATOS (solo si los completaste) ================
hay_otros = bool(PROBS or CODIGO or MATRIZ or len(CODIGO_HAMMING) >= 2 or LEVENSHTEIN[0] or
                 LEVENSHTEIN[1] or TEXTO_PARIDAD or BITS_PARIDAD or RLC)
if hay_otros:
    titulo("PARTE 5 - OTROS DATOS")

# ---- Fuente dada por probabilidades ----
if PROBS:
    titulo("FUENTE DADA POR PROBABILIDADES")
    explicar(CalcEntropia, PROBS)
    cod_p = explicar(huffman, PROBS)
    explicar(resumen_codigo, PROBS, cod_p)
    explicar(shannon_fano, PROBS)
    if N_PROBS > 1:
        ext_p = explicar_extension(PROBS, N_PROBS)
        explicar(detalle_primer_teorema, PROBS, ext_p["codigo"], N_PROBS)

# ---- Código dado para evaluar ----
if CODIGO:
    titulo("CÓDIGO DADO: " + ", ".join(CODIGO))
    base = PROBS if PROBS else (probs1 if hay_ej1 else [])
    clase_cod = clasifica(CODIGO)
    kraft = calcular_kraft(CODIGO)
    mostrar(f"Clasificación del código: {clase_cod}")
    mostrar(f"Suma de Kraft = {kraft:.4f}  ->  " + (
        "cumple Kraft (<= 1): existe un código instantáneo con esas longitudes." if kraft <= 1 + 1e-9 else
        "NO cumple Kraft (> 1): con esas longitudes no puede haber código unívoco."))
    mostrar("")
    if not base:
        mostrar("(Para L, rendimiento y Primer Teorema hacen falta las probabilidades: completá PROBS.)")
    else:
        q = len(base)
        n_cod = 0
        for k in range(1, 7):
            if q ** k == len(CODIGO):
                n_cod = k
        if n_cod == 0:
            mostrar(f"OJO: el código tiene {len(CODIGO)} palabras y la fuente {q} símbolos "
                    f"(no es q**n): revisá que correspondan.")
        else:
            probs_cod = extension_fuente(base, n_cod) if n_cod > 1 else base
            explicar(rendimiento_redundancia, probs_cod, CODIGO)
            explicar(detalle_primer_teorema, base, CODIGO, n_cod)
            if n_cod == 1 and N_PROBS > 1 and PROBS:
                mostrar(f"Extensión de orden {N_PROBS} usando ESTE código (concatenando palabras):")
                explicar(detalle_primer_teorema, base, extension_codigo(CODIGO, N_PROBS), N_PROBS)
    if CADENA_A_DECODIFICAR:
        if hay_ej1 and not PROBS and len(alfabeto) == len(CODIGO):
            simbolos_cod = list(alfabeto)
        else:
            simbolos_cod = [f"S{i + 1}" for i in range(len(CODIGO))]
        if es_instantaneo(CODIGO):
            explicar(decodificar_cadena, CADENA_A_DECODIFICAR, simbolos_cod, CODIGO)
        else:
            mostrar("El código no es instantáneo: no se puede decodificar palabra por palabra.")

# ---- Canal dado por su matriz ----
if MATRIZ:
    titulo("CANAL DADO POR SU MATRIZ")
    nombres_canal()
    pri = PRIORI if PRIORI else [1 / len(MATRIZ)] * len(MATRIZ)
    if not PRIORI:
        mostrar(f"(No se dieron probabilidades a priori: se usan equiprobables {[round(x, 4) for x in pri]})")
    mostrar("")
    explicar(es_sin_ruido, MATRIZ)
    explicar(es_determinante, MATRIZ)
    explicar(probabilidades_salida, pri, MATRIZ)
    explicar(probabilidades_simultaneas, pri, MATRIZ)
    explicar(probabilidades_a_posteriori, pri, MATRIZ)
    explicar(entropias_a_posteriori, pri, MATRIZ)
    explicar(equivocacion, pri, MATRIZ)
    explicar(perdida, pri, MATRIZ)
    explicar(entropia_afin, pri, MATRIZ)
    explicar(informacion_mutua, pri, MATRIZ)
    explicar(analisis_canal, pri, MATRIZ)
    red_m = explicar(reducir_canal, MATRIZ)
    explicar(es_uniforme, MATRIZ)
    if len(MATRIZ) == 2:
        explicar(capacidad_binaria, red_m, 0.0001)
    else:
        explicar(capacidad_canal, MATRIZ)
    explicar(probabilidad_error, pri, MATRIZ)
    explicar(probabilidad_error, pri, MATRIZ, a_posteriori=True)
    if MATRIZ2:
        titulo("CANALES EN SERIE (MATRIZ y después MATRIZ2)")
        serie = explicar(canal_serie, MATRIZ, MATRIZ2)
        i_1 = informacion_mutua(pri, MATRIZ)
        i_s = informacion_mutua(pri, serie)
        mostrar(f"I(A,B) del primer canal = {i_1:.4f}   I(A,C) del canal en serie = {i_s:.4f}")
        mostrar("Frase: " + (
            f"La información mutua del canal en serie ({i_s:.4f}) es menor que la del primer canal "
            f"({i_1:.4f}): al pasar por el segundo canal se pierde información." if i_s < i_1 - 5e-5 else
            f"La información mutua del canal en serie ({i_s:.4f}) es igual a la del primer canal: el "
            "segundo canal no hace perder información."))
        mostrar("")

# ---- Control de errores y compresión ----
if len(CODIGO_HAMMING) >= 2:
    explicar(analizar_codigo_hamming, CODIGO_HAMMING)
if LEVENSHTEIN[0] or LEVENSHTEIN[1]:
    explicar(distancia_levenshtein, LEVENSHTEIN[0], LEVENSHTEIN[1])
if TEXTO_PARIDAD:
    explicar(generar_mensaje_con_paridad, TEXTO_PARIDAD)
if BITS_PARIDAD:
    filas_p = filas_de_bits(BITS_PARIDAD) if isinstance(BITS_PARIDAD, str) else list(BITS_PARIDAD)
    explicar(analizar_matriz_paridad, filas_p)
if RLC:
    explicar(rlc_texto, RLC)
    explicar(rlc_comprimir, RLC)

guardar_registro("resultado_parcial.txt")
mostrar("\n(Todo esto quedó guardado en resultado_parcial.txt)")
