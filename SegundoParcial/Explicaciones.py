"""
Explicaciones.py
================
Ayuda para INTERPRETAR los resultados de las funciones de Func_clase4/5/6.
NO se entrega en el parcial: es para usarlo vos, aparte, mientras escribís
las respuestas de "explicar" y "analizar/concluir".

Uso
---
    from Explicaciones import *

    r = explicar(equivocacion, probs, matriz)

    -> corre equivocacion(probs, matriz), imprime la explicación y devuelve
       el mismo resultado que la función (así podés seguir usándolo).

Cada explicación muestra:
    RESULTADO          el valor que dio la función
    QUÉ SIGNIFICA      qué es esa magnitud
    CÓMO SE OBTUVO     una línea para la pregunta "explicar cómo se obtuvo"
    CÓMO LEERLO        todos los casos posibles; ">>" marca TU caso
    FRASE              texto corto con tus números, para el parcial

Para los ejercicios completos del parcial:
    explicacion_ej1(MENSAJE, N)     conclusiones_ej1(MENSAJE, N)
    explicacion_ej2(ENTRADA, SALIDA) conclusiones_ej2(ENTRADA, SALIDA)

ayuda() lista todas las funciones que se pueden explicar.

Necesita en la misma carpeta: FuncionesParcial2.py (todas las funciones).
"""

import math

from FuncionesParcial2 import (
    CalcEntropia,
    extension_fuente, extension_codigo, detalle_primer_teorema, cumple_primer_teorema,
    rendimiento_redundancia, distancia_hamming, analizar_codigo_hamming, distancia_levenshtein,
    byte_con_paridad, verificar_byte, filas_de_bits, analizar_matriz_paridad,
    generar_mensaje_con_paridad, recuperar_mensaje, huffman, shannon_fano,
    alfabeto_y_probabilidades, resumen_codigo, decodificar_cadena, codificar_mensaje,
    decodificar_mensaje, tasa_compresion, tasa_compresion_codigo, rlc_texto, rlc_comprimir,
    rlc_descomprimir,
    canal_desde_secuencias, matriz_canal, probabilidades_salida, probabilidades_simultaneas,
    probabilidades_a_posteriori, entropias_a_posteriori, equivocacion, perdida, entropia_afin,
    informacion_mutua, analisis_canal, es_sin_ruido, es_determinante, canal_serie,
    es_reduccion_suficiente, matriz_determinante_reduccion, reducir_canal, es_uniforme,
    capacidad_canal, capacidad_binaria, probabilidad_error)

# Dos valores se consideran iguales si difieren en menos de esto (así el caso
# marcado coincide con lo que se ve redondeado a 4 decimales).
_EQ = 5e-5
_ANCHO = 78

# Para los tests: cuenta explicaciones en las que ningún caso coincidió.
SIN_CASO = []

# Nombres de los símbolos de entrada y salida del canal. Los fija
# explicar(canal_desde_secuencias, ...) para que las demás explicaciones digan
# "0", "1", "P", "Q"... en vez de a1, a2, b1, b2. Se usan solo si la matriz
# tiene la misma cantidad de filas/columnas. Cambiarlos: nombres_canal(...).
_NOMBRES = {"A": None, "B": None}


def nombres_canal(entradas=None, salidas=None):
    """Fija (o borra, sin argumentos) los nombres de entradas y salidas del canal."""
    _NOMBRES["A"] = list(entradas) if entradas else None
    _NOMBRES["B"] = list(salidas) if salidas else None


def _na(n):
    a = _NOMBRES["A"]
    return [str(x) for x in a] if a and len(a) == n else [f"a{i + 1}" for i in range(n)]


def _nb(n):
    b = _NOMBRES["B"]
    return [str(x) for x in b] if b and len(b) == n else [f"b{j + 1}" for j in range(n)]


# ---------------------------------------------------------------------------
# Herramientas de formato
# ---------------------------------------------------------------------------
def _f(x):
    return f"{x:.4f}"


def _pct(x):
    return f"{100 * x:.1f}%"


def _igual(a, b):
    return abs(a - b) <= _EQ


def _envolver(texto, sangria="  ", colgante="", primera=None):
    """Corta el texto en líneas de _ANCHO; las líneas de continuación llevan
    sangria + colgante."""
    lineas = []
    for k, parrafo in enumerate(str(texto).split("\n")):
        if not parrafo.strip():
            lineas.append("")
            continue
        actual = primera if (primera is not None and k == 0) else sangria
        for palabra in parrafo.split():
            if len(actual) + len(palabra) + 1 > _ANCHO and actual.strip(" |"):
                lineas.append(actual.rstrip())
                actual = sangria + colgante + palabra + " "
            else:
                actual += palabra + " "
        lineas.append(actual.rstrip())
    return lineas


def _ver_matriz(m, filas=None, cols=None):
    filas = filas or _na(len(m))
    cols = cols or _nb(len(m[0]))
    ancho = max(6, max(len(str(c)) for c in cols))
    cab = " " * 6 + "".join(str(c).rjust(ancho + 2) for c in cols)
    cuerpo = [str(f).rjust(5) + " " + "".join(_f(x).rjust(ancho + 2) for x in fila)
              for f, fila in zip(filas, m)]
    return "\n".join([cab] + cuerpo)


def _bloque(titulo, resultado, significa, obtuvo, casos, frase, notas=None):
    """casos: lista de (se_cumple, condicion, lectura)."""
    sep = "=" * _ANCHO
    out = [sep, " " + titulo, sep, "RESULTADO:"]
    for l in str(resultado).split("\n"):
        out.append("  " + l)
    out += ["", "QUÉ SIGNIFICA:"] + _envolver(significa)
    out += ["", 'CÓMO SE OBTUVO (para "explicar cómo se obtuvieron los resultados"):'] + _envolver(obtuvo)
    if casos:
        out += ["", "CÓMO LEERLO SEGÚN EL VALOR  (>> = tu caso):"]
        marcados = 0
        for cumple, cond, lectura in casos:
            marca = ">> " if cumple else "   "
            marcados += bool(cumple)
            out += _envolver(f"{cond}  ->  {lectura}", sangria="     ", colgante="      ", primera="  " + marca)
        if not marcados:
            SIN_CASO.append(titulo)
            out.append("   (ningún caso coincide: revisá los datos que le pasaste a la función)")
    if notas:
        out += ["", "OJO:"] + _envolver(notas)
    out += ["", "FRASE PARA EL PARCIAL:"] + _envolver(frase, sangria="  | ")
    out.append("")
    return "\n".join(out)


REGISTRO = []   # todo lo que se imprime, para poder guardarlo en un archivo


def _imprimir(texto):
    REGISTRO.append(str(texto))
    try:
        print(texto)
    except UnicodeEncodeError:
        # consola que no acepta acentos: se reemplazan para que no se corte
        print(str(texto).encode("ascii", "replace").decode("ascii"))


def guardar_registro(ruta):
    """Guarda en un archivo de texto todo lo que se imprimió hasta ahora."""
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write("\n".join(REGISTRO) + "\n")


def _lista(nombres):
    nombres = [str(n) for n in nombres]
    if not nombres:
        return ""
    if len(nombres) == 1:
        return nombres[0]
    return ", ".join(nombres[:-1]) + " y " + nombres[-1]


def _H(probs):
    return CalcEntropia([p for p in probs if p > 0])


def _L(probs, codigos):
    return sum(p * len(c) for p, c in zip(probs, codigos))


def _col(m, j):
    return [fila[j] for fila in m]


# ===========================================================================
# UNIDAD 4 y 5: fuentes, códigos y compresión
# ===========================================================================
def _x_entropia(res, probs):
    q = len(probs)
    hmax = math.log2(q) if q > 1 else 0.0
    h = res
    ratio = h / hmax if hmax > 0 else 0.0
    if h <= _EQ:
        frase = (f"H(S) = {_f(h)} bits/símbolo: un símbolo tiene probabilidad 1, así que la "
                 "fuente no aporta información (no hay incertidumbre).")
    else:
        if _igual(h, hmax):
            calif = "los símbolos son equiprobables: es la máxima incertidumbre posible"
        elif ratio >= 0.85:
            calif = ("está cerca del máximo: los símbolos son bastante parejos, así que hay poco margen "
                     "para comprimir respecto de un código de longitud fija")
        elif ratio >= 0.6:
            calif = "la fuente es moderadamente predecible"
        else:
            calif = "la fuente es muy predecible y se puede comprimir mucho"
        frase = (f"H(S) = {_f(h)} bits/símbolo: es la información media que aporta cada símbolo y el "
                 "mínimo de binits por símbolo que puede lograr en promedio un código unívoco. "
                 f"Es el {_pct(ratio)} del máximo log2({q}) = {_f(hmax)}: {calif}.")
    return _bloque(
        "ENTROPÍA DE LA FUENTE  H(S)",
        f"H(S) = {_f(h)} bits/símbolo   (máximo posible con {q} símbolos: log2({q}) = {_f(hmax)})",
        "Es la cantidad media de información que aporta cada símbolo. También es el PISO de la "
        "longitud media: ningún código unívoco puede usar, en promedio, menos binits por símbolo "
        "que H (en base 2).",
        "H(S) = suma de P(si) * log2(1/P(si)): el promedio, ponderado por la probabilidad, de la "
        "cantidad de información de cada símbolo.",
        [(h <= _EQ, "H = 0", "un símbolo es seguro; la fuente no informa nada."),
         (h > _EQ and _igual(h, hmax), f"H = log2(q) = {_f(hmax)}",
          "símbolos equiprobables: máxima incertidumbre, no se puede comprimir por debajo de un "
          "código de longitud fija."),
         (h > _EQ and not _igual(h, hmax), f"0 < H < {_f(hmax)}",
          "hay símbolos más probables que otros; cuanto más lejos del máximo, más predecible y "
          "más compresible.")],
        frase)


def _x_alfabeto(res, mensaje):
    alfabeto, probs = res
    n = len(mensaje)
    pmax, pmin = max(probs), min(probs)
    mas = [s for s, p in zip(alfabeto, probs) if _igual(p, pmax)]
    menos = [s for s, p in zip(alfabeto, probs) if _igual(p, pmin)]
    tabla = "\n".join(f"P({s!r}) = {_f(p)}   ({mensaje.count(s)} de {n})" for s, p in zip(alfabeto, probs))
    equi = _igual(pmax, pmin)
    frase = (f"Las probabilidades se estimaron como la frecuencia relativa de cada símbolo en el "
             f"mensaje de {n} símbolos (cantidad de apariciones / {n}), considerando la fuente de "
             f"memoria nula. ")
    if len(alfabeto) == 1:
        frase += f"El mensaje usa un único símbolo ({alfabeto[0]!r}), con probabilidad 1."
    elif equi:
        frase += f"Los {len(alfabeto)} símbolos son equiprobables (P = {_f(pmax)} cada uno)."
    else:
        frase += (f"El más probable es {_lista(mas)} ({_f(pmax)}) y el menos probable "
                  f"{_lista(menos)} ({_f(pmin)}).")
    return _bloque(
        "ALFABETO Y PROBABILIDADES DE LA FUENTE",
        tabla + f"\nSuma = {_f(sum(probs))}",
        "Es la fuente de información que representa el mensaje: qué símbolos emite y con qué "
        "probabilidad. Se supone fuente de MEMORIA NULA (cada símbolo no depende del anterior); "
        "por eso después vale H(S^n) = n * H(S).",
        "Frecuencia relativa: veces que aparece cada símbolo dividido el largo del mensaje.",
        [(len(alfabeto) == 1, "un solo símbolo", "no hay incertidumbre (H = 0)."),
         (len(alfabeto) > 1 and equi, "todas iguales", "fuente equiprobable: H = log2(q), la máxima."),
         (len(alfabeto) > 1 and not equi, "distintas", "hay símbolos más frecuentes: se pueden "
          "comprimir dándoles palabras más cortas.")],
        frase)


def _x_huffman(res, probs):
    codigos = res
    q = len(probs)
    l = _L(probs, codigos)
    h = _H(probs)
    lens = [len(c) for c in codigos]
    tabla = "\n".join(f"S{i + 1}  P = {_f(p)}  ->  {c}   (longitud {len(c)})"
                      for i, (p, c) in enumerate(zip(probs, codigos)))
    iguales = q > 1 and len(set(lens)) == 1
    ideal = q > 1 and _igual(l, h)
    frase = ("El código se obtuvo con Huffman: se unen repetidamente los dos símbolos (o grupos) "
             "menos probables sumando sus probabilidades y se asigna 0 y 1 a cada rama; la palabra "
             "de cada símbolo es el camino desde la raíz hasta él. Es instantáneo (ninguna palabra "
             f"es prefijo de otra) y compacto: L = {_f(l)} binits/símbolo es la menor longitud media "
             f"posible codificando símbolo a símbolo (H = {_f(h)}).")
    if ideal:
        frase += " Además L = H: es un código ideal, porque las probabilidades son potencias de 1/2."
    elif q > 1:
        frase += (" No llega a H porque las longitudes tienen que ser enteras y las probabilidades "
                  "no son potencias de 1/2.")
    return _bloque(
        "CÓDIGO DE HUFFMAN (código binario óptimo)",
        tabla + f"\nL = {_f(l)} binits/símbolo   H = {_f(h)} bits/símbolo",
        '"Código óptimo" = Huffman. Es COMPACTO (la menor L posible para esa fuente, codificando '
        "símbolo a símbolo) e INSTANTÁNEO (se decodifica palabra por palabra). Si hay "
        "probabilidades empatadas pueden salir otras palabras u otras longitudes, pero la L es "
        "siempre la misma.",
        "Algoritmo de Huffman: unir los dos menos probables, sumar, repetir hasta tener un solo "
        "nodo; 0 y 1 en cada rama; la palabra es el camino desde la raíz.",
        [(q == 1, "un solo símbolo", "no hace falta codificar (se usa una palabra de 1 binit)."),
         (iguales, "todas las palabras miden lo mismo",
          "las probabilidades están parejas: Huffman coincide con un código de longitud fija."),
         (ideal, "L = H", "código ideal (eficiencia 100%): cada P es potencia de 1/2."),
         (q > 1 and not ideal, "L > H", "es lo normal: Huffman es óptimo pero las longitudes "
          "enteras le impiden llegar a H; para acercarse hay que codificar extensiones.")],
        frase)


def _x_shannon_fano(res, probs):
    codigos = res
    l = _L(probs, codigos)
    lh = _L(probs, huffman(probs)) if len(probs) > 1 else l
    h = _H(probs)
    tabla = "\n".join(f"S{i + 1}  P = {_f(p)}  ->  {c}" for i, (p, c) in enumerate(zip(probs, codigos)))
    igual = _igual(l, lh)
    frase = ("El código se obtuvo con Shannon-Fano: se ordenan los símbolos de mayor a menor "
             "probabilidad y se dividen en dos grupos de probabilidad lo más parecida posible "
             "(uno recibe 1 y el otro 0), repitiendo dentro de cada grupo. "
             f"L = {_f(l)} binits/símbolo (H = {_f(h)}). ")
    frase += (f"Coincide con la de Huffman, así que para esta fuente también es óptimo."
              if igual else
              f"Es mayor que la de Huffman ({_f(lh)}): Shannon-Fano es más simple pero no siempre óptimo.")
    return _bloque(
        "CÓDIGO DE SHANNON-FANO",
        tabla + f"\nL = {_f(l)}   (Huffman: {_f(lh)})   H = {_f(h)}",
        "Otro método para armar un código instantáneo. Es más simple que Huffman pero no "
        "garantiza la L mínima: puede igualarlo o quedar por encima, nunca por debajo.",
        "Ordenar por probabilidad, partir en dos grupos de suma parecida (1 arriba, 0 abajo) y "
        "repetir en cada grupo.",
        [(igual, "L(SF) = L(Huffman)", "Shannon-Fano también es óptimo para esta fuente."),
         (not igual, "L(SF) > L(Huffman)", "Shannon-Fano no es óptimo acá; Huffman comprime más.")],
        frase)


def _x_extension_fuente(res, probs, n):
    q = len(probs)
    h = _H(probs)
    return _bloque(
        f"EXTENSIÓN DE ORDEN {n} DE LA FUENTE",
        f"{len(res)} símbolos (q^n = {q}^{n}); suman {_f(sum(res))}\nH(S^{n}) = {n} * H(S) = "
        f"{n} * {_f(h)} = {_f(n * h)} bits por bloque",
        f"Cada símbolo de S^{n} es un bloque de {n} símbolos de la fuente. Con fuente de memoria "
        "nula, su probabilidad es el producto de las probabilidades de sus símbolos, y por eso "
        "H(S^n) = n * H(S). Codificar bloques es lo que permite acercar la longitud media por "
        "símbolo a la entropía (Primer Teorema de Shannon).",
        f"Se formaron los {q}^{n} = {len(res)} bloques posibles y la probabilidad de cada uno es el "
        "producto de las probabilidades de los símbolos que lo forman.",
        [(n == 1, "n = 1", "es la misma fuente."),
         (n > 1, f"n = {n}", f"bloques de {n} símbolos; la tabla crece a {len(res)} palabras.")],
        f"La extensión de orden {n} tiene {len(res)} símbolos (bloques de {n}); por ser una fuente de "
        f"memoria nula, la probabilidad de cada bloque es el producto de las de sus símbolos y "
        f"H(S^{n}) = {n} * H(S) = {_f(n * h)} bits por bloque.",
        "H(S^n) = n * H(S) solo vale para fuentes SIN memoria (fue el error del primer parcial).")


def _x_extension_codigo(res, codigos, n):
    return _bloque(
        f"CÓDIGO DE LA EXTENSIÓN POR CONCATENACIÓN (orden {n})",
        f"{len(res)} palabras; ejemplo: {', '.join(res[:4])}{' ...' if len(res) > 4 else ''}",
        "Es el código de la extensión que se obtiene pegando las palabras del código original "
        "(al bloque SiSj le toca ci + cj). Su longitud media es exactamente n veces la original, "
        "así que por símbolo NO mejora nada.",
        "Concatenando las palabras código de cada símbolo del bloque.",
        [],
        f"Concatenando las palabras se obtiene L_{n} = {n} * L, es decir L_{n}/{n} = L: codificar la "
        "extensión así no mejora la compresión; para mejorarla hay que aplicar Huffman a la extensión.",
        'Si el parcial dice "código óptimo para la extensión", NO es este: es huffman(extension_fuente(probs, n)).')


def _x_detalle_teorema(res, probs, codigos, n, r=None):
    d = res if isinstance(res, dict) else detalle_primer_teorema(probs, codigos, n, r)
    h, ln, lnn, cota, rr = d["H"], d["Ln"], d["Ln_sobre_n"], d["cota_superior"], d["r"]
    cumple = d["cumple"]
    debajo = (not cumple) and lnn < h
    arriba = (not cumple) and not debajo
    ideal = cumple and _igual(lnn, h)
    frase = (f"{'Cumple' if cumple else 'No cumple'} el Primer Teorema de Shannon: con H{rr}(S) = {_f(h)}, "
             f"L_{n}/{n} = {_f(ln)}/{n} = {_f(lnn)} y H + 1/{n} = {_f(cota)}, "
             f"{'se verifica' if cumple else 'no se verifica'} H <= L_n/n < H + 1/n. ")
    if ideal:
        frase += "Además L_n/n = H: el código alcanza la entropía."
    elif cumple:
        frase += "El código es eficiente para ese orden de extensión."
        if n > 1:
            frase += f" Al aumentar n la franja de ancho 1/n se achica y L_n/n se acerca a H."
    elif debajo:
        frase += ("L_n/n queda por debajo de la entropía, cosa imposible para un código unívoco: "
                  "el código no es unívocamente decodificable (o hay un error en los datos).")
    else:
        frase += ("L_n/n queda por encima de H + 1/n: el código es largo de más, no es compacto; "
                  "se puede mejorar con Huffman o codificando una extensión de mayor orden.")
    return _bloque(
        f"PRIMER TEOREMA DE SHANNON (n = {n})",
        f"H{rr}(S) = {_f(h)}   L_{n} = {_f(ln)}   L_{n}/{n} = {_f(lnn)}   H + 1/{n} = {_f(cota)}\n"
        f"Veredicto: {'CUMPLE' if cumple else 'NO CUMPLE'}",
        "El teorema dice que con un código compacto de la extensión de orden n se logra "
        "H <= L_n/n < H + 1/n: nunca menos que la entropía y a menos de 1/n de ella. Al crecer n, "
        "L_n/n tiende a H.",
        f"Se calculó H en base {rr} (tamaño del alfabeto del código), la longitud media L_{n} del "
        f"código de la extensión (con las probabilidades de la extensión) y se verificó "
        f"H <= L_{n}/{n} < H + 1/{n}.",
        [(debajo, "L_n/n < H", "imposible para un código unívoco: el código no es unívoco o hay un error."),
         (ideal, "L_n/n = H", "cumple y alcanza la entropía (código ideal)."),
         (cumple and not ideal, "H <= L_n/n < H + 1/n", "cumple: código eficiente para ese n "
          "(Huffman SIEMPRE cumple)."),
         (arriba, "L_n/n >= H + 1/n", "no cumple: decodificable pero largo de más; no es compacto.")],
        frase,
        "Si un código de Huffman te da 'no cumple', revisá los datos: Huffman siempre cumple."
        if not cumple else None)


def _x_cumple_teorema(res, probs, codigos, n, r=None):
    return _x_detalle_teorema(detalle_primer_teorema(probs, codigos, n, r), probs, codigos, n, r)


def _calif_eta(eta):
    if eta > 1 + _EQ:
        return "imposible"
    if _igual(eta, 1):
        return "ideal"
    if eta >= 0.95:
        return "muy eficiente"
    if eta >= 0.8:
        return "eficiente pero mejorable"
    return "poco eficiente"


def _casos_eta(eta):
    c = _calif_eta(eta)
    return [(c == "imposible", "η > 1", "imposible: L < H; el código no es unívoco o hay un error."),
            (c == "ideal", "η = 1  (R = 0)", "código ideal: cada probabilidad es potencia de 1/r."),
            (c == "muy eficiente", "0,95 <= η < 1", "muy eficiente: casi no desperdicia binits."),
            (c == "eficiente pero mejorable", "0,80 <= η < 0,95",
             "eficiente pero mejorable (con Huffman o con extensiones)."),
            (c == "poco eficiente", "η < 0,80", "poco eficiente: mucha redundancia, conviene otro código.")]


def _frase_eta(eta, red, l, h, unidad="símbolo"):
    unidad_txt = f" binits por {unidad}" if unidad else " binits"
    c = _calif_eta(eta)
    if c == "imposible":
        return (f"η = {_f(eta)} > 1, es decir L = {_f(l)} < H = {_f(h)}: eso es imposible para un código "
                "unívoco, así que el código no es unívocamente decodificable (o hay un error en los datos).")
    base = (f"L = {_f(l)}{unidad_txt}, η = H/L = {_f(eta)} y R = 1 - η = {_f(red)}: el "
            f"{_pct(eta)} de los binits transporta información y el {_pct(red)} es redundancia. ")
    return base + {"ideal": "Es un código ideal: alcanza la entropía.",
                   "muy eficiente": "Es un código muy eficiente, muy cerca de la entropía.",
                   "eficiente pero mejorable": "Es eficiente pero se puede mejorar (por ejemplo codificando extensiones).",
                   "poco eficiente": "Es poco eficiente: tiene mucha redundancia."}[c]


def _x_rendimiento(res, probs, codigos, r=None):
    eta, red = res
    rr = r or max(2, len(set("".join(codigos))))
    h = _H(probs) / math.log2(rr)
    l = _L(probs, codigos)
    return _bloque(
        "RENDIMIENTO Y REDUNDANCIA",
        f"η = {_f(eta)}   R = {_f(red)}   (H{rr} = {_f(h)}, L = {_f(l)})",
        "η = H/L mide qué parte de cada símbolo de código lleva información real; R = 1 - η es la "
        "parte desperdiciada. Sirven para comparar códigos de la MISMA fuente: el de mayor η es mejor.",
        f"η = H{rr}(S) / L, con L = suma de P(si) * longitud(ci); R = 1 - η.",
        _casos_eta(eta),
        _frase_eta(eta, red, l, h),
        "Si le pasaste la extensión de orden n, L es por BLOQUE y η = n*H(S)/L_n "
        "(los tres números tienen que cerrar entre sí).")


def _x_resumen(res, probs, codigos):
    h, l, eta, red = res["H"], res["L"], res["rendimiento"], res["redundancia"]
    return _bloque(
        "RESUMEN DEL CÓDIGO (H, L, η, R)",
        f"H = {_f(h)}   L = {_f(l)}   η = {_f(eta)}   R = {_f(red)}",
        "L es la longitud media (binits por símbolo); siempre L >= H en un código unívoco. "
        "η = H/L es el rendimiento y R = 1 - η la redundancia.",
        "L = suma de P(si) * longitud(ci); η = H/L; R = 1 - η.",
        _casos_eta(eta),
        _frase_eta(eta, red, l, h, unidad=None),
        f"Si son las probabilidades de una extensión de orden n, L = {_f(l)} es por bloque de n "
        f"símbolos y H = n * H(S); por símbolo original sería L/n.")


def _x_tasa(res, mensaje, comprimido, como_fraccion=False):
    a, b = len(mensaje), len(comprimido)
    t = a / b
    casos = [(t > 1 + 1e-12, "tasa > 1", "hubo compresión; cuanto más grande, mejor."),
             (abs(t - 1) <= 1e-12, "tasa = 1", "el comprimido ocupa lo mismo que el original."),
             (t < 1 - 1e-12, "tasa < 1", "el 'comprimido' ocupa MÁS que el original: no conviene.")]
    if t > 1:
        cierre = f"el comprimido ocupa el {_pct(b / a)} del original."
    elif t < 1:
        cierre = "el resultado ocupa más que el original, así que ese método no conviene para este mensaje."
    else:
        cierre = "no se ganó espacio."
    return _bloque(
        "TASA DE COMPRESIÓN",
        f"{res}   ({a} bytes originales / {b} bytes comprimidos = {_f(t)} : 1)",
        "Tamaño original / tamaño comprimido. Se lee 'N : 1': el original ocupa N veces lo que "
        "ocupa el comprimido.",
        "Se dividió el tamaño original (1 byte ASCII por carácter) por la cantidad de bytes del "
        "mensaje comprimido.",
        casos,
        f"Tasa de compresión {_f(t)} : 1: el original ocupa {a} bytes y el comprimido {b}; {cierre}",
        "Si el comprimido viene de codificar_mensaje con cabecera=True, incluye 1 byte extra. En el "
        "parcial usá tasa_compresion_codigo.")


def _x_tasa_codigo(res, mensaje, alfabeto, codigos):
    n = len(mensaje)
    tabla = {s: c for s, c in zip(alfabeto, codigos)}
    bits = sum(len(tabla[c]) for c in mensaje)
    nbytes = math.ceil(bits / 8)
    t = res
    exacta = 8 * n / bits if bits else float("inf")
    casos = [(t > 1 + 1e-12, "tasa > 1", "comprime."),
             (abs(t - 1) <= 1e-12, "tasa = 1", "no gana espacio."),
             (t < 1 - 1e-12, "tasa < 1", "agranda el mensaje (no debería pasar con Huffman sobre ASCII).")]
    frase = (f"Tasa de compresión {_f(t)} : 1. El mensaje original ocupa {8 * n} bits ({n} caracteres "
             f"de 8 bits ASCII) y codificado ocupa {bits} bits ({nbytes} bytes), porque cada símbolo "
             f"pasa de 8 bits a {_f(bits / n)} binits en promedio. ")
    if t > 1:
        frase += f"El mensaje comprimido ocupa el {_pct(1 / t)} del original."
    notas = "La tasa es aproximadamente 8 / L."
    if bits % 8:
        notas += (f" Los {bits} bits no completan bytes enteros: se redondeó a {nbytes} bytes. "
                  f"Contando bits exactos daría {_f(exacta)} : 1.")
    return _bloque(
        "TASA DE COMPRESIÓN DEL MENSAJE CODIFICADO",
        f"{_f(t)} : 1   ({8 * n} bits originales, {bits} bits codificados = {nbytes} bytes)",
        "Cuánto se achica el mensaje al reemplazar cada carácter ASCII (8 bits) por su palabra "
        "código, sin agregar ningún byte extra (como pide la aclaración del parcial).",
        "Tamaño original (8 bits por carácter) dividido el tamaño codificado (suma de las "
        "longitudes de las palabras de cada símbolo del mensaje, en bytes enteros).",
        casos, frase, notas)


def _x_codificar(res, mensaje, alfabeto, codigos, cabecera=True):
    tabla = {s: c for s, c in zip(alfabeto, codigos)}
    bits = sum(len(tabla[c]) for c in mensaje)
    relleno = (8 - bits % 8) % 8
    return _bloque(
        "MENSAJE CODIFICADO EN BYTES",
        f"{len(res)} bytes  ({bits} bits de datos + {relleno} de relleno"
        f"{' + 1 byte de cabecera' if cabecera else ''})",
        "Es el mensaje comprimido real: cada carácter reemplazado por su palabra código y los bits "
        "empaquetados de a 8.",
        "Se concatenaron las palabras código de cada carácter y se agruparon los bits de a 8 "
        "(completando el último byte con ceros).",
        [(cabecera, "cabecera=True", "el primer byte guarda cuántos ceros de relleno hay (sirve para decodificar)."),
         (not cabecera, "cabecera=False", "solo están los bits de las palabras (lo que pide el parcial).")],
        f"El mensaje de {len(mensaje)} caracteres codificado ocupa {bits} bits, que se guardan en {len(res)} bytes.")


def _x_decodificar(res, secuencia, alfabeto, codigos):
    return _bloque(
        "MENSAJE DECODIFICADO",
        repr(res),
        "Es el texto recuperado a partir de los bytes comprimidos. La compresión con Huffman o "
        "Shannon-Fano es SIN PÉRDIDA: tiene que salir exactamente el original.",
        "Se pasaron los bytes a bits, se quitó el relleno y se fue leyendo bit a bit hasta formar "
        "una palabra código (se puede porque el código es instantáneo).",
        [],
        f"Se recuperó el mensaje {res!r}, idéntico al original: es una compresión sin pérdida, posible "
        "porque el código es instantáneo.")


def _x_decodificar_cadena(res, mensaje, simbolos, codigos):
    return _bloque(
        "DECODIFICACIÓN DE LA CADENA",
        " ".join(map(str, res)),
        "La secuencia de símbolos de la fuente que corresponde al mensaje codificado.",
        "Se lee el mensaje de izquierda a derecha y cada vez que lo leído forma una palabra del "
        "código se escribe su símbolo; funciona porque el código es instantáneo.",
        [],
        f"Leyendo el mensaje y reconociendo cada palabra apenas termina (el código es instantáneo) "
        f"se obtiene: {' '.join(map(str, res))}.")


def _rafagas(m):
    r = []
    for c in m:
        if r and r[-1][0] == c:
            r[-1][1] += 1
        else:
            r.append([c, 1])
    return r


def _casos_rlc(prom):
    return [(prom > 2 + 1e-12, "ráfaga promedio > 2", "RLC comprime."),
            (abs(prom - 2) <= 1e-12, "ráfaga promedio = 2", "ocupa lo mismo que el original."),
            (prom < 2 - 1e-12, "ráfaga promedio < 2", "RLC agranda el mensaje: no conviene.")]


def _x_rlc_texto(res, mensaje):
    raf = _rafagas(mensaje)
    prom = len(mensaje) / len(raf) if raf else 0
    return _bloque(
        "RLC (en texto)",
        f"{res}   ({len(raf)} ráfagas, largo promedio {_f(prom)})",
        "Run Length Coding reemplaza cada ráfaga de caracteres iguales seguidos por "
        "(carácter, cantidad). Guardando 2 bytes por ráfaga, solo comprime si las ráfagas miden "
        "más de 2 en promedio.",
        "Se recorrió el mensaje contando cuántas veces seguidas se repite cada carácter.",
        _casos_rlc(prom),
        f"El mensaje de {len(mensaje)} caracteres tiene {len(raf)} ráfagas ({res}), de "
        f"{_f(prom)} caracteres en promedio; con 2 bytes por ráfaga ocupa {2 * len(raf)} bytes, así que "
        f"{'comprime' if prom > 2 else ('queda igual' if prom == 2 else 'no comprime')}.")


def _x_rlc_comprimir(res, mensaje):
    raf = _rafagas(mensaje)
    prom = len(mensaje) / len(raf) if raf else 0
    t = len(mensaje) / len(res) if len(res) else float("inf")
    return _bloque(
        "RLC COMPRIMIDO (bytes)",
        f"{len(res)} bytes para {len(mensaje)} caracteres  ->  tasa {_f(t)} : 1",
        "Cada ráfaga ocupa 2 bytes: el código ASCII del carácter y la cantidad de repeticiones.",
        "Se reemplazó cada ráfaga por el par (carácter, cantidad), un byte cada uno.",
        _casos_rlc(prom),
        f"Con RLC el mensaje pasa de {len(mensaje)} a {len(res)} bytes (tasa {_f(t)} : 1), porque tiene "
        f"{len(raf)} ráfagas de {_f(prom)} caracteres en promedio. RLC conviene solo cuando hay "
        "ráfagas largas de caracteres repetidos.")


def _x_rlc_descomprimir(res, secuencia):
    return _bloque("RLC DESCOMPRIMIDO", repr(res),
                   "El mensaje original reconstruido: RLC es sin pérdida.",
                   "Se repitió cada carácter la cantidad de veces indicada en el byte siguiente.",
                   [], f"Se recuperó el mensaje {res!r} sin pérdida.")


# ---------------------------------------------------------------------------
# Control de errores
# ---------------------------------------------------------------------------
def _x_dist_hamming(res, a, b):
    pos = [i + 1 for i, (x, y) in enumerate(zip(a, b)) if x != y]
    return _bloque(
        "DISTANCIA DE HAMMING ENTRE DOS PALABRAS",
        f"d({a}, {b}) = {res}" + (f"   (difieren en las posiciones {pos})" if pos else ""),
        "Cantidad de posiciones en que difieren dos palabras de igual longitud: cuántos errores de "
        "bit hacen falta para convertir una en la otra.",
        "Comparando posición por posición y contando las diferencias.",
        [(res == 0, "d = 0", "son la misma palabra."),
         (res > 0, f"d = {res}", f"hacen falta {res} errores para confundirlas.")],
        f"La distancia de Hamming entre {a} y {b} es {res}: difieren en {res} posiciones, así que "
        f"hacen falta {res} errores de bit para transformar una en la otra.")


def _x_hamming_codigo(res, codigos):
    d, det, cor = res
    codigos = list(codigos)
    par = None
    for i in range(len(codigos)):
        for j in range(i + 1, len(codigos)):
            if distancia_hamming(codigos[i], codigos[j]) == d:
                par = (codigos[i], codigos[j])
                break
        if par:
            break
    if d == 0:
        frase = f"La distancia del código es 0 porque hay palabras repetidas ({par[0]}): no es un código válido."
    elif d == 1:
        frase = (f"La distancia de Hamming del código es 1 (por ejemplo entre {par[0]} y {par[1]}): no se "
                 "pueden detectar ni corregir errores, porque un solo error puede convertir una palabra "
                 "válida en otra palabra válida.")
    elif d == 2:
        frase = (f"La distancia de Hamming del código es 2 (por ejemplo entre {par[0]} y {par[1]}): se puede "
                 "detectar un error pero no corregir ninguno, porque una palabra con un error queda a la "
                 "misma distancia de dos palabras válidas.")
    else:
        frase = (f"La distancia de Hamming del código es {d} (la mínima, por ejemplo entre {par[0]} y "
                 f"{par[1]}): se pueden detectar hasta d - 1 = {det} errores y corregir hasta "
                 f"(d - 1)/2 = {cor} (parte entera).")
    return _bloque(
        "DISTANCIA DE HAMMING DEL CÓDIGO (detección y corrección)",
        f"d_min = {d}   detecta {det}   corrige {cor}",
        "d_min es la menor distancia entre dos palabras del código. Mide cuántos errores hacen "
        "falta para que una palabra válida se transforme en otra válida. Detecta d-1 errores y "
        "corrige (d-1)/2 (parte entera); detectar y corregir comparten esa capacidad.",
        "Se calculó la distancia de Hamming entre todos los pares de palabras y se tomó la mínima; "
        "detecta = d - 1 y corrige = parte entera de (d - 1)/2.",
        [(d == 0, "d = 0", "hay palabras repetidas: código inválido."),
         (d == 1, "d = 1", "no detecta ni corrige nada."),
         (d == 2, "d = 2", "detecta 1 error, no corrige (como un bit de paridad)."),
         (d == 3, "d = 3", "detecta hasta 2 o corrige 1."),
         (d >= 4, "d >= 4", f"detecta hasta {max(d - 1, 0)} y corrige hasta {max((d - 1) // 2, 0)}.")],
        frase)


def _x_levenshtein(res, a, b):
    mismo = len(a) == len(b)
    hm = distancia_hamming(a, b) if mismo else None
    casos = [(res == 0, "0", "las cadenas son iguales."),
             (res > 0 and mismo, "misma longitud",
              f"Hamming daría {hm}; Levenshtein siempre es <= Hamming."),
             (res > 0 and not mismo, "longitudes distintas",
              f"Hamming no se puede usar; Levenshtein es al menos la diferencia de largos ({abs(len(a) - len(b))}).")]
    frase = (f"La distancia de Levenshtein entre {a!r} y {b!r} es {res}: es la menor cantidad de "
             "inserciones, eliminaciones o sustituciones necesarias para transformar una cadena en la otra.")
    if mismo and res < hm:
        frase += f" Es menor que la de Hamming ({hm}) porque insertar y borrar resulta más barato que sustituir."
    elif not mismo:
        frase += " A diferencia de Hamming, sirve para cadenas de distinta longitud."
    return _bloque(
        "DISTANCIA DE LEVENSHTEIN",
        f"{res}" + (f"   (Hamming: {hm})" if mismo else ""),
        "Distancia de edición: mínimo de operaciones (insertar, borrar o sustituir un símbolo) para "
        "pasar de una cadena a otra. Se usa cuando el canal puede agregar o perder símbolos.",
        "Programación dinámica: se arma la tabla de costos mínimos entre todos los prefijos de las "
        "dos cadenas.",
        casos, frase,
        "Solo corresponde usarla si el canal puede insertar o borrar símbolos; si solo invierte "
        "bits, la medida correcta es Hamming.")


def _x_byte_paridad(res, caracter):
    b = format(res, "08b")
    return _bloque(
        "CARÁCTER CON BIT DE PARIDAD",
        f"{caracter!r} -> {b}   (ASCII {b[:7]} + paridad {b[7]})",
        "Los 7 bits ASCII del carácter más un bit de paridad PAR al final, elegido para que el byte "
        "tenga cantidad par de unos. Permite detectar 1 error (d_min = 2) pero no corregirlo.",
        "Se contó la cantidad de unos del ASCII y se agregó un 1 si era impar o un 0 si era par.",
        [(b[7] == "1", "paridad = 1", "el ASCII tenía cantidad impar de unos."),
         (b[7] == "0", "paridad = 0", "el ASCII ya tenía cantidad par de unos.")],
        f"El carácter {caracter!r} (ASCII {b[:7]}) tiene {b[:7].count('1')} unos, así que el bit de "
        f"paridad par es {b[7]} y el byte queda {b}.")


def _x_verificar_byte(res, byte):
    val = byte[0] if isinstance(byte, (bytes, bytearray)) else byte
    b = format(val, "08b")
    return _bloque(
        "VERIFICACIÓN DE PARIDAD DE UN BYTE",
        f"{b}: {b.count('1')} unos -> {'correcto' if res else 'ERROR'}",
        "Con paridad par, un byte correcto tiene cantidad par de unos.",
        "Se contó la cantidad de unos del byte.",
        [(res, "True", "paridad correcta: no se detectan errores (pero podría haber 2)."),
         (not res, "False", "hubo un error (o una cantidad impar): se detecta pero no se sabe qué bit, no se corrige.")],
        (f"El byte {b} tiene {b.count('1')} unos (par): no se detectan errores. Igual, un número par de "
         "errores pasaría desapercibido." if res else
         f"El byte {b} tiene {b.count('1')} unos (impar): hay un error. La paridad simple lo detecta pero "
         "no permite saber qué bit falló ni corregirlo."))


def _x_filas_bits(res, cadena, ancho=8):
    return _bloque(
        "MATRIZ DE BITS",
        "\n".join(f"fila {i + 1}: {f}" + ("   <- paridad longitudinal (LRC)" if i == 0 else f"   <- carácter {i}")
                  for i, f in enumerate(res)),
        "La tira de bits cortada en filas de 8. Formato de la cátedra: la PRIMERA fila es la paridad "
        "longitudinal (su último bit es la paridad cruzada) y cada una de las otras es un carácter "
        "(7 bits ASCII + paridad vertical).",
        f"Se cortó la secuencia de {len(cadena)} bits en {len(res)} filas de {ancho}.",
        [],
        f"Los {len(cadena)} bits forman {len(res)} filas de {ancho}: la primera es la paridad longitudinal "
        f"y las otras {len(res) - 1} son caracteres ASCII con su bit de paridad vertical.")


def _x_matriz_paridad(res, filas):
    filas = [str(f) for f in filas]
    est = res["estado"]
    fe, ce, pos = res["filas_con_error"], res["columnas_con_error"], res["posicion_error"]
    nch = len(filas) - 1
    tabla = "\n".join(f"fila {i + 1}: {f}" + ("  (LRC)" if i == 0 else "") +
                      ("   <- falla" if (i + 1) in fe else "") for i, f in enumerate(filas))
    tabla += f"\ncolumnas que fallan: {ce if ce else 'ninguna'}\nestado: {est}"
    if res["mensaje"]:
        tabla += f"\nmensaje: {res['mensaje']!r}"
    estructura = (f"La matriz tiene {len(filas)} filas: la primera es la paridad longitudinal (LRC) y "
                  f"las otras {nch} son caracteres (7 bits ASCII + paridad vertical), con paridad par. ")
    donde = ""
    if est == "corregido":
        i, j = pos
        if i == 1 and j == 8:
            donde = "el error estaba en el bit de paridad cruzada, así que los caracteres ya estaban bien"
        elif i == 1:
            donde = "el error estaba en la fila de paridad longitudinal, así que los caracteres ya estaban bien"
        elif j == 8:
            donde = f"el error estaba en el bit de paridad vertical del carácter {i - 1}, que ya estaba bien"
        else:
            donde = f"el error estaba en un bit de datos del carácter {i - 1}"
        frase = (estructura + f"Falla la paridad de la fila {i} y de la columna {j}, así que hay un único "
                 f"error en su intersección; {donde}. Invirtiendo ese bit se recupera el mensaje "
                 f"{res['mensaje']!r}. Con paridad vertical, longitudinal y cruzada (d_min = 4) se "
                 "detectan hasta 3 errores y se corrige 1.")
    elif est == "sin_errores":
        frase = (estructura + "Todas las filas y columnas tienen paridad correcta, así que no se "
                 f"detectan errores y el mensaje es {res['mensaje']!r}.")
    else:
        if fe and ce:
            motivo = f"fallan {len(fe)} filas ({fe}) y {len(ce)} columnas ({ce})"
        elif fe:
            motivo = f"fallan las filas {fe} pero ninguna columna"
        else:
            motivo = f"fallan las columnas {ce} pero ninguna fila"
        frase = (estructura + f"Se detectan errores: {motivo}. Eso no corresponde a un error simple "
                 "(hay al menos 2 errores), así que se pueden detectar pero no corregir: el mensaje "
                 "no es recuperable y habría que pedir la retransmisión.")
    return _bloque(
        "PARIDAD VERTICAL, LONGITUDINAL Y CRUZADA",
        tabla,
        "Cada fila y cada columna deben tener cantidad par de unos. Un error simple hace fallar "
        "exactamente UNA fila y UNA columna, y el bit equivocado está en su cruce. d_min = 4: "
        "detecta hasta 3 errores y corrige 1.",
        "Se armó la matriz de bits, se verificó la paridad par de cada fila y de cada columna, se "
        "invirtió el bit del cruce (si había un error simple) y se decodificaron los 7 bits ASCII "
        "de cada carácter.",
        [(est == "sin_errores", "ninguna fila ni columna falla", "el mensaje llegó bien."),
         (est == "corregido", "falla 1 fila y 1 columna", "error simple en el cruce: se corrige."
          + (f" ({donde})" if donde else "")),
         (est == "no_corregible", "otro patrón de fallas", "2 o más errores: se detectan, no se corrigen.")],
        frase,
        "Escribí el MENSAJE como texto (ej.: SOL), no la tira de bits corregida. Si hubiera 3 "
        "errores con forma de error simple, se 'corregiría' mal sin poder notarlo.")


def _x_generar_paridad(res, cadena):
    filas = [format(b, "08b") for b in res]
    return _bloque(
        "MENSAJE CON PARIDAD VERTICAL, LONGITUDINAL Y CRUZADA",
        "\n".join(f"{f}" + ("  (LRC)" if i == 0 else f"  {cadena[i - 1]!r}") for i, f in enumerate(filas)),
        "El texto protegido: una fila LRC y una fila por carácter. Permite detectar hasta 3 errores "
        "y corregir 1.",
        "Cada carácter es su ASCII de 7 bits + paridad par; la primera fila es la paridad de cada columna.",
        [],
        f"El mensaje {cadena!r} se transmite en {len(res)} bytes: {len(cadena)} caracteres con paridad "
        "vertical y una fila de paridad longitudinal (con el bit de paridad cruzada).")


def _x_recuperar(res, secuencia):
    return _bloque(
        "MENSAJE RECUPERADO",
        repr(res),
        "El texto original si no hubo errores o si había un solo error (corregido); cadena vacía si "
        "los errores no se pueden corregir.",
        "Se verificaron las paridades de filas y columnas y se corrigió el bit del cruce si había un error simple.",
        [(res != "", "texto", "mensaje correcto (sin errores o con un error corregido)."),
         (res == "", "cadena vacía", "errores detectados que no se pueden corregir: pedir retransmisión.")],
        (f"Se recuperó el mensaje {res!r}." if res else
         "Se detectaron errores que no se pueden corregir (más de uno): el mensaje no es recuperable."))


# ===========================================================================
# UNIDAD 6: canales
# ===========================================================================
def _clasificacion(m):
    sr, de = es_sin_ruido(m), es_determinante(m)
    return {(True, True): "Ambos", (True, False): "Sin ruido",
            (False, True): "Determinante", (False, False): "Ninguno"}[(sr, de)]


def _identifica(m, filas, cols):
    """Salidas que identifican la entrada y salidas ambiguas."""
    seguras, ambiguas = [], []
    for j, c in enumerate(cols):
        nz = [filas[i] for i in range(len(m)) if m[i][j] > 1e-9]
        if len(nz) == 1:
            seguras.append((c, nz[0]))
        elif len(nz) > 1:
            ambiguas.append((c, nz))
    return seguras, ambiguas


def _frase_identifica(m, filas, cols):
    seguras, ambiguas = _identifica(m, filas, cols)
    partes = []
    if seguras:
        partes.append("al ver " + _lista([f"{c}" for c, _ in seguras]) +
                      " se sabe con certeza qué entró (" + _lista([f"{c} solo viene de {a}" for c, a in seguras]) + ")")
    if ambiguas:
        partes.append(_lista([c for c, _ in ambiguas]) + (" son ambiguas" if len(ambiguas) > 1 else " es ambigua") +
                      " (pueden venir de más de una entrada)")
    return "En la matriz, " + "; ".join(partes) + "." if partes else ""


def _x_canal_secuencias(res, entrada, salida):
    A, probs, B, m = res
    nombres_canal(A, B)
    ha = _H(probs)
    pri = "   ".join(f"P({a}) = {_f(p)}" for a, p in zip(A, probs))
    frase = ("Las probabilidades a priori son las frecuencias relativas de cada símbolo en la entrada: "
             + ", ".join(f"P({a}) = {_f(p)}" for a, p in zip(A, probs)) + f" (H(A) = {_f(ha)} bits). "
             "La matriz del canal P(b/a) se obtuvo contando, para cada símbolo de entrada, qué fracción "
             "de las veces produjo cada símbolo de salida en la misma posición; cada fila suma 1. "
             + _frase_identifica(m, A, B))
    sumas = [sum(f) for f in m]
    return _bloque(
        "PROBABILIDADES A PRIORI Y MATRIZ DEL CANAL",
        pri + f"   (H(A) = {_f(ha)})\n" + _ver_matriz(m, A, B) +
        "\nsuma de cada fila: " + "  ".join(_f(s) for s in sumas),
        "Fila = símbolo que entró; columna = símbolo que salió. Cada casilla es P(b/a): de las veces "
        "que entró a, qué fracción salió b. Una columna con un solo valor no nulo es una salida que "
        "identifica la entrada; una columna con varios es una salida ambigua.",
        "A priori: frecuencia relativa en la entrada. Matriz: para cada entrada, cantidad de veces que "
        "salió cada símbolo en la misma posición dividido la cantidad de veces que apareció esa entrada.",
        [(True, "cada fila suma 1", "chequeo obligatorio (si una fila no suma 1 hay un error de tipeo)."),
         (_clasificacion(m) == "Ninguno", "alguna columna y alguna fila con más de un valor",
          "canal con ruido y con dispersión (ni sin ruido ni determinante)."),
         (_clasificacion(m) != "Ninguno", "todas las columnas (o todas las filas) con un solo valor",
          "canal sin ruido y/o determinante (ver es_sin_ruido / es_determinante).")],
        frase)


def _x_matriz_canal(res, entrada, salida):
    return _x_canal_secuencias(canal_desde_secuencias(entrada, salida), entrada, salida)


def _x_prob_salida(res, probs, matriz):
    hb = _H(res)
    nb = _nb(len(res))
    ceros = [nb[j] for j, p in enumerate(res) if p <= 1e-12]
    return _bloque(
        "PROBABILIDADES DE SALIDA  P(b)",
        "   ".join(f"P({nb[j]}) = {_f(p)}" for j, p in enumerate(res)) + f"\nH(B) = {_f(hb)} bits",
        "Qué tan seguido aparece cada símbolo a la salida del canal.",
        "P(bj) = suma sobre i de P(ai) * P(bj/ai).",
        [(bool(ceros), "alguna P(b) = 0", f"{_lista(ceros)} nunca aparece."),
         (not ceros, "todas > 0", "todas las salidas pueden aparecer.")],
        "Las probabilidades de salida se obtienen como P(bj) = suma de P(ai) * P(bj/ai): "
        + ", ".join(f"P({nb[j]}) = {_f(p)}" for j, p in enumerate(res)) + f"; la entropía de la salida es H(B) = {_f(hb)} bits.")


def _x_prob_simult(res, probs, matriz):
    return _bloque(
        "PROBABILIDADES DE LOS EVENTOS SIMULTÁNEOS  P(a,b)",
        _ver_matriz(res) + f"\nsuma total: {_f(sum(sum(f) for f in res))}",
        "P(a,b) es la probabilidad de que entre a Y salga b. Toda la matriz suma 1; cada fila suma "
        "P(a) y cada columna P(b).",
        "P(ai, bj) = P(ai) * P(bj/ai).",
        [],
        "Las probabilidades simultáneas se calcularon como P(ai,bj) = P(ai) * P(bj/ai); la matriz suma 1, "
        "sus filas suman las probabilidades a priori y sus columnas las de salida.")


def _x_prob_post(res, probs, matriz):
    s = len(res[0])
    nb = _nb(s)
    ciertas = [nb[j] for j in range(s) if any(abs(res[i][j] - 1) <= _EQ for i in range(len(res)))]
    nulas = [nb[j] for j in range(s)
             if sum(_col(res, j)) > 0.5 and all(abs(res[i][j] - probs[i]) <= _EQ for i in range(len(res)))]
    frase = "Las probabilidades a posteriori P(a/b) se calcularon con Bayes: P(ai/bj) = P(ai,bj)/P(bj); cada columna suma 1."
    if ciertas:
        frase += f" Al recibir {_lista(ciertas)} se sabe con certeza qué entró."
    if nulas:
        frase += f" Recibir {_lista(nulas)} no aporta información (su columna es igual a las a priori)."
    return _bloque(
        "PROBABILIDADES A POSTERIORI  P(a/b)",
        _ver_matriz(res),
        "P(a/b): probabilidad de que haya entrado a sabiendo que salió b. Cada COLUMNA suma 1.",
        "Teorema de Bayes: P(ai/bj) = P(ai) * P(bj/ai) / P(bj).",
        [(bool(ciertas), "columna con un 1", f"{_lista(ciertas)}: identifica la entrada con certeza."),
         (bool(nulas), "columna = a priori", f"{_lista(nulas)}: no aporta información."),
         (not ciertas and not nulas, "columnas repartidas", "cada salida da información parcial.")],
        frase)


def _x_entropias_post(res, probs, matriz):
    ha = _H(probs)
    sal = probabilidades_salida(probs, matriz)
    lineas, ceros, menores, mayores = [], [], [], []
    nb = _nb(len(res))
    for j, (h, pb) in enumerate(zip(res, sal)):
        nombre = nb[j]
        if pb <= 1e-12:
            lineas.append(f"H(A/{nombre}) = {_f(h)}   (esa salida nunca ocurre)")
            continue
        lineas.append(f"H(A/{nombre}) = {_f(h)}")
        if h <= _EQ:
            ceros.append(nombre)
        elif h < ha - _EQ:
            menores.append(nombre)
        elif h > ha + _EQ:
            mayores.append(nombre)
    frase = f"La entropía a priori es H(A) = {_f(ha)} bits. "
    partes = []
    if ceros:
        partes.append(f"al recibir {_lista(ceros)} la incertidumbre se anula (se sabe qué entró)")
    if menores:
        partes.append(f"recibir {_lista(menores)} la reduce")
    if mayores:
        partes.append(f"recibir {_lista(mayores)} la aumenta (puede pasar en una salida puntual, no en promedio)")
    iguales = [nb[j] for j, (h, pb) in enumerate(zip(res, sal)) if pb > 1e-12 and h > _EQ and _igual(h, ha)]
    if iguales:
        partes.append(f"recibir {_lista(iguales)} no la cambia")
    frase += ("A posteriori: " + "; ".join(partes) + ".") if partes else ""
    return _bloque(
        "ENTROPÍAS A POSTERIORI  H(A/bj)",
        f"H(A) = {_f(ha)}\n" + "\n".join(lineas),
        "H(A/bj) es la incertidumbre sobre la entrada que queda después de ver la salida bj. Se "
        "compara con la entropía a priori H(A).",
        "H(A/bj) = suma sobre i de P(ai/bj) * log2(1/P(ai/bj)), con las probabilidades a posteriori.",
        [(bool(ceros), "H(A/bj) = 0", "esa salida identifica la entrada."),
         (bool(menores), "H(A/bj) < H(A)", "esa salida reduce la incertidumbre."),
         (bool(iguales), "H(A/bj) = H(A)", "esa salida no aporta nada."),
         (bool(mayores), "H(A/bj) > H(A)", "esa salida deja más duda que antes (posible solo en salidas puntuales).")],
        frase)


def _x_equivocacion(res, probs, matriz):
    ha = _H(probs)
    x = res
    i = ha - x
    cero = x <= _EQ
    total = (not cero) and _igual(x, ha)
    if cero:
        frase = (f"La equivocación es H(A/B) = {_f(x)}: después de ver la salida no queda ninguna duda "
                 f"sobre la entrada; pasa toda la información (I = H(A) = {_f(ha)} bits).")
    elif total:
        frase = (f"La equivocación es H(A/B) = {_f(x)} = H(A): ver la salida no reduce en nada la "
                 "incertidumbre sobre la entrada; el canal no transmite información.")
    else:
        frase = (f"La equivocación es H(A/B) = {_f(x)} bits: es la incertidumbre que queda sobre la entrada "
                 f"después de observar la salida. Como H(A) = {_f(ha)}, se pierde el {_pct(x / ha)} de la "
                 f"información y pasan I = H(A) - H(A/B) = {_f(i)} bits por símbolo.")
    return _bloque(
        "EQUIVOCACIÓN O RUIDO  H(A/B)",
        f"H(A/B) = {_f(x)} bits   (H(A) = {_f(ha)})",
        "Incertidumbre sobre la ENTRADA que queda después de ver la SALIDA: la información que el "
        "canal no deja pasar. Siempre 0 <= H(A/B) <= H(A).",
        "Por definición: H(A/B) = suma de P(a,b) * log2(1/P(a/b)), con P(a,b) = P(a) * P(b/a) y P(a/b) por Bayes.",
        [(cero, "H(A/B) = 0", "sin ruido para estas probabilidades: la salida dice exactamente qué entró."),
         (not cero and not total, "0 < H(A/B) < H(A)", "se pierde parte de la información; cuanto más cerca de 0, mejor."),
         (total, "H(A/B) = H(A)", "entrada y salida independientes: no pasa información.")],
        frase)


def _x_perdida(res, probs, matriz):
    hb = _H(probabilidades_salida(probs, matriz))
    x = res
    cero = x <= _EQ
    total = (not cero) and _igual(x, hb)
    if cero:
        frase = (f"La pérdida es H(B/A) = {_f(x)}: conociendo la entrada se sabe exactamente qué sale "
                 "(el canal se comporta como determinante).")
    elif total:
        frase = (f"La pérdida es H(B/A) = {_f(x)} = H(B): conocer la entrada no ayuda a predecir la salida; "
                 "entrada y salida son independientes.")
    else:
        frase = (f"La pérdida es H(B/A) = {_f(x)} bits: es la incertidumbre sobre la salida que queda aun "
                 f"conociendo la entrada, el {_pct(x / hb)} de H(B) = {_f(hb)}. Indica cuánto dispersa el "
                 "canal cada símbolo enviado: una misma entrada puede producir salidas distintas.")
    return _bloque(
        "PÉRDIDA  H(B/A)",
        f"H(B/A) = {_f(x)} bits   (H(B) = {_f(hb)})",
        "Incertidumbre sobre la SALIDA que queda aun conociendo la ENTRADA: cuánto 'dispersa' el "
        "canal. Siempre 0 <= H(B/A) <= H(B).",
        "Por definición: H(B/A) = suma de P(a,b) * log2(1/P(b/a)).",
        [(cero, "H(B/A) = 0", "canal determinante: cada entrada da siempre la misma salida."),
         (not cero and not total, "0 < H(B/A) < H(B)", "el canal dispersa; cuanto más alto, más aleatoria la salida."),
         (total, "H(B/A) = H(B)", "la salida no depende de la entrada.")],
        frase)


def _x_entropia_afin(res, probs, matriz):
    ha = _H(probs)
    hb = _H(probabilidades_salida(probs, matriz))
    i = ha + hb - res
    indep = _igual(res, ha + hb)
    det = _igual(res, max(ha, hb))
    frase = (f"La entropía afín es H(A,B) = {_f(res)} bits: la incertidumbre total del par (entrada, salida). "
             f"Cumple H(A,B) = H(A) + H(B) - I(A,B) = {_f(ha)} + {_f(hb)} - {_f(i)}.")
    if indep:
        frase += " Como es igual a H(A) + H(B), entrada y salida son independientes (I = 0)."
    elif det:
        frase += " Como es igual a la mayor de H(A) y H(B), una de las dos determina completamente a la otra."
    return _bloque(
        "ENTROPÍA AFÍN  H(A,B)",
        f"H(A,B) = {_f(res)}   (H(A) = {_f(ha)}, H(B) = {_f(hb)})",
        "Incertidumbre conjunta de entrada y salida: la 'unión' de H(A) y H(B) en el diagrama de Venn. "
        "Siempre max(H(A), H(B)) <= H(A,B) <= H(A) + H(B).",
        "Por definición: H(A,B) = suma de P(a,b) * log2(1/P(a,b)).",
        [(indep, "H(A,B) = H(A) + H(B)", "independientes: el canal no transmite."),
         (det and not indep, "H(A,B) = max(H(A), H(B))", "una determina a la otra."),
         (not indep and not det, "en el medio", "hay dependencia parcial entre entrada y salida.")],
        frase)


def _x_info_mutua(res, probs, matriz):
    ha = _H(probs)
    hb = _H(probabilidades_salida(probs, matriz))
    i = res
    nula = i <= _EQ
    toda_a = (not nula) and _igual(i, ha)
    toda_b = (not nula) and _igual(i, hb)
    if nula:
        frase = (f"La información mutua es I(A,B) = {_f(i)}: entrada y salida son independientes, el canal "
                 "no transmite información.")
    elif toda_a:
        frase = (f"La información mutua es I(A,B) = {_f(i)} = H(A): pasa toda la información de la entrada "
                 "(la salida identifica siempre lo que entró).")
    else:
        frase = (f"La información mutua es I(A,B) = {_f(i)} bits: es la información sobre la entrada que "
                 f"atraviesa el canal. De los {_f(ha)} bits de la entrada pasa el {_pct(i / ha)}; el resto "
                 f"(H(A/B) = {_f(ha - i)}) se pierde.")
        if toda_b:
            frase += " Además I = H(B): la salida depende solo de la entrada (canal determinante)."
    return _bloque(
        "INFORMACIÓN MUTUA  I(A,B)",
        f"I(A,B) = {_f(i)} bits   (H(A) = {_f(ha)}, H(B) = {_f(hb)})",
        "Información sobre la entrada que se obtiene al observar la salida: lo que realmente atraviesa "
        "el canal. Es recíproca (I(A,B) = I(B,A)), nunca negativa, y su máximo sobre todas las "
        "probabilidades de entrada es la capacidad.",
        "Por definición: I(A,B) = suma de P(a,b) * log2(P(a,b) / (P(a) * P(b))). "
        "Se verifica I = H(A) - H(A/B) = H(B) - H(B/A).",
        [(nula, "I = 0", "independientes: no pasa nada."),
         (not nula and not toda_a, "0 < I < H(A)", "pasa una parte de la información."),
         (toda_a, "I = H(A)", "canal sin ruido para estas probabilidades: pasa todo."),
         (toda_b, "I = H(B)", "canal determinante (H(B/A) = 0).")],
        frase)


def _x_analisis(res, probs, matriz):
    r = res
    ha, i = r["H(A)"], r["I(A,B)"]
    pct = _pct(i / ha) if ha > _EQ else "0%"
    return _bloque(
        "TODAS LAS ENTROPÍAS DEL CANAL",
        "\n".join(f"{k:8s} = {_f(v)}" for k, v in r.items() if k != "verifica_relaciones") +
        f"\nrelaciones verificadas: {r['verifica_relaciones']}",
        "H(A): entrada. H(B): salida. H(A/B): equivocación. H(B/A): pérdida. H(A,B): afín. I: lo que "
        "pasa. Relaciones: I = H(A) - H(A/B) = H(B) - H(B/A); H(A,B) = H(A) + H(B) - I.",
        "Cada una por su definición a partir de P(a,b), P(a/b) y P(b/a).",
        [(r["verifica_relaciones"], "relaciones = True", "las cuentas son coherentes."),
         (not r["verifica_relaciones"], "relaciones = False", "hay un error en los datos.")],
        f"H(A) = {_f(ha)}, H(B) = {_f(r['H(B)'])}, H(A/B) = {_f(r['H(A/B)'])}, H(B/A) = {_f(r['H(B/A)'])}, "
        f"H(A,B) = {_f(r['H(A,B)'])} e I(A,B) = I(B,A) = {_f(i)} bits: pasa el {pct} de la información de "
        "la entrada y se verifican I = H(A) - H(A/B) = H(B) - H(B/A) y H(A,B) = H(A) + H(B) - I.")


def _x_sin_ruido(res, matriz):
    if res:
        frase = ("El canal es sin ruido: cada columna de la matriz tiene un único valor no nulo, así que "
                 "cada salida proviene de una sola entrada y viendo la salida se sabe qué entró "
                 "(H(A/B) = 0).")
    else:
        j = next(j for j in range(len(matriz[0])) if sum(1 for p in _col(matriz, j) if p > 1e-9) != 1)
        na, nb = _na(len(matriz)), _nb(len(matriz[0]))
        nz = [na[i] for i in range(len(matriz)) if matriz[i][j] > 1e-9]
        frase = (f"No es sin ruido: la salida {nb[j]} " +
                 (f"puede provenir de {_lista(nz)}" if nz else "no aparece nunca") +
                 ", así que viendo la salida no siempre se sabe qué entró.")
    return _bloque(
        "¿CANAL SIN RUIDO?", str(res),
        "Sin ruido = cada COLUMNA tiene un solo valor distinto de 0: cada salida viene de una única entrada.",
        "Se revisó cada columna de la matriz contando sus valores no nulos.",
        [(res, "True", "H(A/B) = 0, I = H(A), C = log2(cantidad de entradas)."),
         (not res, "False", "alguna salida puede venir de más de una entrada.")],
        frase)


def _x_determinante(res, matriz):
    if res:
        frase = ("El canal es determinante: cada fila tiene un único valor no nulo (un 1), así que cada "
                 "entrada produce siempre la misma salida (H(B/A) = 0).")
    else:
        i = next(i for i in range(len(matriz)) if sum(1 for p in matriz[i] if p > 1e-9) != 1)
        na, nb = _na(len(matriz)), _nb(len(matriz[0]))
        nz = [nb[j] for j in range(len(matriz[0])) if matriz[i][j] > 1e-9]
        frase = f"No es determinante: la entrada {na[i]} puede producir {_lista(nz)}."
    return _bloque(
        "¿CANAL DETERMINANTE?", str(res),
        "Determinante = cada FILA tiene un solo valor distinto de 0 (un 1): cada entrada da siempre la misma salida.",
        "Se revisó cada fila de la matriz contando sus valores no nulos.",
        [(res, "True", "H(B/A) = 0, I = H(B), C = log2(cantidad de salidas)."),
         (not res, "False", "alguna entrada puede dar salidas distintas.")],
        frase)


def _x_serie(res, matriz1, matriz2):
    return _bloque(
        "CANALES EN SERIE", _ver_matriz(res),
        "La salida del primer canal es la entrada del segundo. La matriz compuesta es el producto de "
        "las dos matrices. Siempre I(A,C) <= I(A,B): procesar no agrega información.",
        "Producto de matrices: P(c/a) = suma sobre b de P(b/a) * P(c/b).",
        [],
        "La matriz del canal compuesto es el producto de las matrices de los dos canales. Su información "
        "mutua no puede superar a la del primer canal: pasar la señal por otro canal (procesarla) no "
        "agrega información, a lo sumo la conserva.",
        "Para comparar, calculá informacion_mutua del primer canal y del compuesto con las mismas P(a).")


def _x_red_suf(res, matriz, j, k):
    cj, ck = _col(matriz, j), _col(matriz, k)
    return _bloque(
        f"¿REDUCCIÓN SUFICIENTE COLUMNAS {j} y {k}? (índices desde 0)",
        f"columna {j}: {[_f(x) for x in cj]}\ncolumna {k}: {[_f(x) for x in ck]}\n-> {res}",
        "Dos salidas se pueden combinar sin perder información si sus columnas son proporcionales: "
        "dicen exactamente lo mismo sobre la entrada.",
        "Se verificó si una columna es múltiplo constante de la otra.",
        [(res, "True", "combinarlas no cambia I(A,B) para ninguna distribución de entrada."),
         (not res, "False", "combinarlas perdería información.")],
        (f"Las columnas {j} y {k} son proporcionales, por eso se pueden combinar en una reducción "
         "suficiente sin perder información." if res else
         f"Las columnas {j} y {k} no son proporcionales: combinarlas haría perder información."))


def _x_det_reduccion(res, matriz, j, k):
    return _bloque(
        "CANAL DETERMINANTE DE LA REDUCCIÓN", _ver_matriz(res),
        "Canal determinante que, puesto en serie, junta las salidas j y k en una sola.",
        "Matriz de s filas y s-1 columnas con un único 1 por fila.",
        [],
        f"La reducción se hace poniendo en serie un canal determinante que envía las salidas {j} y {k} a la misma salida.")


def _grupos_reduccion(matriz):
    actual = [list(f) for f in matriz]
    grupos = [[j] for j in range(len(matriz[0]))]
    cambio = True
    while cambio and len(actual[0]) > 1:
        cambio = False
        s = len(actual[0])
        for j in range(s):
            for k in range(j + 1, s):
                if es_reduccion_suficiente(actual, j, k):
                    actual = canal_serie(actual, matriz_determinante_reduccion(actual, j, k))
                    grupos[j] += grupos[k]
                    del grupos[k]
                    cambio = True
                    break
            if cambio:
                break
    return grupos, actual


def _texto_grupos(grupos, cols):
    partes = []
    for g in grupos:
        n = [str(cols[j]) for j in sorted(g)]
        partes.append(f"{n[0]} con {n[1]}" if len(n) == 2 else _lista(n))
    return _lista(partes)


def _x_reducir(res, matriz, pasos=False, cols=None):
    grupos, final = _grupos_reduccion(matriz)
    cols = cols or _nb(len(matriz[0]))
    nombres = ["".join(cols[j] for j in sorted(g)) if all(len(str(cols[x])) == 1 for x in g)
               else "+".join(str(cols[j]) for j in sorted(g)) for g in grupos]
    combinados = [g for g in grupos if len(g) > 1]
    hubo = bool(combinados)
    det = es_determinante(final)
    txt = _ver_matriz(final, _na(len(final)), nombres)
    if hubo:
        frase = ("Se combinaron " + _texto_grupos(combinados, cols) +
                 " porque sus columnas son proporcionales (dicen lo mismo sobre la entrada). El canal reducido "
                 f"tiene {len(final[0])} salidas ({', '.join(nombres)}) y conserva la misma información mutua "
                 "que el original, para cualquier distribución de entrada: por eso son reducciones suficientes. ")
        frase += ("El canal reducido es determinante." if det else "El canal reducido no es determinante.")
    else:
        frase = ("El canal no admite reducciones suficientes: no hay dos columnas proporcionales, así que "
                 "cualquier combinación de salidas perdería información.")
    return _bloque(
        "REDUCCIONES SUFICIENTES",
        txt + f"\n({len(matriz[0])} salidas -> {len(final[0])} salidas; determinante: {det})",
        "Reducir = juntar salidas. Es SUFICIENTE si no se pierde información, y eso pasa cuando las "
        "columnas son proporcionales. La I(A,B) del canal reducido es la misma que la del original.",
        "Mientras hubo dos columnas proporcionales, se combinaron poniendo en serie un canal "
        "determinante (producto de matrices).",
        [(not hubo, "no cambia", "no hay columnas proporcionales."),
         (hubo and det, "reducido determinante", "cada entrada lleva a una sola salida del canal reducido."),
         (hubo and not det, "reducido no determinante", "se simplificó pero sigue habiendo dispersión.")],
        frase,
        "Verificá con informacion_mutua(probs, reducido) que da igual que con el original.")


def _x_uniforme(res, matriz):
    return _bloque(
        "¿CANAL UNIFORME?", str(res),
        "Uniforme = todas las filas tienen los mismos valores (en otro orden) y todas las columnas "
        "también. El canal binario simétrico (BSC) es el ejemplo típico.",
        "Se comparó cada fila y cada columna con la primera (mismos valores, en cualquier orden).",
        [(res, "True", "C = log2(salidas) - H(fila), con entradas equiprobables."),
         (not res, "False", "no vale esa fórmula; para 2 entradas usar capacidad_binaria.")],
        ("El canal es uniforme: todas las filas y columnas son permutaciones entre sí, así que trata igual a "
         "todas las entradas y la capacidad se alcanza con entradas equiprobables." if res else
         "El canal no es uniforme: las filas (o las columnas) no tienen los mismos valores."))


def _x_capacidad(res, matriz):
    c, tipo = res
    casos = [(tipo == "determinante", "determinante", "C = log2(cantidad de salidas usadas)."),
             (tipo == "sin ruido", "sin ruido", "C = log2(cantidad de entradas): no pierde nada."),
             (tipo == "uniforme", "uniforme", "C = log2(salidas) - H(fila), con entradas equiprobables."),
             (c is None, "sin fórmula directa", "para 2 entradas usar capacidad_binaria(matriz, 0.0001).")]
    if c is None:
        frase = "Este canal no tiene fórmula directa de capacidad; se estima con capacidad_binaria."
    else:
        frase = (f"La capacidad es C = {_f(c)} bits por símbolo (canal {tipo}): es la máxima información "
                 "mutua que puede transmitir el canal, eligiendo la mejor distribución de entrada.")
        if c <= _EQ:
            frase += " C = 0: el canal no transmite información."
    return _bloque("CAPACIDAD DEL CANAL", f"C = {_f(c) if c is not None else 'None'}   ({tipo})",
                   "Máxima información mutua posible, probando todas las distribuciones de entrada.",
                   "Fórmula directa según el tipo de canal.", casos, frase)


def _x_capacidad_binaria(res, matriz, paso):
    c, p = res
    a1, a2 = _na(2)
    cerca = abs(p - 0.5) <= 0.02 + 1e-9
    casos = [(c <= _EQ, "C = 0", "el canal no transmite información con ninguna distribución."),
             (c > _EQ and cerca, f"P({a1}) cerca de 0,5", "le convienen entradas casi equiprobables."),
             (c > _EQ and not cerca and p > 0.5, f"P({a1}) > 0,5", f"conviene enviar más {a1} que {a2}."),
             (c > _EQ and not cerca and p < 0.5, f"P({a1}) < 0,5", f"conviene enviar más {a2} que {a1}.")]
    frase = (f"La capacidad del canal es C = {_f(c)} bits por símbolo: es la máxima información mutua posible. "
             f"Se alcanza con P({a1}) = {_f(p)} y P({a2}) = {_f(1 - p)}, que son las probabilidades que maximizan "
             "I(A,B) (no las a priori del ejercicio). ")
    frase += (f"Como un canal binario puede transmitir como máximo 1 bit, este aprovecha el {_pct(c)} de ese máximo."
              if c > _EQ else "C = 0: entrada y salida son independientes para cualquier distribución.")
    return _bloque(
        "CAPACIDAD DE UN CANAL BINARIO (estimada)",
        f"C = {_f(c)} bits   con P({a1}) = {_f(p)}   P({a2}) = {_f(1 - p)}   (paso {paso})",
        "C = máximo de I(A,B) sobre todas las distribuciones de entrada. Las P(a1), P(a2) que se "
        "informan son las que LOGRAN ese máximo. Siempre I(A,B) <= C.",
        f"Se calculó la información mutua para P({a1}) desde 0 hasta 1 con paso {paso} (P({a2}) = 1 - P({a1})) "
        "y se tomó el valor máximo.",
        casos, frase,
        "En 2025 se marcó mal informar P = 0,5/0,5: las probabilidades son las que da esta función. "
        "Comparala con la I(A,B) del ejercicio: I <= C.")


def _x_prob_error(res, probs, matriz, a_posteriori=False):
    conj = probabilidades_simultaneas(probs, matriz)
    s = len(matriz[0])
    reglas = []
    na, nb = _na(len(matriz)), _nb(s)
    for j in range(s):
        crit = _col(conj, j) if a_posteriori else _col(matriz, j)
        reglas.append(f"{nb[j]}->{na[crit.index(max(crit))]}")
    otra = probabilidad_error(probs, matriz, not a_posteriori)
    adivinar = 1 - max(probs)
    pe = res
    nombre = "máxima probabilidad a posteriori" if a_posteriori else "máxima posibilidad"
    criterio = "con mayor P(a)*P(b/a)" if a_posteriori else "con mayor P(b/a) (la mayor de la columna)"
    casos = [(pe <= _EQ, "P_E = 0", "el receptor nunca se equivoca."),
             (pe > _EQ and pe <= adivinar + _EQ, f"0 < P_E <= {_f(adivinar)}",
              "mejor que adivinar siempre la entrada más probable sin mirar la salida."),
             (pe > adivinar + _EQ, f"P_E > {_f(adivinar)}",
              "peor que adivinar sin mirar la salida: pasa con la regla de máxima posibilidad cuando "
              "las entradas no son equiprobables; revisá los datos y compará con la otra regla.")]
    frase = (f"Con la regla de {nombre}, ante cada salida se decide la entrada {criterio}: "
             f"{', '.join(reglas)}. Así el receptor se equivoca con probabilidad P_E = {_f(pe)}, "
             f"es decir en el {_pct(pe)} de los símbolos.")
    if _igual(pe, otra):
        frase += " La otra regla de decisión da el mismo resultado."
    return _bloque(
        "PROBABILIDAD DE ERROR  P_E",
        f"P_E = {_f(pe)}   (regla: {nombre}; con la otra regla: {_f(otra)})\n"
        f"decisiones: {'  '.join(reglas)}\nerror de adivinar siempre la entrada más probable: {_f(adivinar)}",
        "Probabilidad de que el receptor decida mal qué entró, usando una regla de decisión fija. "
        "Depende de la matriz Y de las probabilidades de entrada.",
        f"Para cada salida se eligió la entrada {criterio}; P_E = 1 - suma de P(a*, b) de las decisiones.",
        casos, frase,
        "La guía usa máxima posibilidad (por defecto). Con entradas equiprobables las dos reglas dan igual.")


# ===========================================================================
# Dispatcher
# ===========================================================================
_EXPLICADORES = {
    "CalcEntropia": _x_entropia,
    "alfabeto_y_probabilidades": _x_alfabeto,
    "GeneraAlfabetoYProb": _x_alfabeto,
    "huffman": _x_huffman,
    "shannon_fano": _x_shannon_fano,
    "extension_fuente": _x_extension_fuente,
    "extension_codigo": _x_extension_codigo,
    "detalle_primer_teorema": _x_detalle_teorema,
    "cumple_primer_teorema": _x_cumple_teorema,
    "rendimiento_redundancia": _x_rendimiento,
    "resumen_codigo": _x_resumen,
    "tasa_compresion": _x_tasa,
    "tasa_compresion_codigo": _x_tasa_codigo,
    "codificar_mensaje": _x_codificar,
    "decodificar_mensaje": _x_decodificar,
    "decodificar_cadena": _x_decodificar_cadena,
    "rlc_texto": _x_rlc_texto,
    "rlc_comprimir": _x_rlc_comprimir,
    "rlc_descomprimir": _x_rlc_descomprimir,
    "distancia_hamming": _x_dist_hamming,
    "analizar_codigo_hamming": _x_hamming_codigo,
    "distancia_levenshtein": _x_levenshtein,
    "byte_con_paridad": _x_byte_paridad,
    "verificar_byte": _x_verificar_byte,
    "filas_de_bits": _x_filas_bits,
    "analizar_matriz_paridad": _x_matriz_paridad,
    "generar_mensaje_con_paridad": _x_generar_paridad,
    "recuperar_mensaje": _x_recuperar,
    "canal_desde_secuencias": _x_canal_secuencias,
    "matriz_canal": _x_matriz_canal,
    "probabilidades_salida": _x_prob_salida,
    "probabilidades_simultaneas": _x_prob_simult,
    "probabilidades_a_posteriori": _x_prob_post,
    "entropias_a_posteriori": _x_entropias_post,
    "equivocacion": _x_equivocacion,
    "perdida": _x_perdida,
    "entropia_afin": _x_entropia_afin,
    "informacion_mutua": _x_info_mutua,
    "analisis_canal": _x_analisis,
    "es_sin_ruido": _x_sin_ruido,
    "es_determinante": _x_determinante,
    "canal_serie": _x_serie,
    "es_reduccion_suficiente": _x_red_suf,
    "matriz_determinante_reduccion": _x_det_reduccion,
    "reducir_canal": _x_reducir,
    "es_uniforme": _x_uniforme,
    "capacidad_canal": _x_capacidad,
    "capacidad_binaria": _x_capacidad_binaria,
    "probabilidad_error": _x_prob_error,
}


def texto_explicacion(funcion, *args, **kwargs):
    """Como explicar, pero devuelve (resultado, texto) sin imprimir."""
    nombre = funcion if isinstance(funcion, str) else getattr(funcion, "__name__", str(funcion))
    if isinstance(funcion, str):
        funcion = globals()[funcion]
    res = funcion(*args, **kwargs)
    explicador = _EXPLICADORES.get(nombre)
    if explicador is None:
        return res, f"(No tengo explicación para '{nombre}'. Usá ayuda() para ver la lista.)"
    if nombre == "reducir_canal" and kwargs.get("pasos", args[1] if len(args) > 1 else False):
        return res, explicador(res[-1], *args, **kwargs)
    return res, explicador(res, *args, **kwargs)


def explicar(funcion, *args, **kwargs):
    """
    Corre funcion(*args, **kwargs), imprime qué significa el resultado, cómo
    se obtuvo, cómo leerlo según el valor (marcando tu caso) y una frase para
    el parcial. Devuelve el mismo resultado que la función.

    Ejemplos:
        explicar(equivocacion, probs, matriz)
        explicar(analizar_codigo_hamming, ["0000", "0011", "1010", "0101"])
        explicar(analizar_matriz_paridad, filas_de_bits(ENTRADA))
    """
    res, texto = texto_explicacion(funcion, *args, **kwargs)
    _imprimir(texto)
    return res


def ayuda():
    """Lista las funciones que se pueden pasar a explicar()."""
    _imprimir("Funciones que se pueden explicar con explicar(funcion, argumentos...):\n  " +
              "\n  ".join(sorted(_EXPLICADORES)) +
              "\n\nAparte: explicar_extension(probs, n)"
              "\n\nPor ejercicio completo: explicacion_ej1, conclusiones_ej1, explicacion_ej2, conclusiones_ej2")


def explicar_extension(probs, n):
    """
    Explica el código ÓPTIMO (Huffman) de la extensión de orden n, con las
    unidades bien puestas (L_n es por bloque; L_n/n por símbolo), y lo compara
    con el código de la fuente. Devuelve un dict con L, η y R de la extensión.

    Uso:  explicar_extension(probs, 3)      # probs = las de la fuente ORIGINAL
    """
    pe = extension_fuente(probs, n)
    cod = huffman(pe)
    h = _H(probs)
    ln = _L(pe, cod)
    lnn = ln / n
    eta = n * h / ln
    red = 1 - eta
    l1 = _L(probs, huffman(probs)) if len(probs) > 1 else 1.0
    eta1 = h / l1
    mejora = lnn < l1 - _EQ
    frase = (f"Para la extensión de orden {n} se aplicó Huffman a los {len(pe)} bloques de {n} símbolos: "
             f"L_{n} = {_f(ln)} binits por bloque, es decir L_{n}/{n} = {_f(lnn)} binits por símbolo "
             f"(H = {_f(h)}). El rendimiento es η = {n}*H/L_{n} = {_f(eta)} y la redundancia R = {_f(red)}. ")
    if mejora:
        frase += (f"Comparado con el código de la fuente (L = {_f(l1)}, η = {_f(eta1)}), codificar bloques reparte "
                  "el redondeo de las longitudes entre varios símbolos y acerca la longitud por símbolo a la entropía.")
    else:
        frase += (f"No mejora al código de la fuente (L = {_f(l1)}), que ya era tan bueno como permiten estas "
                  "probabilidades.")
    _imprimir(_bloque(
        f"CÓDIGO ÓPTIMO DE LA EXTENSIÓN DE ORDEN {n}",
        f"L_{n} = {_f(ln)} binits/bloque   L_{n}/{n} = {_f(lnn)} binits/símbolo   "
        f"η = {_f(eta)}   R = {_f(red)}\n(fuente: L = {_f(l1)}, η = {_f(eta1)};  H = {_f(h)})",
        "Se codifican bloques de n símbolos en vez de símbolos sueltos. L_n se mide por BLOQUE; "
        "para comparar con la fuente se divide por n. η = H(S^n)/L_n = n*H(S)/L_n.",
        f"Se calcularon las {len(pe)} probabilidades de la extensión (productos, fuente de memoria nula), "
        "se aplicó Huffman sobre ellas y se calcularon L_n, η = n*H/L_n y R = 1 - η.",
        _casos_eta(eta) + [(mejora, "L_n/n < L de la fuente", "la extensión mejora la compresión."),
                           (not mejora, "L_n/n = L de la fuente", "la extensión no mejora nada.")],
        frase,
        "En el parcial, la 'L de la extensión' es L_n (por bloque). Chequeo: η = n*H/L_n tiene que "
        "dar el η que informás (en 2025 se marcó que L, η y R se contradecían)."))
    return {"L": ln, "L_sobre_n": lnn, "rendimiento": eta, "redundancia": red, "codigo": cod}


# ===========================================================================
# Ejercicios completos del parcial: "explicar" y "concluir"
# ===========================================================================
def _datos_ej1(mensaje, n):
    alf, probs = alfabeto_y_probabilidades(mensaje)
    cod = huffman(probs)
    r1 = resumen_codigo(probs, cod)
    pe = extension_fuente(probs, n)
    codn = huffman(pe)
    rn = resumen_codigo(pe, codn)
    d1 = detalle_primer_teorema(probs, cod, 1)
    dn = detalle_primer_teorema(probs, codn, n)
    tasa = tasa_compresion_codigo(mensaje, alf, cod)
    return alf, probs, cod, r1, pe, codn, rn, d1, dn, tasa


def explicacion_ej1(mensaje, n):
    """Texto para 'Explicar brevemente cómo se obtuvieron los resultados' (ejercicio tipo 1)."""
    alf, probs, cod, r1, pe, codn, rn, d1, dn, tasa = _datos_ej1(mensaje, n)
    q = len(alf)
    t = ("Las probabilidades se estimaron como la frecuencia relativa de cada símbolo en el mensaje "
         f"({len(mensaje)} símbolos), considerando una fuente de memoria nula, y la entropía como "
         "H(S) = suma de P(si) * log2(1/P(si)). "
         "El código binario óptimo se generó con el algoritmo de Huffman: se unen sucesivamente los "
         "dos símbolos o grupos menos probables, sumando sus probabilidades, y se asigna 0 y 1 a cada "
         "rama; la palabra de cada símbolo es el camino desde la raíz hasta él. "
         "La tasa de compresión es el tamaño del mensaje original (8 bits ASCII por carácter) dividido "
         "el tamaño del mensaje codificado (suma de las longitudes de las palabras de sus símbolos), sin "
         "agregar redundancia. "
         f"Para la extensión de orden {n} se calcularon las {q}^{n} = {q ** n} probabilidades de los bloques "
         f"como producto de las probabilidades de sus símbolos y se aplicó Huffman sobre ellas. "
         f"Para cada código: L = suma de P * longitud, η = H/L (para la extensión, H(S^{n}) = {n} * H(S)) "
         "y R = 1 - η. "
         f"El Primer Teorema se verificó comprobando H(S) <= L_n/n < H(S) + 1/n, con n = 1 para la fuente "
         f"y n = {n} para la extensión.")
    _imprimir("\n".join(["EXPLICACIÓN (ejercicio 1)", "-" * _ANCHO] + _envolver(t, "")))
    return t


def conclusiones_ej1(mensaje, n):
    """Texto para 'Analizar los resultados y realizar conclusiones' (ejercicio tipo 1)."""
    alf, probs, cod, r1, pe, codn, rn, d1, dn, tasa = _datos_ej1(mensaje, n)
    h, l1, e1, red1 = r1["H"], r1["L"], r1["rendimiento"], r1["redundancia"]
    ln, en = rn["L"], rn["rendimiento"]
    lnn = ln / n
    q = len(alf)
    items = []
    items.append(f"Shannon y la longitud media: la entropía H(S) = {_f(h)} bits/símbolo es el límite inferior "
                 f"de la longitud media de cualquier código unívoco; ninguno de los dos códigos baja de ese "
                 f"valor (L = {_f(l1)} y L_{n}/{n} = {_f(lnn)}).")
    if _igual(e1, 1):
        items.append("Códigos compactos: el código de Huffman de la fuente ya alcanza la entropía (η = 1) "
                     "porque las probabilidades son potencias de 1/2; no hay redundancia que eliminar.")
    else:
        items.append(f"Códigos compactos: Huffman da la menor L posible codificando símbolo a símbolo, por eso "
                     f"{'ambos cumplen' if d1['cumple'] and dn['cumple'] else 'debería cumplir'} el Primer "
                     f"Teorema. Aun así L = {_f(l1)} > H porque las longitudes son enteras y las "
                     f"probabilidades no son potencias de 1/2: se desperdicia un {_pct(red1)} (R).")
    if lnn < l1 - _EQ:
        items.append(f"Extensiones: al codificar bloques de {n} símbolos, el redondeo a enteros se reparte entre "
                     f"{n} símbolos: L_{n}/{n} = {_f(lnn)} queda a {_f(lnn - h)} de H y el rendimiento pasa de "
                     f"{_pct(e1)} a {_pct(en)}. Es lo que predice el Primer Teorema: la cota superior H + 1/n "
                     f"se achica (de {_f(h + 1)} a {_f(h + 1 / n)}) y L_n/n tiende a H cuando n crece.")
    else:
        items.append(f"Extensiones: codificar bloques de {n} símbolos no mejora la longitud por símbolo "
                     f"(L_{n}/{n} = {_f(lnn)} = L), porque el código de la fuente ya era tan bueno como permite "
                     "el teorema para estas probabilidades.")
    items.append(f"Costo de la extensión: la tabla pasa de {q} a {q ** n} palabras y hay que esperar {n} símbolos "
                 "para codificar; se gana rendimiento a cambio de complejidad.")
    items.append(f"Compresión: la tasa es {_f(tasa)} : 1, el mensaje codificado ocupa el {_pct(1 / tasa)} de "
                 "lo que ocupa en ASCII.")
    items.append(f"Primer Teorema: la fuente {'cumple' if d1['cumple'] else 'NO cumple'} "
                 f"({_f(h)} <= {_f(l1)} < {_f(h + 1)}) y la extensión {'cumple' if dn['cumple'] else 'NO cumple'} "
                 f"({_f(h)} <= {_f(lnn)} < {_f(h + 1 / n)}).")
    lineas = ["CONCLUSIONES (ejercicio 1)", "-" * _ANCHO]
    for it in items:
        lineas += _envolver("- " + it, "", "  ")
    _imprimir("\n".join(lineas))
    return "\n".join("- " + it for it in items)


def _datos_ej2(entrada, salida):
    A, probs, B, m = canal_desde_secuencias(entrada, salida)
    d = {"A": A, "B": B, "probs": probs, "m": m,
         "clase": _clasificacion(m), "HA": _H(probs),
         "HAB": equivocacion(probs, m), "HBA": perdida(probs, m), "I": informacion_mutua(probs, m),
         "post": entropias_a_posteriori(probs, m), "pb": probabilidades_salida(probs, m)}
    grupos, red = _grupos_reduccion(m)
    d["grupos"], d["red"] = grupos, red
    if len(A) == 2:
        d["C"], d["pC"] = capacidad_binaria(red, 0.0001)
    else:
        c, _ = capacidad_canal(red)
        d["C"], d["pC"] = c, None
    d["PE"] = probabilidad_error(probs, m)
    d["PE_post"] = probabilidad_error(probs, m, True)
    d["par"] = None
    if set(entrada) <= {"0", "1"} and len(entrada) % 8 == 0 and len(entrada) >= 16:
        d["par"] = analizar_matriz_paridad(filas_de_bits(entrada))
    return d


def explicacion_ej2(entrada, salida):
    """Texto para 'Explicar brevemente cómo se obtuvieron los resultados' (ejercicio tipo 2)."""
    d = _datos_ej2(entrada, salida)
    t = ("Las probabilidades a priori son las frecuencias relativas de cada símbolo en la secuencia de "
         "entrada. La matriz del canal P(b/a) se obtuvo contando, para cada símbolo de entrada, qué "
         "fracción de las veces produjo cada símbolo de salida en la misma posición; cada fila suma 1. "
         "Para clasificar el canal se verificó si cada columna tiene un único valor no nulo (sin ruido) "
         "y si cada fila tiene un único valor no nulo (determinante). "
         "Con P(a,b) = P(a) * P(b/a), P(b) = suma de P(a,b) y P(a/b) = P(a,b)/P(b) se calcularon por "
         "definición la equivocación H(A/B) = suma de P(a,b) * log2(1/P(a/b)), la pérdida "
         "H(B/A) = suma de P(a,b) * log2(1/P(b/a)) y la información mutua "
         "I(A,B) = suma de P(a,b) * log2(P(a,b)/(P(a)P(b))). "
         "Las reducciones suficientes se hicieron combinando columnas proporcionales, poniendo en serie "
         "un canal determinante. ")
    if d["pC"] is not None:
        t += ("La capacidad se obtuvo calculando la información mutua del canal reducido para P(a1) entre "
              "0 y 1 con paso 0,0001 y tomando el máximo; las probabilidades informadas son las que lo "
              "alcanzan. ")
    t += ("La probabilidad de error se calculó con la regla de máxima posibilidad: para cada salida se "
          "decide la entrada con mayor P(b/a) y P_E = 1 - suma de P(a*, b). ")
    if d["par"] is not None:
        t += (f"Para el mensaje, los {len(entrada)} bits se ordenaron en {len(entrada) // 8} filas de 8 (la "
              "primera es la paridad longitudinal y las demás son caracteres ASCII de 7 bits más su paridad "
              "vertical), se verificó la paridad par de cada fila y columna, se corrigió el bit ubicado en "
              "el cruce de la fila y la columna con error y se decodificó cada carácter.")
    _imprimir("\n".join(["EXPLICACIÓN (ejercicio 2)", "-" * _ANCHO] + _envolver(t, "")))
    return t


def conclusiones_ej2(entrada, salida):
    """Texto para 'Analizar los resultados y realizar conclusiones' (ejercicio tipo 2)."""
    d = _datos_ej2(entrada, salida)
    A, B, m = d["A"], d["B"], d["m"]
    ha, hab, i = d["HA"], d["HAB"], d["I"]
    items = []
    if ha <= _EQ:
        items.append("La entrada tiene un solo símbolo: no hay información que transmitir (H(A) = 0).")
    elif i <= _EQ:
        items.append(f"El canal no transmite información: I(A,B) = 0, la salida es independiente de la entrada.")
    elif _igual(i, ha):
        items.append(f"El canal transmite toda la información de la entrada: I(A,B) = H(A) = {_f(ha)} bits "
                     "y la equivocación es 0.")
    else:
        calif = "muy ruidoso" if i / ha < 0.5 else "con ruido"
        items.append(f"El canal es {calif}: de los {_f(ha)} bits que tiene cada símbolo de entrada solo atraviesan "
                     f"I(A,B) = {_f(i)} ({_pct(i / ha)}); la equivocación H(A/B) = {_f(hab)} es la información "
                     "que se pierde.")
    seguras, ambiguas = _identifica(m, A, B)
    partes = []
    for j, b in enumerate(B):
        if d["pb"][j] > 1e-12:
            partes.append(f"H(A/{b}) = {_f(d['post'][j])}")
    if seguras or ambiguas:
        txt = ""
        if seguras:
            txt += (f"Las salidas {_lista([c for c, _ in seguras])} identifican la entrada con certeza "
                    "(su entropía a posteriori es 0)")
        if ambiguas:
            txt += ("; " if txt else "") + (f"{_lista([c for c, _ in ambiguas])} "
                                            f"{'son ambiguas' if len(ambiguas) > 1 else 'es ambigua'}")
        items.append(txt + " (" + ", ".join(partes) + ").")
    items.append({"Ninguno": "No es sin ruido (hay salidas que pueden venir de las dos entradas) ni determinante "
                             "(cada entrada puede producir varias salidas).",
                  "Sin ruido": "Es un canal sin ruido: cada salida viene de una sola entrada.",
                  "Determinante": "Es un canal determinante: cada entrada produce siempre la misma salida.",
                  "Ambos": "Es sin ruido y determinante: la salida es la entrada renombrada."}[d["clase"]])
    comb = [g for g in d["grupos"] if len(g) > 1]
    if comb:
        items.append("Las reducciones suficientes (se combinaron " + _texto_grupos(comb, B) +
                     f") dejan un canal de {len(d['red'][0])} salidas que transmite exactamente lo mismo "
                     f"(I = {_f(informacion_mutua(d['probs'], d['red']))}): simplifican el canal sin perder información"
                     + ("; el reducido es determinante." if es_determinante(d["red"]) else "."))
    else:
        items.append("No hay reducciones suficientes: todas las salidas aportan información distinta.")
    if d["C"] is not None:
        if d["pC"] is not None:
            items.append(f"La capacidad es C = {_f(d['C'])} bits y se alcanza con P({A[0]}) = {_f(d['pC'])} y "
                         f"P({A[1]}) = {_f(1 - d['pC'])}; con las probabilidades actuales el canal transmite "
                         f"{_f(i)}, el {_pct(i / d['C']) if d['C'] > _EQ else '0%'} de su capacidad.")
        else:
            items.append(f"La capacidad es C = {_f(d['C'])} bits.")
        if ha > d["C"] + _EQ:
            items.append(f"Como H(A) = {_f(ha)} > C = {_f(d['C'])}, por el Segundo Teorema de Shannon no se puede "
                         "transmitir esta fuente a razón de un símbolo por uso del canal con error arbitrariamente "
                         "chico: habría que agregar redundancia (codificar) para bajar la tasa por debajo de C.")
        else:
            items.append(f"Como H(A) = {_f(ha)} <= C = {_f(d['C'])}, por el Segundo Teorema de Shannon existe una "
                         "codificación que permite transmitir esta fuente con error tan chico como se quiera.")
    items.append(f"Sin codificar, el receptor se equivoca en el {_pct(d['PE'])} de los símbolos (P_E = {_f(d['PE'])}, "
                 "regla de máxima posibilidad).")
    par = d["par"]
    if par is not None:
        if par["estado"] == "corregido":
            items.append(f"La secuencia de entrada traía un error de un bit (fila {par['posicion_error'][0]}, "
                         f"columna {par['posicion_error'][1]}); la paridad vertical, longitudinal y cruzada "
                         f"permitió localizarlo y corregirlo, y el mensaje es {par['mensaje']!r}.")
        elif par["estado"] == "sin_errores":
            items.append(f"La paridad de la entrada es correcta: no se detectan errores y el mensaje es {par['mensaje']!r}.")
        else:
            items.append("La paridad detecta errores que no forman un error simple (2 o más): se detectan pero no "
                         "se pueden corregir, el mensaje no es recuperable.")
    lineas = ["CONCLUSIONES (ejercicio 2)", "-" * _ANCHO]
    for it in items:
        lineas += _envolver("- " + it, "", "  ")
    _imprimir("\n".join(lineas))
    return "\n".join("- " + it for it in items)
