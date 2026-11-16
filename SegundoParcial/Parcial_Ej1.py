"""
Parcial - Ejercicio 1 (fuente + código óptimo + extensión + Primer Teorema)
==========================================================================
Plantilla: en el parcial SOLO hay que cambiar MENSAJE y N.
Archivo AUTOCONTENIDO (no importa nada propio; solo math). Antes necesitaba: Formulas.py, FormulasCodificacion.py,
Func_clase4.py y Func_clase5.py.
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


# --- DevuelveExtyFdp (de Formulas.py)
def DevuelveExtyFdp(simbolos, probs, n):
    ext, fdp = ([''], [1.0])
    for _ in range(n):
        ext = [e + s for e in ext for s in simbolos]
        fdp = [f * p for f in fdp for p in probs]
    return (ext, fdp)


# --- get_alfabetoCodigo (de FormulasCodificacion.py)
def get_alfabetoCodigo(codigos):
    return sorted(set(''.join(codigos)))


# --- get_longitudMedia (de FormulasCodificacion.py)
def get_longitudMedia(codigos, probs):
    return sum((len(c) * p for c, p in zip(codigos, probs)))


# --- _validar_probs (de Func_clase4.py)
def _validar_probs(probs):
    if len(probs) == 0:
        raise ValueError('La lista de probabilidades está vacía.')
    if any((p < 0 for p in probs)):
        raise ValueError('Hay probabilidades negativas.')
    if abs(sum(probs) - 1) > 1e-06:
        raise ValueError(f'Las probabilidades suman {sum(probs)}, deberían sumar 1.')


# --- _orden_alfabeto (de Func_clase4.py)
def _orden_alfabeto(codigos, r=None):
    if r is not None:
        return r
    return max(2, len(get_alfabetoCodigo(codigos)))


# --- _entropia_base_r (de Func_clase4.py)
def _entropia_base_r(probs, r):
    return CalcEntropia(probs) / math.log2(r)


# --- _longitud_media (de Func_clase4.py)
def _longitud_media(probs, codigos):
    if len(probs) != len(codigos):
        raise ValueError('probs y codigos deben tener la misma cantidad de elementos.')
    return get_longitudMedia(codigos, probs)


# --- extension_fuente (de Func_clase4.py)
def extension_fuente(probs, n):
    _validar_probs(probs)
    if n < 1:
        raise ValueError('n debe ser >= 1.')
    simbolos = [str(i) for i in range(len(probs))]
    return DevuelveExtyFdp(simbolos, probs, n)[1]


# --- detalle_primer_teorema (de Func_clase4.py)
def detalle_primer_teorema(probs, codigos, n, r=None):
    _validar_probs(probs)
    if n < 1:
        raise ValueError('n debe ser >= 1.')
    if len(codigos) != len(probs) ** n:
        raise ValueError(f'Para n={n} se esperan {len(probs) ** n} palabras código (q**n) y se recibieron {len(codigos)}.')
    orden = _orden_alfabeto(codigos, r)
    h = _entropia_base_r(probs, orden)
    ln = _longitud_media(extension_fuente(probs, n), codigos)
    ln_n = ln / n
    cota_sup = h + 1 / n
    if ln_n < h - _TOL:
        cumple = False
        motivo = 'L_n/n es menor que H_r(S): el código está por debajo del límite de Shannon, por lo que no puede ser unívocamente decodificable.'
    elif ln_n >= cota_sup - _TOL:
        cumple = False
        motivo = 'L_n/n es mayor o igual que H_r(S) + 1/n: el código es demasiado largo para lo que el teorema permite; se puede mejorar.'
    else:
        cumple = True
        motivo = 'Se verifica H_r(S) <= L_n/n < H_r(S) + 1/n.'
    return {'r': orden, 'H': h, 'Ln': ln, 'Ln_sobre_n': ln_n, 'cota_superior': cota_sup, 'cumple': cumple, 'motivo': motivo}


# --- rendimiento_redundancia (de Func_clase4.py)
def rendimiento_redundancia(probs, codigos, r=None):
    _validar_probs(probs)
    orden = _orden_alfabeto(codigos, r)
    h = _entropia_base_r(probs, orden)
    l_media = _longitud_media(probs, codigos)
    eta = h / l_media
    return (eta, 1 - eta)


# --- huffman (de Func_clase4.py)
def huffman(probs):
    _validar_probs(probs)
    if len(probs) == 1:
        return ['0']
    codigos = [''] * len(probs)
    grupos = [[p, [i]] for i, p in enumerate(probs)]
    while len(grupos) > 1:
        grupos.sort(key=lambda g: g[0])
        menor = grupos.pop(0)
        siguiente = grupos.pop(0)
        for i in menor[1]:
            codigos[i] = '0' + codigos[i]
        for i in siguiente[1]:
            codigos[i] = '1' + codigos[i]
        grupos.append([menor[0] + siguiente[0], menor[1] + siguiente[1]])
    return codigos


# --- alfabeto_y_probabilidades (de Func_clase5.py)
def alfabeto_y_probabilidades(mensaje):
    if not mensaje:
        raise ValueError('El mensaje está vacío.')
    alfabeto = sorted(set(mensaje))
    probabilidades = [mensaje.count(c) / len(mensaje) for c in alfabeto]
    return (alfabeto, probabilidades)


# --- resumen_codigo (de Func_clase5.py)
def resumen_codigo(probs, codigos):
    if len(probs) != len(codigos):
        raise ValueError('probs y codigos deben tener la misma cantidad de elementos.')
    r = max(2, len(set(''.join(codigos))))
    eta, redundancia = rendimiento_redundancia(probs, codigos)
    return {'H': CalcEntropia(probs) / math.log2(r), 'L': get_longitudMedia(codigos, probs), 'rendimiento': eta, 'redundancia': redundancia}


# --- codificar_mensaje (de Func_clase5.py)
def codificar_mensaje(mensaje, alfabeto, codigos, cabecera=True):
    if len(alfabeto) != len(codigos):
        raise ValueError('alfabeto y codigos deben tener la misma cantidad de elementos.')
    tabla = {s: c for s, c in zip(alfabeto, codigos)}
    faltan = sorted(set(mensaje) - set(tabla))
    if faltan:
        raise ValueError(f'Caracteres que no están en el alfabeto: {faltan}')
    bits = ''.join((tabla[c] for c in mensaje))
    relleno = (8 - len(bits) % 8) % 8
    bits += '0' * relleno
    datos = [int(bits[i:i + 8], 2) for i in range(0, len(bits), 8)]
    return bytearray(([relleno] if cabecera else []) + datos)


# --- tasa_compresion (de Func_clase5.py)
def tasa_compresion(mensaje, comprimido, como_fraccion=False):
    original = len(mensaje)
    final = len(comprimido)
    if final == 0:
        raise ValueError('La secuencia comprimida está vacía.')
    if como_fraccion:
        d = math.gcd(original, final)
        return f'{original // d}/{final // d}'
    return original / final


# --- tasa_compresion_codigo (de Func_clase5.py)
def tasa_compresion_codigo(mensaje, alfabeto, codigos):
    return tasa_compresion(mensaje, codificar_mensaje(mensaje, alfabeto, codigos, cabecera=False))


# ======================================================================
# RESOLUCIÓN
# ======================================================================

# ------------------------- DATOS DEL PARCIAL -------------------------
MENSAJE = "GIIHGGGHGIHHIHIIGFHH"   # parcial 2025
N = 3                              # orden de la extensión
# ---------------------------------------------------------------------

# 1) Probabilidades (frecuencias relativas) y entropía
alfabeto, probs = alfabeto_y_probabilidades(MENSAJE)
print("Probabilidades:")
for s, p in zip(alfabeto, probs):
    print(f"  P({s}) = {p:.4f}")

# 2) Código binario óptimo (Huffman) para la fuente
codigo = huffman(probs)
print("Código de Huffman para la fuente:")
for s, c in zip(alfabeto, codigo):
    print(f"  {s} -> {c}")

fuente = resumen_codigo(probs, codigo)
print(f"Entropía de la fuente: H2(S) = {fuente['H']:.4f} bits/símbolo")

# 3) Tasa de compresión (sin bytes extra, como pide la aclaración)
print(f"Tasa de compresión: {tasa_compresion_codigo(MENSAJE, alfabeto, codigo):.4f}:1")
bits = sum(len(codigo[alfabeto.index(c)]) for c in MENSAJE)
print(f"  (original {8 * len(MENSAJE)} bits / comprimido {bits} bits = {8 * len(MENSAJE) / bits:.4f}:1 contando bits exactos)")

# 4) Código óptimo (Huffman) para la extensión de orden N
probs_ext = extension_fuente(probs, N)
codigo_ext = huffman(probs_ext)
ext = resumen_codigo(probs_ext, codigo_ext)

# 5) Longitud media, rendimiento y redundancia de cada código
print("Código para la fuente:")
print(f"  L = {fuente['L']:.4f}   η = {fuente['rendimiento']:.4f}   R = {fuente['redundancia']:.4f}")
print(f"Código para la extensión de orden {N}:")
print(f"  L = {ext['L']:.4f}   η = {ext['rendimiento']:.4f}   R = {ext['redundancia']:.4f}")
print(f"  (L/N = {ext['L'] / N:.4f} binits por símbolo original)")

# 6) Primer Teorema de Shannon:  H(S) <= L_n/n < H(S) + 1/n
for nombre, cod, n in (("Fuente", codigo, 1), ("Extensión", codigo_ext, N)):
    d = detalle_primer_teorema(probs, cod, n)
    veredicto = "Cumple" if d["cumple"] else "NO cumple"
    print(f"Primer Teorema ({nombre}, n={n}): {d['H']:.4f} <= {d['Ln_sobre_n']:.4f} "
          f"< {d['cota_superior']:.4f}  ->  {veredicto}")