"""
Verificar.py
============
Compara TUS respuestas del parcial con las correctas, calculadas con las
funciones verificadas de FuncionesParcial2.py. Dice, casillero por
casillero, BIEN o MAL y cuál es el valor correcto.

Uso:
  1. Completá los DATOS (igual que en ResolverParcial.py).
  2. Completá TUS_RESPUESTAS con lo que respondiste. Lo que no completes
     (None) no se revisa.
  3. Corré:  python Verificar.py

Criterio: un número está BIEN si difiere del correcto en 0.00015 o menos
(cubre redondear o truncar a 4 decimales). Solo importa math y random
(a través de FuncionesParcial2.py).
"""
from FuncionesParcial2 import *

# ============================ DATOS DEL PARCIAL ============================
MENSAJE = "GIIHGGGHGIHHIHIIGFHH"
N = 3
ENTRADA = "10100000101011101001111110011001"
SALIDA = "QQPQQPPQQQPQRRRQSPQSQRQSQQPSQQPP"

# =============================== TUS RESPUESTAS =============================
# Ejemplo cargado con las respuestas del intento 2025 (tiene errores a propósito).
TUS_RESPUESTAS = {
    # ---- Ejercicio 1 ----
    "probabilidades": {"F": 0.05, "G": 0.3, "H": 0.35, "I": 0.3},   # símbolo -> P
    "entropia": 1.7884,
    "codigo_fuente": None,           # ej.: {"F": "00", "G": "01", "H": "11", "I": "10"}
    "tasa_compresion": 4,
    "L_fuente": 2, "eta_fuente": 0.8942, "R_fuente": 0.1058,
    "L_extension": 5.15, "eta_extension": 0.9966, "R_extension": 0.0034,
    "teorema_fuente": "Cumple", "teorema_extension": "Cumple",      # "Cumple" / "No cumple"
    # ---- Ejercicio 2 ----
    "priori": {"0": 0.4688, "1": 0.5312},                            # entrada -> P
    "matriz": [[0.3333, 0.6667, 0, 0], [0.1765, 0.3539, 0.2353, 0.2353]],
    "clasificacion": "Ninguno",      # "Sin ruido" / "Determinante" / "Ambos" / "Ninguno"
    "equivocacion": 0.7158, "perdida": 1.4686, "informacion_mutua": 0.2814,
    "canal_reducido": [[1, 0], [0.5294, 0.2988]],
    "capacidad": 0.2988,
    "P_capacidad": {"0": 0.5, "1": 0.5},                             # entrada -> P que logra C
    "probabilidad_error": 0.75,
    "mensaje_corregido": "10100000101001101001111110011001",
}
# ===========================================================================

TOL = 0.00015
resultado = {"bien": 0, "mal": 0}


def informe(nombre, ok, tuyo, correcto, nota=""):
    resultado["bien" if ok else "mal"] += 1
    marca = "BIEN" if ok else "MAL "
    linea = f"[{marca}] {nombre}: respondiste {tuyo}"
    if not ok:
        linea += f"  ->  correcto: {correcto}"
    if nota:
        linea += f"   ({nota})"
    print(linea)


def num_ok(tuyo, correcto):
    try:
        return abs(float(tuyo) - float(correcto)) <= TOL
    except (TypeError, ValueError):
        return False


def numero(nombre, clave, correcto, nota=""):
    tuyo = TUS_RESPUESTAS.get(clave)
    if tuyo is None:
        return
    informe(nombre, num_ok(tuyo, correcto), tuyo, round(correcto, 4), nota)


def f4(m):
    return [[round(x, 4) for x in fila] for fila in m]


def matriz_ok(tuya, correcta, columnas_en_cualquier_orden=False):
    if len(tuya) != len(correcta) or any(len(a) != len(b) for a, b in zip(tuya, correcta)):
        return False
    if columnas_en_cualquier_orden:
        cols_t = sorted([[fila[j] for fila in tuya] for j in range(len(tuya[0]))])
        cols_c = sorted([[fila[j] for fila in correcta] for j in range(len(correcta[0]))])
        return all(num_ok(x, y) for ct, cc in zip(cols_t, cols_c) for x, y in zip(ct, cc))
    return all(num_ok(x, y) for ft, fc in zip(tuya, correcta) for x, y in zip(ft, fc))


def si_no(texto):
    t = str(texto).strip().lower()
    if t in ("true", "cumple", "si", "sí"):
        return True
    if t in ("false", "no cumple", "no"):
        return False
    return None


# ================================ EJERCICIO 1 ===============================
if MENSAJE:
    print("=" * 70 + "\nEJERCICIO 1\n" + "=" * 70)
    alf, probs = alfabeto_y_probabilidades(MENSAJE)
    cod = huffman(probs)
    r1 = resumen_codigo(probs, cod)
    pe = extension_fuente(probs, N)
    cod_ext = huffman(pe)
    rn = resumen_codigo(pe, cod_ext)
    d1 = detalle_primer_teorema(probs, cod, 1)
    dn = detalle_primer_teorema(probs, cod_ext, N)

    tus_p = TUS_RESPUESTAS.get("probabilidades")
    if tus_p is not None:
        for s, p in zip(alf, probs):
            informe(f"P({s})", s in tus_p and num_ok(tus_p[s], p), tus_p.get(s, "(falta)"), round(p, 4))
        sobran = [s for s in tus_p if s not in alf]
        if sobran:
            informe("símbolos", False, sobran, alf, "esos símbolos no están en el mensaje")
    numero("Entropía H(S)", "entropia", r1["H"])

    tu_cod = TUS_RESPUESTAS.get("codigo_fuente")
    if tu_cod is not None:
        if sorted(tu_cod) != sorted(alf):
            informe("Código de la fuente", False, tu_cod, dict(zip(alf, cod)), "no tiene una palabra por símbolo")
        else:
            palabras = [tu_cod[s] for s in alf]
            inst = es_instantaneo(palabras)
            l_tuyo = sum(p * len(w) for p, w in zip(probs, palabras))
            optimo = abs(l_tuyo - r1["L"]) <= 1e-9
            nota = ("instantáneo y con la L mínima (Huffman): es óptimo; con empates puede haber otras palabras igual de válidas"
                    if inst and optimo else
                    ("no es instantáneo (una palabra es prefijo de otra)" if not inst else
                     f"su L = {l_tuyo:.4f} es mayor que la óptima {r1['L']:.4f}: no es óptimo"))
            informe("Código de la fuente", inst and optimo, tu_cod, dict(zip(alf, cod)), nota)

    numero("Tasa de compresión", "tasa_compresion", tasa_compresion_codigo(MENSAJE, alf, cod), "8 bits ASCII / bits del código")
    numero("L fuente", "L_fuente", r1["L"])
    numero("η fuente", "eta_fuente", r1["rendimiento"])
    numero("R fuente", "R_fuente", r1["redundancia"])
    numero(f"L extensión (por bloque de {N})", "L_extension", rn["L"], "L_n de Huffman sobre la extensión")
    numero("η extensión", "eta_extension", rn["rendimiento"], f"η = {N}*H/L_n")
    numero("R extensión", "R_extension", rn["redundancia"])
    for clave, d, nombre in (("teorema_fuente", d1, "Primer Teorema fuente"), ("teorema_extension", dn, "Primer Teorema extensión")):
        tuyo = TUS_RESPUESTAS.get(clave)
        if tuyo is not None:
            informe(nombre, si_no(tuyo) == d["cumple"], tuyo, "Cumple" if d["cumple"] else "No cumple",
                    f"{d['H']:.4f} <= {d['Ln_sobre_n']:.4f} < {d['cota_superior']:.4f}")

    # coherencia interna de tus números de la extensión
    l_t, e_t = TUS_RESPUESTAS.get("L_extension"), TUS_RESPUESTAS.get("eta_extension")
    if l_t and e_t and abs(N * r1["H"] / float(l_t) - float(e_t)) > 0.001:
        print(f"   OJO: tu L de la extensión ({l_t}) y tu η ({e_t}) se contradicen: "
              f"{N}*H/L = {N * r1['H'] / float(l_t):.4f}")

# ================================ EJERCICIO 2 ===============================
if ENTRADA and SALIDA:
    print("=" * 70 + "\nEJERCICIO 2\n" + "=" * 70)
    A, pa, B, m = canal_desde_secuencias(ENTRADA, SALIDA)
    tus_pa = TUS_RESPUESTAS.get("priori")
    if tus_pa is not None:
        for a, p in zip(A, pa):
            informe(f"P({a})", str(a) in tus_pa and num_ok(tus_pa[str(a)], p), tus_pa.get(str(a), "(falta)"), round(p, 4))
    tu_m = TUS_RESPUESTAS.get("matriz")
    if tu_m is not None:
        nota = f"filas = {A}, columnas = {B}"
        malas = [i + 1 for i, fila in enumerate(tu_m) if abs(sum(float(x) for x in fila) - 1) > 0.001]
        if malas:
            nota += f"; tus filas {malas} no suman 1"
        informe("Matriz del canal", matriz_ok(tu_m, m), f4(tu_m), f4(m), nota)
    clase = {(True, True): "Ambos", (True, False): "Sin ruido",
             (False, True): "Determinante", (False, False): "Ninguno"}[(es_sin_ruido(m), es_determinante(m))]
    if TUS_RESPUESTAS.get("clasificacion") is not None:
        informe("Clasificación", str(TUS_RESPUESTAS["clasificacion"]).strip().lower() == clase.lower(),
                TUS_RESPUESTAS["clasificacion"], clase)
    numero("Equivocación H(A/B)", "equivocacion", equivocacion(pa, m))
    numero("Pérdida H(B/A)", "perdida", perdida(pa, m))
    i_ab = informacion_mutua(pa, m)
    numero("Información mutua I(A,B)", "informacion_mutua", i_ab)
    red = reducir_canal(m)
    tu_red = TUS_RESPUESTAS.get("canal_reducido")
    if tu_red is not None:
        malas = [i + 1 for i, fila in enumerate(tu_red) if abs(sum(float(x) for x in fila) - 1) > 0.001]
        informe("Canal reducido", matriz_ok(tu_red, red, columnas_en_cualquier_orden=True), f4(tu_red), f4(red),
                f"tus filas {malas} no suman 1" if malas else "")
    if len(A) == 2:
        c, p = capacidad_binaria(red, 0.0001)
        numero("Capacidad C", "capacidad", c)
        tu_pc = TUS_RESPUESTAS.get("P_capacidad")
        if tu_pc is not None:
            try:
                p_tuya = float(tu_pc[str(A[0])])
                i_con_tuya = informacion_mutua([p_tuya, 1 - p_tuya], red)
                ok = i_con_tuya >= c - 0.0001 and abs(float(tu_pc[str(A[1])]) - (1 - p_tuya)) <= TOL
            except (KeyError, TypeError, ValueError):
                ok, i_con_tuya = False, float("nan")
            informe("P que logra la capacidad", ok, tu_pc, {str(A[0]): round(p, 4), str(A[1]): round(1 - p, 4)},
                    f"con tus P la información mutua es {i_con_tuya:.4f}; la capacidad es {c:.4f}")
    pe_ml = probabilidad_error(pa, m)
    pe_map = probabilidad_error(pa, m, a_posteriori=True)
    tu_pe = TUS_RESPUESTAS.get("probabilidad_error")
    if tu_pe is not None:
        if num_ok(tu_pe, pe_ml):
            informe("Probabilidad de error", True, tu_pe, round(pe_ml, 4), "regla de máxima posibilidad (la de la guía)")
        elif num_ok(tu_pe, pe_map):
            informe("Probabilidad de error", True, tu_pe, round(pe_map, 4),
                    f"coincide con la regla a posteriori; con máxima posibilidad da {pe_ml:.4f}: aclarar la regla")
        else:
            informe("Probabilidad de error", False, tu_pe, round(pe_ml, 4),
                    f"máxima posibilidad {pe_ml:.4f}, a posteriori {pe_map:.4f}; no puede superar {1 - max(pa):.4f}")
    if TUS_RESPUESTAS.get("mensaje_corregido") is not None and set(ENTRADA) <= {"0", "1"} and len(ENTRADA) % 8 == 0:
        par = analizar_matriz_paridad(filas_de_bits(ENTRADA))
        correcto = par["mensaje"] if par["mensaje"] else "(no se puede corregir: más de un error)"
        tuyo = str(TUS_RESPUESTAS["mensaje_corregido"]).strip()
        nota = ""
        if set(tuyo) <= {"0", "1"} and par["mensaje"]:
            nota = "pusiste los bits: hay que decodificarlos y escribir el TEXTO"
        informe("Mensaje corregido", tuyo == par["mensaje"] or (not par["mensaje"] and "no" in tuyo.lower()),
                tuyo, correcto, nota)

print("\n" + "=" * 70)
print(f"TOTAL: {resultado['bien']} bien, {resultado['mal']} mal")
