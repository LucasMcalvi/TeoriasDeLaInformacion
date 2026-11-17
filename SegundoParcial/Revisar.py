"""
Revisar.py
==========
Revisa TU script del parcial: lo corre tal cual, mira cada variable que
creaste y te dice:
  - qué inciso del parcial es,
  - si el valor está BIEN o MAL (comparado con lo correcto, calculado con
    las funciones verificadas de FuncionesParcial2.py),
  - qué incisos te FALTAN y con qué función se hacen,
  - si tus imports están permitidos.

Uso:
  1. Poné el nombre de tu archivo en ARCHIVO (tiene que estar en esta carpeta).
  2. Tu archivo tiene que tener los datos en variables con estos nombres:
       MENSAJE y N            (ejercicio de la fuente; N = orden de la extensión)
       ENTRADA y SALIDA       (ejercicio del canal)
  3. Corré:  python Revisar.py

Tu archivo NO se modifica. Este archivo no importa nada salvo tus funciones.
"""

ARCHIVO = "mi_parcial.py"

from FuncionesParcial2 import *

TOL = 1e-6          # tus valores salen de funciones: tienen que coincidir casi exacto
TOL_TIPEADO = 0.00015
PERMITIDOS = ("math", "random", "FuncionesParcial2", "Explicaciones", "Func_clase4", "Func_clase5",
              "Func_clase6", "Formulas", "FormulasCodificacion")


# ---------------------------------------------------------------------------
# Comparaciones
# ---------------------------------------------------------------------------
def es_num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def igual(a, b, tol=TOL):
    """Compara números, listas, tuplas, matrices y diccionarios."""
    if es_num(a) and es_num(b):
        return abs(a - b) <= tol
    if isinstance(a, bool) or isinstance(b, bool):
        return a is b
    if isinstance(a, str) and isinstance(b, str):
        return a == b
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(igual(x, y, tol) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return set(a) == set(b) and all(igual(a[k], b[k], tol) for k in a)
    try:
        return list(a) == list(b)
    except TypeError:
        return False


def corto(x, largo=110):
    if isinstance(x, float):
        return f"{x:.4f}"
    if isinstance(x, (list, tuple)) and x and all(es_num(v) for v in x):
        return "[" + ", ".join(f"{v:.4f}" if isinstance(v, float) else str(v) for v in x) + "]"
    if isinstance(x, (list, tuple)) and x and all(isinstance(f, (list, tuple)) for f in x):
        return "[" + ", ".join(corto(f) for f in x) + "]"
    t = repr(x)
    return t if len(t) <= largo else t[:largo] + "..."


# ---------------------------------------------------------------------------
# Leer y correr el archivo de Lucas
# ---------------------------------------------------------------------------
print("=" * 78)
print(f" REVISIÓN DE {ARCHIVO}")
print("=" * 78)
try:
    with open(ARCHIVO, encoding="utf-8") as f:
        codigo = f.read()
except FileNotFoundError:
    print(f"No encuentro '{ARCHIVO}' en esta carpeta. Poné el nombre correcto en ARCHIVO.")
    raise SystemExit

# imports
print("\nIMPORTS:")
malos, propios = [], []
for numero, linea in enumerate(codigo.split("\n"), 1):
    l = linea.strip()
    if l.startswith("import ") or l.startswith("from "):
        partes = l.split("#")[0].replace(",", " ").split()
        if l.startswith("from "):
            modulos = [partes[1]]
        else:
            modulos, saltar = [], False
            for p in partes[1:]:
                if saltar:
                    saltar = False
                elif p == "as":
                    saltar = True
                else:
                    modulos.append(p)
        for m in modulos:
            base = m.split(".")[0]
            if base in ("as",) or not base:
                continue
            if base not in PERMITIDOS:
                malos.append((numero, base))
            elif base not in ("math", "random"):
                propios.append(base)
if malos:
    for numero, m in malos:
        print(f"  [MAL ] línea {numero}: importa '{m}'. Solo se permite math y random (y tus módulos).")
else:
    print("  [BIEN] solo importa math, random y tus módulos.")
if propios:
    print(f"  OJO: importa módulos propios ({', '.join(sorted(set(propios)))}). Si este es el archivo que "
          "ENTREGÁS, tenés que entregar también esos archivos o copiar las funciones adentro "
          "(en el primer parcial el .py no corrió por esto).")

# correr
print("\nSALIDA DE TU PROGRAMA:")
print("-" * 78)
ns = {"__name__": "__main__"}
error = None
try:
    exec(compile(codigo, ARCHIVO, "exec"), ns)
except SystemExit:
    pass
except Exception as e:
    error = e
print("-" * 78)
if error is not None:
    print(f"[MAL ] Tu código se cortó con un error: {type(error).__name__}: {error}")
    texto_error = str(error)
    if "palabras código (q**n)" in texto_error:
        print("       PISTA: en detalle_primer_teorema / cumple_primer_teorema van las probabilidades de la")
        print("       fuente ORIGINAL y el código de la EXTENSIÓN: detalle_primer_teorema(probs, cod_ext, N)")
    elif "misma cantidad de elementos" in texto_error:
        print("       PISTA: las probabilidades y las palabras código tienen que ser de la misma fuente")
        print("       (para la extensión: resumen_codigo(pe, cod_ext), con pe = extension_fuente(probs, N))")
    elif "is not defined" in texto_error:
        print("       PISTA: usás una variable o función que no existe (¿mal escrita o sin importar?)")
    print("       (reviso igual las variables que llegó a crear)")

MENSAJE = ns.get("MENSAJE", "")
N = ns.get("N", None)
ENTRADA = ns.get("ENTRADA", "")
SALIDA = ns.get("SALIDA", "")
if isinstance(MENSAJE, str) is False:
    MENSAJE = ""

# ---------------------------------------------------------------------------
# Catálogo de respuestas correctas
# ---------------------------------------------------------------------------
# Cada entrada: (inciso, descripción, valor_correcto, como_se_hace)
esperados = []
tipicos = []      # (descripción del error, valor equivocado, explicación)
codigos_validos = []   # (inciso, descripción, probs, L_optima)
booleanos = []

if MENSAJE:
    alf, probs = alfabeto_y_probabilidades(MENSAJE)
    cod = huffman(probs)
    h = CalcEntropia(probs)
    r1 = resumen_codigo(probs, cod)
    d1 = detalle_primer_teorema(probs, cod, 1)
    tasa = tasa_compresion_codigo(MENSAJE, alf, cod)
    esperados += [
        ("1a", "alfabeto de la fuente", alf, "alf, probs = alfabeto_y_probabilidades(MENSAJE)"),
        ("1a", "probabilidades de la fuente", probs, "alf, probs = alfabeto_y_probabilidades(MENSAJE)"),
        ("1a", "alfabeto y probabilidades", (alf, probs), "alfabeto_y_probabilidades(MENSAJE)"),
        ("1a", "entropía H(S)", h, "CalcEntropia(probs)"),
        ("1b", "código óptimo (Huffman) de la fuente", cod, "huffman(probs)"),
        ("1c", "tasa de compresión", tasa, "tasa_compresion_codigo(MENSAJE, alf, cod)"),
        ("1e", "L del código de la fuente", r1["L"], "resumen_codigo(probs, cod)['L']"),
        ("1e", "rendimiento η de la fuente", r1["rendimiento"], "resumen_codigo(probs, cod)['rendimiento']"),
        ("1e", "redundancia R de la fuente", r1["redundancia"], "resumen_codigo(probs, cod)['redundancia']"),
        ("1e", "resumen del código de la fuente (H, L, η, R)", r1, "resumen_codigo(probs, cod)"),
        ("1e", "(η, R) de la fuente", rendimiento_redundancia(probs, cod), "rendimiento_redundancia(probs, cod)"),
        ("1f", "Primer Teorema de la fuente (detalle)", d1, "detalle_primer_teorema(probs, cod, 1)"),
    ]
    codigos_validos.append(("1b", "código óptimo de la fuente", probs, r1["L"]))
    booleanos.append(("1f", "Primer Teorema de la fuente", d1["cumple"], "cumple_primer_teorema(probs, cod, 1)"))
    tipicos += [
        ("tasa con el byte de cabecera", tasa_compresion(MENSAJE, codificar_mensaje(MENSAJE, alf, cod)),
         "tasa_compresion(...) con codificar_mensaje cuenta 1 byte extra; el parcial pide tasa_compresion_codigo(MENSAJE, alf, cod)"),
    ]
    sf = shannon_fano(probs)
    esperados.append(("extra", "código de Shannon-Fano (no es el óptimo que se pide)", sf, "shannon_fano(probs)"))
    if N and isinstance(N, int) and N >= 1:
        pe = extension_fuente(probs, N)
        cod_ext = huffman(pe)
        rn = resumen_codigo(pe, cod_ext)
        dn = detalle_primer_teorema(probs, cod_ext, N)
        esperados += [
            ("1d", f"probabilidades de la extensión de orden {N}", pe, f"extension_fuente(probs, {N})"),
            ("1d", f"código óptimo (Huffman) de la extensión de orden {N}", cod_ext, "huffman(pe)"),
            ("1e", f"L de la extensión (por bloque de {N})", rn["L"], "resumen_codigo(pe, cod_ext)['L']"),
            ("1e", "rendimiento η de la extensión", rn["rendimiento"], "resumen_codigo(pe, cod_ext)['rendimiento']"),
            ("1e", "redundancia R de la extensión", rn["redundancia"], "resumen_codigo(pe, cod_ext)['redundancia']"),
            ("1e", "resumen del código de la extensión", rn, "resumen_codigo(pe, cod_ext)"),
            ("1e", "(η, R) de la extensión", rendimiento_redundancia(pe, cod_ext), "rendimiento_redundancia(pe, cod_ext)"),
            ("1f", "Primer Teorema de la extensión (detalle)", dn, f"detalle_primer_teorema(probs, cod_ext, {N})"),
            ("extra", f"entropía de la extensión H(S^{N}) = {N}*H(S)", N * h, f"{N} * CalcEntropia(probs)"),
        ]
        codigos_validos.append(("1d", f"código óptimo de la extensión de orden {N}", pe, rn["L"]))
        booleanos.append(("1f", "Primer Teorema de la extensión", dn["cumple"], f"cumple_primer_teorema(probs, cod_ext, {N})"))
        tipicos += [
            (f"L de la extensión dividida por {N} (por símbolo)", rn["L"] / N,
             f"eso es L_n/n; en el casillero 'L de la extensión' va L_n = {rn['L']:.4f} (por bloque)"),
            ("código de la extensión concatenando palabras", extension_codigo(cod, N),
             "concatenar no es el código óptimo de la extensión: hay que hacer huffman(extension_fuente(probs, N))"),
            ("L del código concatenado", N * r1["L"], "esa es la L de concatenar; el óptimo es huffman sobre la extensión"),
        ]

if ENTRADA and SALIDA and len(ENTRADA) == len(SALIDA):
    A, pa, B, m = canal_desde_secuencias(ENTRADA, SALIDA)
    red = reducir_canal(m)
    pb = probabilidades_salida(pa, m)
    esperados += [
        ("2a", "a priori y matriz (A, P(a), B, matriz)", (A, pa, B, m), "canal_desde_secuencias(ENTRADA, SALIDA)"),
        ("2a", "probabilidades a priori", pa, "canal_desde_secuencias(...)[1]"),
        ("2a", "matriz del canal", m, "canal_desde_secuencias(...)[3]"),
        ("2a", "alfabeto de entrada", A, "canal_desde_secuencias(...)[0]"),
        ("2a", "alfabeto de salida", B, "canal_desde_secuencias(...)[2]"),
        ("2c", "equivocación H(A/B)", equivocacion(pa, m), "equivocacion(probs, matriz)"),
        ("2c", "pérdida H(B/A)", perdida(pa, m), "perdida(probs, matriz)"),
        ("2c", "información mutua I(A,B)", informacion_mutua(pa, m), "informacion_mutua(probs, matriz)"),
        ("2d", "canal reducido", red, "reducir_canal(matriz)"),
        ("2e", "probabilidad de error P_E (máxima posibilidad, la de la guía)", probabilidad_error(pa, m),
         "probabilidad_error(probs, matriz)"),
        ("extra", "H(A)", CalcEntropia(pa), "CalcEntropia(probs)"),
        ("extra", "H(B)", CalcEntropia(pb), "CalcEntropia(probabilidades_salida(probs, matriz))"),
        ("extra", "entropía afín H(A,B)", entropia_afin(pa, m), "entropia_afin(probs, matriz)"),
        ("extra", "probabilidades de salida P(b)", pb, "probabilidades_salida(probs, matriz)"),
        ("extra", "probabilidades a posteriori P(a/b)", probabilidades_a_posteriori(pa, m), "probabilidades_a_posteriori(probs, matriz)"),
        ("extra", "probabilidades simultáneas P(a,b)", probabilidades_simultaneas(pa, m), "probabilidades_simultaneas(probs, matriz)"),
        ("extra", "entropías a posteriori H(A/b)", entropias_a_posteriori(pa, m), "entropias_a_posteriori(probs, matriz)"),
        ("extra", "todas las entropías del canal", analisis_canal(pa, m), "analisis_canal(probs, matriz)"),
    ]
    pe_post = probabilidad_error(pa, m, a_posteriori=True)
    if abs(pe_post - probabilidad_error(pa, m)) > TOL:
        esperados.append(("2e", "P_E con la regla a posteriori (aclarar la regla)", pe_post,
                          "probabilidad_error(probs, matriz, a_posteriori=True)"))
    booleanos += [("2b", "¿es sin ruido?", es_sin_ruido(m), "es_sin_ruido(matriz)"),
                  ("2b", "¿es determinante?", es_determinante(m), "es_determinante(matriz)")]
    if len(A) == 2:
        c, p = capacidad_binaria(red, 0.0001)
        esperados += [
            ("2e", "capacidad y P que la logra (C, P(a1))", (c, p), "capacidad_binaria(reducido, 0.0001)"),
            ("2e", "capacidad C", c, "capacidad_binaria(reducido, 0.0001)[0]"),
            ("2e", f"P({A[0]}) que logra la capacidad", p, "capacidad_binaria(reducido, 0.0001)[1]"),
            ("2e", f"P({A[1]}) que logra la capacidad", 1 - p, "1 - capacidad_binaria(reducido, 0.0001)[1]"),
        ]
        tipicos.append(("capacidad calculada sobre el canal original (da igual que con el reducido)",
                        capacidad_binaria(m, 0.0001), "está bien: el canal reducido tiene la misma capacidad"))
    if set(ENTRADA) <= {"0", "1"} and len(ENTRADA) % 8 == 0 and len(ENTRADA) >= 16:
        filas = filas_de_bits(ENTRADA)
        par = analizar_matriz_paridad(filas)
        esperados += [
            ("2f", "filas de bits (LRC + caracteres)", filas, "filas_de_bits(ENTRADA)"),
            ("2f", "análisis de paridad", par, "analizar_matriz_paridad(filas_de_bits(ENTRADA))"),
        ]
        if par["mensaje"]:
            esperados.append(("2f", "mensaje corregido", par["mensaje"],
                              "analizar_matriz_paridad(filas_de_bits(ENTRADA))['mensaje']"))
            if par["matriz_corregida"]:
                tipicos.append(("mensaje dejado en bits", "".join(par["matriz_corregida"]),
                                f"hay que decodificarlo: el mensaje es '{par['mensaje']}'"))
                tipicos.append(("matriz corregida (filas de bits)", par["matriz_corregida"],
                                f"está bien como paso, pero la respuesta es el texto '{par['mensaje']}'"))
    tipicos.append(("P_E calculada con el canal reducido", probabilidad_error(pa, red),
                    "la P_E se calcula con la matriz ORIGINAL"))

if not esperados:
    print("\nNo encontré los datos. Tu archivo tiene que definir MENSAJE (y N) y/o ENTRADA y SALIDA.")
    raise SystemExit
if MENSAJE and not N:
    print("\nOJO: no definiste N (orden de la extensión), así que no reviso la extensión. Agregá  N = ...")

# ---------------------------------------------------------------------------
# Revisar cada variable
# ---------------------------------------------------------------------------
DATOS = {"MENSAJE", "N", "ENTRADA", "SALIDA"}
encontrados = set()


def buscar(valor, tol):
    hallados = [(i, d) for i, d, v, _ in esperados if igual(valor, v, tol)]
    return hallados


def codigo_valido(valor):
    if not (isinstance(valor, (list, tuple)) and valor and all(isinstance(x, str) for x in valor)):
        return None
    for inciso, desc, ps, l_opt in codigos_validos:
        if len(valor) == len(ps) and set("".join(valor)) <= {"0", "1"}:
            inst = es_instantaneo(list(valor))
            l = sum(p * len(w) for p, w in zip(ps, valor))
            return inciso, desc, inst, l, l_opt
    return None


print("\nTUS VARIABLES:")
hubo = False
for nombre, valor in ns.items():
    if nombre.startswith("_") or nombre in DATOS or nombre == "__builtins__":
        continue
    if callable(valor) or type(valor).__name__ == "module":
        continue
    hubo = True
    hallados = buscar(valor, TOL) or buscar(valor, TOL_TIPEADO)
    if hallados and all(i == "extra" for i, _ in hallados) and codigo_valido(valor):
        hallados = []          # un código (por ej. Shannon-Fano): se juzga abajo como código
    if hallados:
        for inciso, desc in hallados:
            encontrados.add(desc)
        incisos = ", ".join(f"{i}) {d}" for i, d in hallados)
        print(f"  [BIEN] {nombre} = {corto(valor)}")
        print(f"         -> {incisos}")
        continue
    cv = codigo_valido(valor)
    if cv:
        inciso, desc, inst, l, l_opt = cv
        if inst and abs(l - l_opt) <= 1e-9:
            encontrados.add(desc.replace("código óptimo", "código óptimo (Huffman)"))
            encontrados.add(desc)
            print(f"  [BIEN] {nombre} = {corto(valor)}")
            print(f"         -> {inciso}) {desc}: instantáneo y con la L mínima ({l:.4f}); "
                  "no son las mismas palabras que da huffman(), pero con la misma L también es óptimo")
        else:
            print(f"  [MAL ] {nombre} = {corto(valor)}")
            print(f"         -> parece el {desc}, pero " +
                  ("no es instantáneo" if not inst else f"su L = {l:.4f} es mayor que la óptima {l_opt:.4f}"))
        continue
    if isinstance(valor, bool):
        coinc = [(i, d, f) for i, d, v, f in booleanos if v is valor]
        if coinc:
            print(f"  [ ?? ] {nombre} = {valor}  -> si es " + " / ".join(f"{i}) {d}" for i, d, _ in coinc) +
                  ": está bien")
        else:
            print(f"  [ ?? ] {nombre} = {valor}  -> correcto: " +
                  "; ".join(f"{i}) {d} = {v}" for i, d, v, _ in booleanos))
        continue
    tip = [(d, x) for d, v, x in tipicos if igual(valor, v, TOL)]
    if tip:
        d, x = tip[0]
        print(f"  [MAL ] {nombre} = {corto(valor)}")
        print(f"         -> esto es: {d}. {x}")
        continue
    print(f"  [ ?? ] {nombre} = {corto(valor)}")
    print("         -> no coincide con ninguna respuesta del parcial. Revisá con qué función y "
          "qué datos lo calculaste.")
if not hubo:
    print("  (no hay variables con resultados)")

# booleanos (clasificación, teorema): cuentan como hechos si están en una variable
# con el valor correcto y se usó la función correspondiente
for inciso, desc, v, forma in booleanos:
    func = forma.split("(")[0]
    if func in codigo and any(isinstance(x, bool) and x is v for x in ns.values()):
        encontrados.add(desc)

# ---------------------------------------------------------------------------
# Qué falta: un renglón por casillero del parcial (con las formas válidas)
# ---------------------------------------------------------------------------
requeridos = []
if MENSAJE:
    requeridos += [
        ("1a", "probabilidades", ["probabilidades de la fuente", "alfabeto y probabilidades"],
         "alf, probs = alfabeto_y_probabilidades(MENSAJE)"),
        ("1a", "entropía", ["entropía H(S)"], "CalcEntropia(probs)"),
        ("1b", "código óptimo de la fuente", ["código óptimo (Huffman) de la fuente", "código óptimo de la fuente"],
         "cod = huffman(probs)"),
        ("1c", "tasa de compresión", ["tasa de compresión"], "tasa_compresion_codigo(MENSAJE, alf, cod)"),
        ("1e", "L de la fuente", ["L del código de la fuente", "resumen del código de la fuente (H, L, η, R)"],
         "resumen_codigo(probs, cod)  (trae L, rendimiento y redundancia)"),
        ("1e", "η y R de la fuente", ["rendimiento η de la fuente", "(η, R) de la fuente",
                                      "resumen del código de la fuente (H, L, η, R)"],
         "resumen_codigo(probs, cod)"),
        ("1f", "Primer Teorema de la fuente", ["Primer Teorema de la fuente (detalle)", "Primer Teorema de la fuente"],
         "detalle_primer_teorema(probs, cod, 1)"),
    ]
    if N:
        requeridos += [
            ("1d", f"código óptimo de la extensión de orden {N}",
             [f"código óptimo (Huffman) de la extensión de orden {N}", f"código óptimo de la extensión de orden {N}"],
             f"pe = extension_fuente(probs, {N});  cod_ext = huffman(pe)"),
            ("1e", "L de la extensión", [f"L de la extensión (por bloque de {N})", "resumen del código de la extensión"],
             "resumen_codigo(pe, cod_ext)   (con pe, no con probs)"),
            ("1e", "η y R de la extensión", ["rendimiento η de la extensión", "(η, R) de la extensión",
                                             "resumen del código de la extensión"],
             "resumen_codigo(pe, cod_ext)"),
            ("1f", "Primer Teorema de la extensión", ["Primer Teorema de la extensión (detalle)",
                                                     "Primer Teorema de la extensión"],
             f"detalle_primer_teorema(probs, cod_ext, {N})   (con probs ORIGINALES)"),
        ]
if ENTRADA and SALIDA and len(ENTRADA) == len(SALIDA):
    requeridos += [
        ("2a", "probabilidades a priori", ["probabilidades a priori", "a priori y matriz (A, P(a), B, matriz)"],
         "A, probs, B, matriz = canal_desde_secuencias(ENTRADA, SALIDA)"),
        ("2a", "matriz del canal", ["matriz del canal", "a priori y matriz (A, P(a), B, matriz)"],
         "canal_desde_secuencias(ENTRADA, SALIDA)"),
        ("2b", "¿sin ruido?", ["¿es sin ruido?"], "es_sin_ruido(matriz)"),
        ("2b", "¿determinante?", ["¿es determinante?"], "es_determinante(matriz)"),
        ("2c", "equivocación H(A/B)", ["equivocación H(A/B)"], "equivocacion(probs, matriz)"),
        ("2c", "pérdida H(B/A)", ["pérdida H(B/A)"], "perdida(probs, matriz)"),
        ("2c", "información mutua I(A,B)", ["información mutua I(A,B)"], "informacion_mutua(probs, matriz)"),
        ("2d", "canal reducido", ["canal reducido"], "reducido = reducir_canal(matriz)"),
        ("2e", "probabilidad de error", ["probabilidad de error P_E (máxima posibilidad, la de la guía)",
                                         "P_E con la regla a posteriori (aclarar la regla)"],
         "probabilidad_error(probs, matriz)"),
    ]
    if len(set(ENTRADA)) == 2:
        A0 = sorted(set(ENTRADA))
        requeridos += [
            ("2e", "capacidad", ["capacidad C", "capacidad y P que la logra (C, P(a1))"],
             "C, p = capacidad_binaria(reducido, 0.0001)"),
            ("2e", "P que logran la capacidad", ["capacidad y P que la logra (C, P(a1))",
                                                 f"P({A0[0]}) que logra la capacidad"],
             f"C, p = capacidad_binaria(reducido, 0.0001)   (p = P({A0[0]}), 1-p = P({A0[1]}))"),
        ]
    if set(ENTRADA) <= {"0", "1"} and len(ENTRADA) % 8 == 0 and len(ENTRADA) >= 16:
        requeridos.append(("2f", "mensaje corregido (texto)", ["mensaje corregido", "análisis de paridad"],
                           "analizar_matriz_paridad(filas_de_bits(ENTRADA))['mensaje']"))

faltan = [(i, d, f) for i, d, alternativas, f in requeridos if not any(a in encontrados for a in alternativas)]

print("\nTE FALTA (incisos que no encontré en tus variables):")
if faltan:
    for inciso, desc, forma in faltan:
        print(f"  {inciso}) {desc:42s} ->  {forma}")
else:
    print("  Nada: están todos los incisos.")
print("\nReferencia: [BIEN] coincide con la respuesta correcta; [MAL ] es un error conocido;")
print("[ ?? ] no coincide con nada (o es un True/False: fijate a qué corresponde).")
