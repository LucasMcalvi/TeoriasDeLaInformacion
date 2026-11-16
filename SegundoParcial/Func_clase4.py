"""
Func_clase4.py
==============
Funciones de Python para el TP4 de Teoría de la Información (clase 4):
Codificación de fuentes de información y control de errores.

Cada función tiene un docstring con: qué es, para qué se usa y cómo
interpretar el resultado. Se puede ver con help(nombre_funcion).

Índice (ejercicio de la guía -> función)
-----------------------------------------
Ej. 1   cumple_primer_teorema        (+ detalle_primer_teorema)
Ej. 6   rendimiento_redundancia
Ej. 10  analizar_codigo_hamming      (+ distancia_hamming)
Ej. 12a byte_con_paridad
Ej. 12b verificar_byte
Ej. 14a generar_mensaje_con_paridad
Ej. 14b recuperar_mensaje            (+ analizar_matriz_paridad, útil para el Ej. 13)

Herramientas de apoyo (para los ejercicios 2 a 5, 7, 8)
-------------------------------------------------------
extension_fuente, extension_codigo, huffman, shannon_fano

Agregadas para el parcial
-------------------------
filas_de_bits          corta una tira de bits (la "Entrada" del parcial) en
                       filas de 8 para pasársela a analizar_matriz_paridad
distancia_levenshtein  distancia de edición (teoría 4), por si la piden

Reutiliza funciones ya desarrolladas (tienen que estar en la misma carpeta):
  Formulas.py              CalcEntropia, DevuelveExtyFdp
  FormulasCodificacion.py  get_alfabetoCodigo, get_longitudMedia
Solo se usan las librerías math y random (esta última, a través de esos módulos).
"""

import math
from Formulas import CalcEntropia, DevuelveExtyFdp
from FormulasCodificacion import get_alfabetoCodigo, get_longitudMedia

_TOL = 1e-9


# ---------------------------------------------------------------------------
# Validaciones internas
# ---------------------------------------------------------------------------
def _validar_probs(probs):
    if len(probs) == 0:
        raise ValueError("La lista de probabilidades está vacía.")
    if any(p < 0 for p in probs):
        raise ValueError("Hay probabilidades negativas.")
    if abs(sum(probs) - 1) > 1e-6:
        raise ValueError(f"Las probabilidades suman {sum(probs)}, deberían sumar 1.")


def _orden_alfabeto(codigos, r=None):
    if r is not None:
        return r
    return max(2, len(get_alfabetoCodigo(codigos)))


def _entropia_base_r(probs, r):
    return CalcEntropia(probs) / math.log2(r)


def _longitud_media(probs, codigos):
    if len(probs) != len(codigos):
        raise ValueError("probs y codigos deben tener la misma cantidad de elementos.")
    return get_longitudMedia(codigos, probs)


# ---------------------------------------------------------------------------
# Extensiones de una fuente y de su código
# ---------------------------------------------------------------------------
def extension_fuente(probs, n):
    """
    Qué es:
        Distribución de probabilidades de la extensión de orden n de una
        fuente de memoria nula. Cada símbolo de S^n es una secuencia de n
        símbolos de S y su probabilidad es el producto de las probabilidades
        individuales.

    Para qué se usa:
        Para trabajar con bloques de n símbolos en lugar de símbolos sueltos,
        que es lo que permite acercarse a la entropía (Primer Teorema de
        Shannon). Se usa en los ejercicios 2 a 5.

    Cómo interpretar el resultado:
        - La lista tiene q**n elementos y suma 1.
        - El orden es: S1S1, S1S2, ..., S1Sq, S2S1, S2S2, ... (el último
          símbolo es el que cambia más rápido). Es el mismo orden en que hay
          que escribir las palabras código de la extensión.
        - La entropía de la extensión es n veces la de la fuente original:
          H(S^n) = n * H(S).

    Parámetros:
        probs: probabilidades de la fuente original.
        n: orden de la extensión.
    Devuelve:
        lista de q**n probabilidades.
    """
    _validar_probs(probs)
    if n < 1:
        raise ValueError("n debe ser >= 1.")
    simbolos = [str(i) for i in range(len(probs))]
    return DevuelveExtyFdp(simbolos, probs, n)[1]


def extension_codigo(codigos, n):
    """
    Qué es:
        Código de la extensión de orden n obtenido concatenando las palabras
        código de la fuente original. A la secuencia SiSj le corresponde
        c_i + c_j.

    Para qué se usa:
        Para responder "¿la extensión de orden n de la fuente, con ESTA
        codificación, cumple el Primer Teorema?" (ejercicio 2): se arma el
        código de la extensión y se lo evalúa con cumple_primer_teorema.

    Cómo interpretar el resultado:
        - Lista de q**n palabras, en el mismo orden que extension_fuente.
        - La longitud media L_n de este código es exactamente n * L, por lo
          que L_n / n = L: concatenar no mejora la compresión. Para mejorarla
          hay que volver a codificar la extensión (por ejemplo con Huffman).

    Parámetros:
        codigos: palabras código de la fuente original.
        n: orden de la extensión.
    Devuelve:
        lista de q**n strings.
    """
    if n < 1:
        raise ValueError("n debe ser >= 1.")
    return DevuelveExtyFdp(list(codigos), [1] * len(codigos), n)[0]


# ---------------------------------------------------------------------------
# Ejercicio 1: Primer Teorema de Shannon
# ---------------------------------------------------------------------------
def detalle_primer_teorema(probs, codigos, n, r=None):
    """
    Qué es:
        Versión "con detalle" de cumple_primer_teorema. Devuelve todos los
        números que intervienen en la verificación, para poder armar las
        tablas de los ejercicios 2, 3 y 5.

    Para qué se usa:
        Para ver por qué un código cumple o no cumple, y para completar la
        tabla H_r(S) / L_n / veredicto de la guía.

    Cómo interpretar el resultado (diccionario):
        'r'             orden del alfabeto del código (cantidad de símbolos
                        distintos que usan las palabras, o el r indicado).
        'H'             H_r(S): entropía de la fuente original (cota inferior).
        'Ln'            longitud media de las palabras del código de la
                        extensión de orden n.
        'Ln_sobre_n'    L_n / n: símbolos de código por símbolo de la fuente.
        'cota_superior' H_r(S) + 1/n.
        'cumple'        True si H <= L_n/n < H + 1/n.
        'motivo'        texto con la explicación del veredicto.

    Parámetros:
        probs: probabilidades de la fuente ORIGINAL (no de la extensión).
        codigos: q**n palabras código de la extensión de orden n, en el
                 orden S1S1, S1S2, ..., S1Sq, S2S1, ... (ver extension_fuente).
                 Para n=1 son simplemente las palabras de la fuente.
        n: orden de la extensión.
        r: tamaño del alfabeto del código; si no se da, se deduce de los
           símbolos usados en las palabras (mínimo 2).
    """
    _validar_probs(probs)
    if n < 1:
        raise ValueError("n debe ser >= 1.")
    if len(codigos) != len(probs) ** n:
        raise ValueError(
            f"Para n={n} se esperan {len(probs) ** n} palabras código "
            f"(q**n) y se recibieron {len(codigos)}."
        )

    orden = _orden_alfabeto(codigos, r)
    h = _entropia_base_r(probs, orden)
    ln = _longitud_media(extension_fuente(probs, n), codigos)
    ln_n = ln / n
    cota_sup = h + 1 / n

    if ln_n < h - _TOL:
        cumple = False
        motivo = (
            "L_n/n es menor que H_r(S): el código está por debajo del límite "
            "de Shannon, por lo que no puede ser unívocamente decodificable."
        )
    elif ln_n >= cota_sup - _TOL:
        cumple = False
        motivo = (
            "L_n/n es mayor o igual que H_r(S) + 1/n: el código es demasiado "
            "largo para lo que el teorema permite; se puede mejorar."
        )
    else:
        cumple = True
        motivo = "Se verifica H_r(S) <= L_n/n < H_r(S) + 1/n."

    return {
        "r": orden,
        "H": h,
        "Ln": ln,
        "Ln_sobre_n": ln_n,
        "cota_superior": cota_sup,
        "cumple": cumple,
        "motivo": motivo,
    }


def cumple_primer_teorema(probs, codigos, n, r=None):
    """
    Qué es:
        Función booleana que verifica el Primer Teorema de Shannon para la
        extensión de orden n:

            H_r(S)  <=  L_n / n  <  H_r(S) + 1/n

        H_r(S) es la entropía de la fuente original (en base r, el tamaño del
        alfabeto del código) y L_n la longitud media del código de la
        extensión de orden n.

    Para qué se usa:
        Para saber si una codificación está dentro de lo que el teorema
        permite: no puede ser más corta que la entropía y, para ser
        considerada buena, tiene que quedar a menos de 1/n de ella. Al subir
        n, esa franja se achica y L_n/n tiende a H_r(S).

    Cómo interpretar el resultado:
        - True: L_n/n está entre H y H + 1/n. El código es eficiente para ese
          orden de extensión (más cerca de H cuanto mayor es n).
        - False porque L_n/n < H: el código "comprime de más"; eso es
          imposible para un código decodificable (viola Kraft-McMillan).
        - False porque L_n/n >= H + 1/n: el código es decodificable pero
          largo de más; se puede acortar (por ejemplo con Huffman o
          codificando una extensión de mayor orden).
        - Ojo: solo verifica la desigualdad. No comprueba si el código es
          instantáneo ni unívocamente decodificable. Para ver los valores
          que intervienen usar detalle_primer_teorema.

    Parámetros:
        probs: probabilidades de la fuente ORIGINAL.
        codigos: q**n palabras código de la extensión de orden n, en orden
                 S1S1, S1S2, ..., S1Sq, S2S1, ... (n=1: las de la fuente).
        n: orden de la extensión.
        r: tamaño del alfabeto del código (opcional; se deduce de las
           palabras).
    Devuelve:
        bool.

    Ejemplo (ejercicio 3, C1 = {11, 010, 00}):
        >>> cumple_primer_teorema([0.5, 0.2, 0.3], ["11", "010", "00"], 1)
        True
    """
    return detalle_primer_teorema(probs, codigos, n, r)["cumple"]


# ---------------------------------------------------------------------------
# Ejercicio 6: rendimiento y redundancia
# ---------------------------------------------------------------------------
def rendimiento_redundancia(probs, codigos, r=None):
    """
    Qué es:
        Calcula el rendimiento (eficiencia) η = H_r(S) / L y la redundancia
        R = 1 - η de un código, a partir de dos listas paralelas: la
        probabilidad de cada símbolo y su palabra código.

    Para qué se usa:
        Para medir qué tan cerca está un código del límite ideal (la
        entropía) y comparar códigos distintos de una misma fuente
        (ejercicios 7 y 8).

    Cómo interpretar el resultado (devuelve la tupla (η, R)):
        - η cercano a 1 (R cercano a 0): código muy eficiente, casi no
          desperdicia símbolos de código.
        - η = 1 (R = 0): código compacto ideal; se da cuando cada
          probabilidad es r^(-l_i).
        - η bajo (R alto): R es la fracción de la longitud media que es
          pura redundancia, es decir, símbolos de código que no aportan
          información. Se puede mejorar el código.
        - Al comparar códigos de la misma fuente, el de mayor η (menor R) es
          mejor.
        - η > 1 no es posible en un código decodificable: indicaría que
          L < H y que el código no se puede decodificar sin ambigüedad.
        - Si se pasan las probabilidades y palabras de la extensión de orden
          n, el η que se obtiene es H(S^n)/L_n = H(S)/(L_n/n), y crece hacia
          1 al aumentar n.

    Parámetros:
        probs: probabilidades de cada símbolo (o de cada símbolo de la
               extensión).
        codigos: palabras código en el mismo orden que probs.
        r: tamaño del alfabeto del código (opcional; se deduce de las
           palabras, mínimo 2).
    Devuelve:
        tupla (rendimiento, redundancia).

    Ejemplo (ejercicio 7, código C1):
        >>> rendimiento_redundancia([0.5, 0.2, 0.3], ["11", "010", "00"])
        (0.6752..., 0.3247...)
    """
    _validar_probs(probs)
    orden = _orden_alfabeto(codigos, r)
    h = _entropia_base_r(probs, orden)
    l_media = _longitud_media(probs, codigos)
    eta = h / l_media
    return eta, 1 - eta


# ---------------------------------------------------------------------------
# Ejercicio 10: distancia de Hamming, detección y corrección
# ---------------------------------------------------------------------------
def distancia_hamming(a, b):
    """
    Qué es:
        Distancia de Hamming entre dos palabras de igual longitud: cantidad
        de posiciones en las que sus símbolos son distintos.

    Para qué se usa:
        Para medir cuántos errores de bit hacen falta para que una palabra
        se convierta en otra. Es la base para calcular la distancia de un
        código completo.

    Cómo interpretar el resultado:
        - 0: las palabras son idénticas.
        - k: hay que alterar k bits para pasar de una a otra. Ejemplo:
          d(01010101, 00001111) = 4.
        - Solo está definida para palabras de la misma longitud.

    Parámetros:
        a, b: strings de igual longitud.
    Devuelve:
        int.
    """
    if len(a) != len(b):
        raise ValueError("La distancia de Hamming requiere palabras de igual longitud.")
    return sum(x != y for x, y in zip(a, b))


def analizar_codigo_hamming(codigos):
    """
    Qué es:
        Dada una codificación (lista de palabras código), calcula su
        distancia de Hamming d_min (la menor distancia entre todos los pares
        de palabras) y, a partir de ella, cuántos errores puede detectar y
        cuántos puede corregir.

            detecta  α = d_min - 1
            corrige  β = (d_min - 1) // 2     (parte entera)

    Para qué se usa:
        Para evaluar la capacidad de protección contra errores de un código
        de bloque (ejercicios 9 y 11).

    Cómo interpretar el resultado (devuelve (d_min, detectables, corregibles)):
        - d_min = 1: no detecta ni corrige nada; un error en un bit
          convierte una palabra válida en otra palabra válida.
        - d_min = 2: detecta 1 error, no corrige ninguno (ej.: bit de
          paridad simple).
        - d_min = 3: detecta hasta 2 errores o bien corrige 1.
        - d_min = 4: detecta hasta 3 errores y corrige 1.
        - d_min = 5: detecta hasta 4 errores y corrige 2.
        - En general, corregir β errores exige d_min >= 2β + 1 y detectar α
          errores exige d_min >= α + 1. Detectar y corregir al mismo tiempo
          comparten la capacidad del código ("o bien", no "y además").
        - d_min = 0 significa que hay palabras repetidas (código inválido).

    Parámetros:
        codigos: lista de al menos 2 strings de igual longitud.
    Devuelve:
        tupla (distancia_hamming, errores_detectables, errores_corregibles).

    Ejemplo (ejercicio 9, código 3):
        >>> analizar_codigo_hamming(["0000", "0011", "1010", "0101"])
        (2, 1, 0)
    """
    codigos = list(codigos)
    if len(codigos) < 2:
        raise ValueError("Se necesitan al menos 2 palabras código.")
    d = None
    for i in range(len(codigos)):
        for j in range(i + 1, len(codigos)):
            dij = distancia_hamming(codigos[i], codigos[j])
            if d is None or dij < d:
                d = dij
    detectables = max(d - 1, 0)
    corregibles = max((d - 1) // 2, 0)
    return d, detectables, corregibles


# ---------------------------------------------------------------------------
# Distancia de Levenshtein (teoría 4)
# ---------------------------------------------------------------------------
def distancia_levenshtein(a, b):
    """
    Qué es:
        Distancia de Levenshtein (o de edición) entre dos cadenas: la menor
        cantidad de operaciones de inserción, eliminación o sustitución de
        un símbolo necesarias para transformar una en la otra.

    Para qué se usa:
        Para comparar cadenas cuando el canal puede agregar o perder
        símbolos (no solo invertirlos). A diferencia de Hamming, sirve para
        cadenas de distinta longitud.

    Cómo interpretar el resultado:
        - 0: las cadenas son iguales.
        - k: hacen falta k ediciones como mínimo para pasar de una a otra.
        - Siempre es <= que la de Hamming (cuando las longitudes son
          iguales), porque una sustitución también es una edición.
        - Es al menos la diferencia de longitudes.

    Parámetros:
        a, b: strings.
    Devuelve:
        int.

    Ejemplo:
        >>> distancia_levenshtein("casa", "calle")
        3
    """
    anterior = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        actual = [i]
        for j, y in enumerate(b, 1):
            actual.append(min(anterior[j] + 1,              # eliminación
                              actual[j - 1] + 1,            # inserción
                              anterior[j - 1] + (x != y)))  # sustitución
        anterior = actual
    return anterior[-1]


# ---------------------------------------------------------------------------
# Ejercicio 12: paridad simple sobre un carácter ASCII
# ---------------------------------------------------------------------------
def byte_con_paridad(caracter):
    """
    Qué es:
        Convierte un carácter en un byte: los 7 bits de su código ASCII en
        las posiciones altas y, en el bit menos significativo, un bit de
        paridad par (se elige 0 o 1 para que la cantidad total de unos del
        byte sea par).

    Para qué se usa:
        Para agregar detección de errores a cada carácter transmitido (el
        chequeo de paridad vertical, VRC, de la teoría).

    Cómo interpretar el resultado:
        - Devuelve un entero de 0 a 255. Para ver los bits: format(b, '08b').
        - Los 7 bits de arriba son el carácter; el último es la paridad.
        - El byte siempre tiene cantidad par de unos. Ejemplo: 'C' (1000011)
          tiene tres unos, entonces el bit de paridad es 1 y el byte es
          10000111.
        - El carácter debe ser ASCII de 7 bits (código < 128).

    Parámetros:
        caracter: string de longitud 1.
    Devuelve:
        int entre 0 y 255.
    """
    if len(caracter) != 1:
        raise ValueError("Se debe pasar exactamente un carácter.")
    codigo = ord(caracter)
    if codigo > 127:
        raise ValueError("El carácter no pertenece al ASCII de 7 bits.")
    paridad = bin(codigo).count("1") % 2
    return (codigo << 1) | paridad


def verificar_byte(byte):
    """
    Qué es:
        Verifica un byte generado con byte_con_paridad comprobando que su
        cantidad de unos sea par.

    Para qué se usa:
        Para detectar errores de transmisión en un carácter protegido con
        un bit de paridad.

    Cómo interpretar el resultado:
        - True: la paridad es correcta; no se detectaron errores.
        - False: hubo un error (en realidad, una cantidad impar de bits
          alterados). Se sabe que el byte está mal, pero no cuál bit ni se
          puede corregir.
        - Limitación: si se alteraron 2 bits (o cualquier cantidad par), la
          paridad sigue dando bien y el error pasa desapercibido, porque la
          distancia de Hamming de este código es 2.

    Parámetros:
        byte: int entre 0 y 255 (o un objeto bytes/bytearray de un byte).
    Devuelve:
        bool.
    """
    if isinstance(byte, (bytes, bytearray)):
        if len(byte) != 1:
            raise ValueError("Se debe pasar exactamente un byte.")
        byte = byte[0]
    if not 0 <= byte <= 255:
        raise ValueError("El byte debe estar entre 0 y 255.")
    return bin(byte).count("1") % 2 == 0


# ---------------------------------------------------------------------------
# Ejercicios 13 y 14: paridad vertical, longitudinal y cruzada
# ---------------------------------------------------------------------------
def filas_de_bits(cadena, ancho=8):
    """
    Qué es:
        Corta una tira de bits en filas de 'ancho' bits (por defecto 8).

    Para qué se usa:
        En el parcial la "Entrada" del canal viene como una sola tira, por
        ejemplo 10100000101011101001111110011001 (32 bits). Hay que cortarla
        en filas de 8 para armar la matriz de paridad y pasársela a
        analizar_matriz_paridad.

    Cómo interpretar el resultado:
        - Lista de strings de 'ancho' bits. Con el formato de la cátedra, la
          PRIMERA fila es la de paridad longitudinal (LRC) y las siguientes
          son los caracteres (7 bits ASCII + paridad vertical).
        - 32 bits -> 4 filas -> 1 fila LRC + 3 caracteres.

    Parámetros:
        cadena: string de '0' y '1' cuya longitud es múltiplo de 'ancho'.
        ancho: bits por fila.
    Devuelve:
        list de str.
    """
    cadena = cadena.strip()
    if len(cadena) % ancho:
        raise ValueError(f"La cadena tiene {len(cadena)} bits, que no es múltiplo de {ancho}.")
    return [cadena[i:i + ancho] for i in range(0, len(cadena), ancho)]


def analizar_matriz_paridad(filas):
    """
    Qué es:
        Analiza una matriz de bits con paridad vertical, longitudinal y
        cruzada (paridad par), detecta errores y, si es un error simple, lo
        corrige. Es la herramienta para resolver el ejercicio 13.

        Formato de la matriz (el mismo de la guía), lista de strings de 8
        bits:
          - Fila 1: paridad longitudinal (LRC). Cada bit es la paridad de
            su columna; el último bit es la paridad cruzada.
          - Filas 2 en adelante: un carácter por fila, 7 bits ASCII + bit de
            paridad (vertical) en el último lugar.
        Se numeran filas y columnas desde 1, como se lee en la guía.

    Para qué se usa:
        Para recuperar el mensaje original de una transmisión con ruido
        cuando se puede, o saber que no se puede.

    Cómo interpretar el resultado (diccionario):
        'estado':
            'sin_errores'  ninguna fila ni columna falla; el mensaje es
                           correcto.
            'corregido'    falla exactamente 1 fila y 1 columna; el error
                           está en su intersección y se corrige invirtiendo
                           ese bit.
            'no_corregible' hay errores pero no forman un error simple (por
                           ejemplo 2 errores): se detectan, no se pueden
                           corregir.
        'filas_con_error':    filas cuya paridad no cierra.
        'columnas_con_error': columnas cuya paridad no cierra.
        'posicion_error':     (fila, columna) del bit corregido, o None.
        'matriz_corregida':   la matriz ya corregida (igual a la original si
                              no había errores), o None si no es corregible.
        'mensaje':            texto decodificado, o '' si no es corregible.
        - Esta estructura tiene d_min = 4: detecta hasta 3 errores y corrige
          1. Con 3 errores que casualmente se vean como un error simple, la
          corrección es incorrecta sin que se pueda notar.

    Parámetros:
        filas: lista de strings de '0' y '1', todos de 8 caracteres.
    """
    filas = [str(f) for f in filas]
    if not filas:
        raise ValueError("La matriz está vacía.")
    if any(len(f) != 8 or set(f) - {"0", "1"} for f in filas):
        raise ValueError("Cada fila debe ser un string de 8 bits ('0'/'1').")

    bits = [[int(b) for b in f] for f in filas]
    filas_err = [i for i, fila in enumerate(bits) if sum(fila) % 2]
    cols_err = [j for j in range(8) if sum(fila[j] for fila in bits) % 2]

    resultado = {
        "estado": None,
        "filas_con_error": [i + 1 for i in filas_err],
        "columnas_con_error": [j + 1 for j in cols_err],
        "posicion_error": None,
        "matriz_corregida": None,
        "mensaje": "",
    }

    if not filas_err and not cols_err:
        resultado["estado"] = "sin_errores"
        corregida = filas
    elif len(filas_err) == 1 and len(cols_err) == 1:
        i, j = filas_err[0], cols_err[0]
        bits[i][j] ^= 1
        corregida = ["".join(map(str, fila)) for fila in bits]
        resultado["estado"] = "corregido"
        resultado["posicion_error"] = (i + 1, j + 1)
    else:
        resultado["estado"] = "no_corregible"
        return resultado

    resultado["matriz_corregida"] = corregida
    resultado["mensaje"] = "".join(chr(int(f[:7], 2)) for f in corregida[1:])
    return resultado


def generar_mensaje_con_paridad(cadena):
    """
    Qué es:
        Convierte una cadena de texto en un bytearray protegido con paridad
        vertical, longitudinal y cruzada (paridad par).

        Formato del resultado (igual al de las matrices del ejercicio 13):
          - Byte 0: fila de paridad longitudinal; su último bit es la
            paridad cruzada.
          - Bytes 1 en adelante: un byte por carácter, con 7 bits ASCII y el
            bit de paridad vertical al final (ver byte_con_paridad).

    Para qué se usa:
        Para transmitir texto con capacidad de detectar hasta 3 errores y
        corregir 1 error simple por mensaje.

    Cómo interpretar el resultado:
        - Largo = cantidad de caracteres + 1 byte.
        - Se puede ver como matriz con
          [format(b, '08b') for b in resultado].
        - Todas las filas y todas las columnas de esa matriz tienen cantidad
          par de unos.
        - Para decodificarlo y corregirlo se usa recuperar_mensaje.
        - Todos los caracteres deben ser ASCII de 7 bits.

    Parámetros:
        cadena: string.
    Devuelve:
        bytearray.
    """
    filas = [byte_con_paridad(c) for c in cadena]
    lrc = 0
    for fila in filas:
        lrc ^= fila
    return bytearray([lrc] + filas)


def recuperar_mensaje(secuencia):
    """
    Qué es:
        Decodifica una secuencia de bytes generada con
        generar_mensaje_con_paridad: verifica las paridades, corrige un
        error simple si lo hay y devuelve el texto original.

    Para qué se usa:
        Para recibir un mensaje a través de un canal con ruido y recuperar
        el texto cuando es posible.

    Cómo interpretar el resultado:
        - Un texto: el mensaje es correcto, ya sea porque no hubo errores o
          porque había un único error y fue corregido.
        - Cadena vacía '': se detectaron errores que no se pueden corregir
          (por ejemplo 2 errores). El mensaje no es confiable y habría que
          pedir retransmisión.
        - Limitación: un mensaje vacío también devuelve ''. Si hubo 3
          errores con forma de error simple, se "corrige" mal sin avisar.
        - Para saber qué pasó exactamente (dónde estaba el error, qué filas
          y columnas fallaron) usar analizar_matriz_paridad.

    Parámetros:
        secuencia: bytes o bytearray con el formato de
                   generar_mensaje_con_paridad.
    Devuelve:
        str.
    """
    filas = [format(b, "08b") for b in secuencia]
    if not filas:
        return ""
    return analizar_matriz_paridad(filas)["mensaje"]


# ---------------------------------------------------------------------------
# Apoyo para ejercicios 4 y 5: construcción de códigos
# ---------------------------------------------------------------------------
def huffman(probs):
    """
    Qué es:
        Algoritmo de Huffman para un alfabeto binario: construye un código
        instantáneo óptimo (compacto) para la distribución dada, fusionando
        siempre los dos símbolos menos probables.

    Para qué se usa:
        Para obtener la mejor codificación posible símbolo a símbolo
        (ejercicio 5a) y para codificar extensiones de una fuente
        (ejercicio 4), donde acerca L_n/n a la entropía. En el parcial,
        "código binario óptimo" = Huffman.

    Cómo interpretar el resultado:
        - Devuelve una lista de palabras código en el mismo orden que probs.
        - Es un código instantáneo (ninguna palabra es prefijo de otra).
        - Su longitud media es la mínima posible para esa distribución: no
          existe un código instantáneo binario con menor L. Se puede
          evaluar con get_longitudMedia, rendimiento_redundancia y
          cumple_primer_teorema.
        - Si hay probabilidades empatadas, pueden salir otras palabras
          (o largos repartidos distinto) igual de válidas; la longitud media
          es la misma.
        - Una fuente de 2 símbolos siempre da longitudes {1, 1}, sin
          importar las probabilidades.

    Parámetros:
        probs: lista de probabilidades.
    Devuelve:
        lista de strings de '0' y '1'.
    """
    _validar_probs(probs)
    if len(probs) == 1:
        return ["0"]

    codigos = [""] * len(probs)
    grupos = [[p, [i]] for i, p in enumerate(probs)]
    while len(grupos) > 1:
        grupos.sort(key=lambda g: g[0])
        menor = grupos.pop(0)
        siguiente = grupos.pop(0)
        for i in menor[1]:
            codigos[i] = "0" + codigos[i]
        for i in siguiente[1]:
            codigos[i] = "1" + codigos[i]
        grupos.append([menor[0] + siguiente[0], menor[1] + siguiente[1]])
    return codigos


def shannon_fano(probs):
    """
    Qué es:
        Algoritmo de Shannon-Fano para un alfabeto binario: ordena los
        símbolos de mayor a menor probabilidad, los parte en dos grupos con
        suma de probabilidades lo más parecida posible (el grupo de arriba
        recibe un 1 y el de abajo un 0) y repite el proceso dentro de cada
        grupo.

    Para qué se usa:
        Para obtener una codificación alternativa a Huffman (ejercicio 5b).
        Es un método más simple pero subóptimo.

    Cómo interpretar el resultado:
        - Devuelve una lista de palabras código en el mismo orden que probs
          (no en el orden de las probabilidades ordenadas).
        - Es un código instantáneo. Los símbolos más probables reciben
          palabras más cortas.
        - Su longitud media es mayor o igual que la de Huffman; cuando
          coinciden, el código es igual de bueno.
        - Si hay más de una forma de partir con la misma diferencia mínima,
          se elige el corte con menos símbolos arriba. Con probabilidades
          empatadas se ubica primero el símbolo que aparece más tarde en la
          lista (es el criterio con el que coinciden los resultados de las
          guías). Cambiar ese orden no altera la longitud media.

    Parámetros:
        probs: lista de probabilidades.
    Devuelve:
        lista de strings de '0' y '1'.
    """
    _validar_probs(probs)
    codigos = [""] * len(probs)
    if len(probs) == 1:
        return ["0"]

    def dividir(indices):
        if len(indices) <= 1:
            return
        total = sum(probs[i] for i in indices)
        acumulado = 0.0
        mejor_k, mejor_dif = 1, float("inf")
        for k in range(1, len(indices)):
            acumulado += probs[indices[k - 1]]
            dif = abs(acumulado - (total - acumulado))
            if dif < mejor_dif - _TOL:
                mejor_k, mejor_dif = k, dif
        for i in indices[:mejor_k]:
            codigos[i] += "1"
        for i in indices[mejor_k:]:
            codigos[i] += "0"
        dividir(indices[:mejor_k])
        dividir(indices[mejor_k:])

    dividir(sorted(range(len(probs)), key=lambda i: (-probs[i], -i)))
    return codigos
