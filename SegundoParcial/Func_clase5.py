"""
Func_clase5.py
==============
Funciones de Python para el TP5 de Teoría de la Información (clase 5):
Compresión de datos.

Cada función tiene un docstring con: qué es, para qué se usa y cómo
interpretar el resultado. Se puede ver con help(nombre_funcion).

Índice (ejercicio de la guía -> función)
-----------------------------------------
Ej. 3   huffman, shannon_fano            (vienen de Func_clase4)
Ej. 7a  codificar_mensaje
Ej. 7b  decodificar_mensaje
Ej. 8   tasa_compresion
Ej. 9   guardar_binario, leer_binario    (+ los de los ejercicios 3, 7 y 8)
Ej. 11  rlc_comprimir                    (+ rlc_descomprimir)

Herramientas de apoyo para los ejercicios teóricos
--------------------------------------------------
Ej. 2, 5, 9  alfabeto_y_probabilidades
Ej. 4, 5, 9  resumen_codigo
Ej. 4d       dibujar_arbol (dibujo de arriba hacia abajo), arbol_codigo
Ej. 6        decodificar_cadena
Ej. 10       rlc_texto

Agregada para el parcial
------------------------
tasa_compresion_codigo   tasa de compresión SIN bytes extra (lo que pide la
                         aclaración del parcial: "no incluir ningún tipo de
                         redundancia adicional")

Reutiliza funciones ya desarrolladas (tienen que estar en la misma carpeta):
  Formulas.py              CalcEntropia
  FormulasCodificacion.py  get_longitudMedia, es_instantaneo
  Func_clase4.py           huffman, shannon_fano, rendimiento_redundancia
Solo se usan las librerías math y random (esta última, a través de esos módulos).
"""

import math
from Formulas import CalcEntropia
from FormulasCodificacion import get_longitudMedia, es_instantaneo
from Func_clase4 import huffman, shannon_fano, rendimiento_redundancia


# ---------------------------------------------------------------------------
# Apoyo: fuente a partir de un mensaje, métricas y árbol
# ---------------------------------------------------------------------------
def alfabeto_y_probabilidades(mensaje):
    """
    Qué es:
        Obtiene la fuente de información que representa un mensaje: el
        alfabeto (los caracteres distintos, ordenados) y la probabilidad de
        cada uno, estimada como su frecuencia relativa en el mensaje.

    Para qué se usa:
        Para los ejercicios que dan un "mensaje representativo" en lugar de
        una tabla de probabilidades (2 y 5, y el ejercicio 1 del parcial),
        y para preparar cualquier texto antes de codificarlo con Huffman o
        Shannon-Fano (9).

    Cómo interpretar el resultado:
        - Devuelve (alfabeto, probabilidades). El alfabeto es una lista con
          los símbolos ordenados y las probabilidades una lista paralela que
          suma 1 (la posición i de una corresponde a la posición i de la otra).
        - A diferencia de GeneraAlfabetoYProb (Formulas.py), el espacio
          cuenta como un símbolo más, porque en el ejercicio 9 es el
          símbolo más frecuente.
        - Cuanto más representativo (largo) sea el mensaje, más se parecen
          estas frecuencias a las probabilidades reales de la fuente.

    Parámetros:
        mensaje: string no vacío.
    Devuelve:
        tupla (alfabeto: list, probabilidades: list).
    """
    if not mensaje:
        raise ValueError("El mensaje está vacío.")
    alfabeto = sorted(set(mensaje))
    probabilidades = [mensaje.count(c) / len(mensaje) for c in alfabeto]
    return alfabeto, probabilidades


def resumen_codigo(probs, codigos):
    """
    Qué es:
        Reúne en un solo resultado las métricas de un código: entropía de
        la fuente, longitud media, rendimiento y redundancia.

    Para qué se usa:
        Para comparar los códigos de Huffman y de Shannon-Fano de una misma
        fuente (ejercicios 4e, 5d y 9).

    Cómo interpretar el resultado (diccionario):
        'H'            entropía de la fuente (bits/símbolo). Es el mínimo
                       teórico de L.
        'L'            longitud media del código (binits/símbolo).
        'rendimiento'  η = H/L. Cuanto más cerca de 1, mejor.
        'redundancia'  1 - η: fracción de la longitud que se desperdicia.
        - Entre dos códigos de la misma fuente, el de menor L es el de
          mayor η y menor redundancia, o sea, el que más comprime.
        - Huffman siempre da el L mínimo; Shannon-Fano puede igualarlo o
          quedar por encima.
        - Si las palabras usan un alfabeto de r símbolos, H se expresa en
          base r.
        - Si se pasan las probabilidades y el código de una EXTENSIÓN de
          orden n, 'H' es H(S^n) = n*H(S) y 'L' es L_n (binits por bloque
          de n símbolos), que es lo que pide el parcial como "L de la
          extensión".

    Parámetros:
        probs: probabilidades de la fuente.
        codigos: palabras código en el mismo orden que probs.
    Devuelve:
        dict.
    """
    if len(probs) != len(codigos):
        raise ValueError("probs y codigos deben tener la misma cantidad de elementos.")
    r = max(2, len(set("".join(codigos))))
    eta, redundancia = rendimiento_redundancia(probs, codigos)
    return {
        "H": CalcEntropia(probs) / math.log2(r),
        "L": get_longitudMedia(codigos, probs),
        "rendimiento": eta,
        "redundancia": redundancia,
    }


def arbol_codigo(codigos, simbolos=None):
    """
    Qué es:
        Devuelve, como texto, el árbol binario que corresponde a un código:
        cada palabra es el camino desde la raíz hasta una hoja (0 y 1 son
        las ramas).

    Para qué se usa:
        Como guía para graficar los árboles de Huffman y Shannon-Fano
        (ejercicio 4d). Se muestra con print(arbol_codigo(...)).

    Cómo interpretar el resultado:
        - Cada nivel de sangría es un nivel de profundidad; la profundidad
          de una hoja es la longitud de su palabra.
        - Las hojas muestran "-> símbolo".
        - En un código instantáneo todos los símbolos están en hojas: ninguno
          queda en un nodo intermedio (ninguna palabra es prefijo de otra).
        - Un árbol "completo" (todo nodo intermedio tiene sus dos hijos)
          indica que no hay ramas desperdiciadas; Huffman siempre lo cumple.

    Parámetros:
        codigos: lista de palabras binarias.
        simbolos: nombres de los símbolos (string o lista); si no se dan,
                  se usan S1, S2, ...
    Devuelve:
        str.
    """
    if simbolos is None:
        simbolos = [f"S{i + 1}" for i in range(len(codigos))]
    if len(simbolos) != len(codigos):
        raise ValueError("simbolos y codigos deben tener la misma cantidad de elementos.")

    hoja = {c: s for s, c in zip(simbolos, codigos)}
    lineas = ["(raíz)"]

    def recorrer(prefijo):
        for bit in "01":
            camino = prefijo + bit
            if camino in hoja:
                lineas.append("    " * len(prefijo) + f"{bit} -> {hoja[camino]}")
            if any(c.startswith(camino) and c != camino for c in codigos):
                if camino not in hoja:
                    lineas.append("    " * len(prefijo) + bit)
                recorrer(camino)

    recorrer("")
    return "\n".join(lineas)


def dibujar_arbol(codigos, probs=None, simbolos=None, decimales=3):
    """
    Qué es:
        Dibuja en pantalla el árbol binario de un código, de arriba hacia
        abajo, como se dibuja en el pizarrón: la raíz arriba, cada nodo se
        abre en dos ramas (0 a la izquierda, 1 a la derecha) y los símbolos
        quedan en las hojas de abajo.

    Para qué se usa:
        Para graficar los árboles de Huffman y Shannon-Fano (ejercicio 4d)
        y poder compararlos. Se muestra con print(dibujar_arbol(...)).

    Cómo interpretar el resultado:
        - Cada hoja muestra el símbolo y, debajo, su probabilidad.
        - Cada nodo intermedio muestra entre paréntesis la suma de las
          probabilidades de todo lo que cuelga de él. La raíz siempre suma 1.
        - La palabra código de un símbolo se lee juntando los 0 y 1 de las
          ramas desde la raíz hasta su hoja.
        - La cantidad de niveles que hay que bajar hasta una hoja es la
          longitud de su palabra: los símbolos más probables deberían
          quedar más arriba.
        - Si aparece una "x", esa rama quedó sin usar (el código no es
          completo y se desperdicia una palabra posible). En Huffman y
          Shannon-Fano no debería aparecer.
        - Con muchos símbolos (por ejemplo los 32 del ejercicio 9) el
          dibujo queda muy ancho y conviene agrandar la ventana o usar
          arbol_codigo.

    Parámetros:
        codigos: lista de palabras binarias.
        probs: lista de probabilidades en el mismo orden (opcional; si no
               se da, el árbol se dibuja sin probabilidades).
        simbolos: nombres de los símbolos (string o lista); si no se dan,
                  se usan S1, S2, ...
        decimales: cantidad de decimales con que se muestran las
                   probabilidades (para el ejercicio 9 conviene 6).
    Devuelve:
        str.
    """
    if simbolos is None:
        simbolos = [f"S{i + 1}" for i in range(len(codigos))]
    simbolos = list(simbolos)
    if len(simbolos) != len(codigos):
        raise ValueError("simbolos y codigos deben tener la misma cantidad de elementos.")
    if probs is not None and len(probs) != len(codigos):
        raise ValueError("probs y codigos deben tener la misma cantidad de elementos.")

    indice_de = {c: i for i, c in enumerate(codigos)}
    separacion = 3

    def texto_prob(prefijo):
        total = sum(probs[i] for i, c in enumerate(codigos) if c.startswith(prefijo))
        return f"{total:.{decimales}f}"

    def centrar(lineas):
        ancho = max(len(l) for l in lineas)
        return [l.center(ancho) for l in lineas], ancho, (ancho - 1) // 2

    def bloque(prefijo):
        # Hoja: un símbolo.
        if prefijo in indice_de:
            i = indice_de[prefijo]
            lineas = [simbolos[i]]
            if probs is not None:
                lineas.append(f"{probs[i]:.{decimales}f}")
            return centrar(lineas)

        # Rama sin usar.
        if not any(c.startswith(prefijo) for c in codigos):
            return centrar(["x"])

        # Nodo intermedio: se arma con sus dos hijos.
        izq, ancho_izq, centro_izq = bloque(prefijo + "0")
        der, ancho_der, centro_der = bloque(prefijo + "1")
        ancho = ancho_izq + separacion + ancho_der
        centro_der += ancho_izq + separacion
        raiz = (centro_izq + centro_der) // 2

        etiqueta = f"({texto_prob(prefijo)})" if probs is not None else "o"
        inicio = raiz - len(etiqueta) // 2
        corrimiento = max(0, -inicio)
        relleno = max(0, inicio + corrimiento + len(etiqueta) - (ancho + corrimiento))

        fila_ramas = [" "] * ancho
        fila_bits = [" "] * ancho
        for x in range(centro_izq, centro_der + 1):
            fila_ramas[x] = "─"
        fila_ramas[centro_izq] = "┌"
        fila_ramas[centro_der] = "┐"
        fila_ramas[raiz] = "┴"
        fila_bits[centro_izq] = "0"
        fila_bits[centro_der] = "1"

        fila_etiqueta = [" "] * (ancho + corrimiento + relleno)
        for k, ch in enumerate(etiqueta):
            fila_etiqueta[inicio + corrimiento + k] = ch

        hijos = []
        for k in range(max(len(izq), len(der))):
            a = izq[k] if k < len(izq) else " " * ancho_izq
            b = der[k] if k < len(der) else " " * ancho_der
            hijos.append(a + " " * separacion + b)

        cuerpo = ["".join(fila_ramas), "".join(fila_bits)] + hijos
        cuerpo = [" " * corrimiento + l + " " * relleno for l in cuerpo]
        lineas = ["".join(fila_etiqueta)] + cuerpo
        return lineas, ancho + corrimiento + relleno, raiz + corrimiento

    if len(codigos) == 1:
        lineas, _, _ = bloque(codigos[0])
    else:
        lineas, _, _ = bloque("")
    return "\n".join(l.rstrip() for l in lineas)


# ---------------------------------------------------------------------------
# Ejercicio 6: decodificación de una cadena con cualquier alfabeto código
# ---------------------------------------------------------------------------
def decodificar_cadena(mensaje, simbolos, codigos):
    """
    Qué es:
        Decodifica un mensaje escrito con las palabras de un código
        instantáneo (en cualquier alfabeto código: binario, {A, B, C}, etc.)
        y devuelve la secuencia de símbolos de la fuente.

    Para qué se usa:
        Para el ejercicio 6, donde el código del TP4 usa el alfabeto
        {A, B, C}. También la usa internamente decodificar_mensaje.

    Cómo interpretar el resultado:
        - Devuelve una lista con un símbolo de la fuente por cada palabra
          reconocida, en orden. Para ver los símbolos juntos:
          " ".join(resultado).
        - Si el código no es instantáneo, da error: con un código así no se
          puede reconocer cada palabra apenas termina.
        - Si sobran caracteres al final que no completan ninguna palabra,
          da error: el mensaje está incompleto o tiene un error.

    Parámetros:
        mensaje: string codificado.
        simbolos: símbolos de la fuente (string o lista), paralelos a codigos.
        codigos: palabras código.
    Devuelve:
        list.

    Ejemplo (ejercicio 6a):
        >>> decodificar_cadena("ABACBAACABABAACBABA",
        ...                    ["S1", "S2", "S3", "S4"], ["BA", "CAB", "A", "CBA"])
        ['S3', 'S1', 'S4', 'S3', 'S2', 'S3', 'S1', 'S3', 'S4', 'S1']
    """
    if len(simbolos) != len(codigos):
        raise ValueError("simbolos y codigos deben tener la misma cantidad de elementos.")
    if not es_instantaneo(list(codigos)):
        raise ValueError("El código no es instantáneo: no se puede decodificar palabra a palabra.")

    tabla = {c: s for s, c in zip(simbolos, codigos)}
    resultado = []
    actual = ""
    for caracter in mensaje:
        actual += caracter
        if actual in tabla:
            resultado.append(tabla[actual])
            actual = ""
    if actual:
        raise ValueError(f"Sobran símbolos al final que no forman una palabra código: '{actual}'.")
    return resultado


# ---------------------------------------------------------------------------
# Ejercicio 7: codificar y decodificar a bytes
# ---------------------------------------------------------------------------
def codificar_mensaje(mensaje, alfabeto, codigos, cabecera=True):
    """
    Qué es:
        Comprime un mensaje: reemplaza cada carácter por su palabra código
        binaria y empaqueta la secuencia de bits resultante en bytes.

        Formato del bytearray:
          - Byte 0 (solo si cabecera=True): cantidad de bits de relleno
            (0 a 7) agregados al final para completar el último byte.
          - Bytes siguientes: los bits del mensaje codificado, 8 por byte.

    Para qué se usa:
        Para obtener el mensaje comprimido "real" que se guarda en un archivo
        o se transmite (ejercicios 7a y 9).

    Cómo interpretar el resultado:
        - Su tamaño en bytes es lo que ocupa el mensaje comprimido; se
          compara con el original usando tasa_compresion.
        - Cuanto más corta sea la longitud media del código, menos bytes
          ocupa.
        - El byte de cabecera es necesario para que al decodificar no se
          tomen los ceros de relleno como palabras del mensaje.
        - EN EL PARCIAL usar cabecera=False (o directamente
          tasa_compresion_codigo): la aclaración dice que el comprimido debe
          contener únicamente los códigos de los símbolos.
        - Para recuperar el texto se necesitan el mismo alfabeto y el mismo
          código (por ejemplo, la tabla del ejercicio 9 + la misma función).

    Parámetros:
        mensaje: string escrito con caracteres del alfabeto.
        alfabeto: string o lista con los símbolos de la fuente, paralelo a codigos.
        codigos: lista de palabras binarias (strings de '0' y '1').
        cabecera: si es True agrega el byte 0 con la cantidad de relleno.
    Devuelve:
        bytearray.
    """
    if len(alfabeto) != len(codigos):
        raise ValueError("alfabeto y codigos deben tener la misma cantidad de elementos.")
    tabla = {s: c for s, c in zip(alfabeto, codigos)}
    faltan = sorted(set(mensaje) - set(tabla))
    if faltan:
        raise ValueError(f"Caracteres que no están en el alfabeto: {faltan}")

    bits = "".join(tabla[c] for c in mensaje)
    relleno = (8 - len(bits) % 8) % 8
    bits += "0" * relleno
    datos = [int(bits[i:i + 8], 2) for i in range(0, len(bits), 8)]
    return bytearray(([relleno] if cabecera else []) + datos)


def decodificar_mensaje(secuencia, alfabeto, codigos):
    """
    Qué es:
        Descomprime una secuencia de bytes generada con codificar_mensaje
        (con cabecera=True) y devuelve el mensaje original.

    Para qué se usa:
        Para recuperar el texto a partir del archivo o la transmisión
        comprimida (ejercicios 7b y 9).

    Cómo interpretar el resultado:
        - Devuelve exactamente el mensaje original: es compresión sin
          pérdida.
        - Si da error, los bytes no corresponden a ese alfabeto y código (o
          se dañaron): sobran bits que no forman ninguna palabra.
        - Si el código usado no es el mismo que al comprimir, puede salir un
          texto distinto sin dar error.

    Parámetros:
        secuencia: bytes o bytearray con el formato de codificar_mensaje.
        alfabeto: string o lista con los símbolos de la fuente.
        codigos: lista de palabras binarias, paralela al alfabeto.
    Devuelve:
        str.
    """
    if len(secuencia) == 0:
        return ""
    relleno = secuencia[0]
    bits = "".join(format(b, "08b") for b in secuencia[1:])
    if relleno:
        bits = bits[:-relleno]
    return "".join(decodificar_cadena(bits, list(alfabeto), codigos))


# ---------------------------------------------------------------------------
# Ejercicio 8: tasa de compresión
# ---------------------------------------------------------------------------
def tasa_compresion(mensaje, comprimido, como_fraccion=False):
    """
    Qué es:
        Tasa de compresión = tamaño original / tamaño comprimido. El tamaño
        original se toma como 1 byte por carácter del mensaje (ASCII).

    Para qué se usa:
        Para medir cuánto se achicó un mensaje al comprimirlo con Huffman,
        Shannon-Fano o RLC (ejercicios 8, 9 y 12).

    Cómo interpretar el resultado:
        - Se lee como "N:1": el original ocupa N veces lo que ocupa el
          comprimido. Por ejemplo, 4/3 significa 4:3, unos 1.33:1.
        - Mayor que 1: hubo compresión. Cuanto más grande, mejor.
        - Igual a 1: el comprimido ocupa lo mismo que el original.
        - Menor que 1: el "comprimido" ocupa más que el original (pasa con
          RLC sobre textos sin repeticiones seguidas).
        - Ojo: si 'comprimido' tiene el byte de cabecera de
          codificar_mensaje, ese byte también cuenta. Para el parcial usar
          tasa_compresion_codigo.

    Parámetros:
        mensaje: string original.
        comprimido: bytes o bytearray con el mensaje comprimido.
        como_fraccion: si es True devuelve un string simplificado, como "4/3"
                       (el formato de los resultados de la guía).
    Devuelve:
        float, o str si como_fraccion es True.
    """
    original = len(mensaje)
    final = len(comprimido)
    if final == 0:
        raise ValueError("La secuencia comprimida está vacía.")
    if como_fraccion:
        d = math.gcd(original, final)
        return f"{original // d}/{final // d}"
    return original / final


def tasa_compresion_codigo(mensaje, alfabeto, codigos):
    """
    Qué es:
        Tasa de compresión de un mensaje codificado con un código binario,
        SIN agregar nada además de las palabras código (es lo que pide la
        aclaración del parcial: "no incluir ningún tipo de redundancia
        adicional"):

            tasa = (8 bits * cantidad de caracteres) / (bytes comprimidos * 8)

        El original ocupa 1 byte (ASCII) por carácter; el comprimido ocupa
        los bits del mensaje codificado, redondeados hacia arriba a bytes
        enteros.

    Para qué se usa:
        Ejercicio 1 del parcial: "Determinar la tasa de compresión que se
        obtiene codificando el mensaje". En el parcial 2025 daba 4 (se
        escribe 4:1).

    Cómo interpretar el resultado:
        - Se lee "N:1": el original ocupa N veces lo que ocupa el
          comprimido. 4 -> el mensaje comprimido ocupa la cuarta parte.
        - Aproximadamente vale 8 / L (8 bits ASCII contra L binits por
          símbolo): cuanto menor la longitud media, mayor la tasa.
        - Mayor que 1: comprime. Menor que 1: agranda (no debería pasar
          con Huffman sobre texto ASCII).

    Parámetros:
        mensaje: string original.
        alfabeto: lista o string con los símbolos, paralela a codigos.
        codigos: palabras binarias.
    Devuelve:
        float.
    """
    return tasa_compresion(mensaje, codificar_mensaje(mensaje, alfabeto, codigos, cabecera=False))


# ---------------------------------------------------------------------------
# Ejercicio 9: archivos binarios
# ---------------------------------------------------------------------------
def guardar_binario(ruta, datos):
    """
    Qué es:
        Guarda una secuencia de bytes en un archivo binario.

    Para qué se usa:
        Para el ejercicio 9: guardar el mensaje comprimido y enviárselo a un
        compañero.

    Cómo interpretar el resultado:
        - Devuelve la cantidad de bytes escritos, que es el tamaño del
          archivo y coincide con len(datos).
        - Ese tamaño es el "tamaño comprimido" de la tasa de compresión.

    Parámetros:
        ruta: nombre o ruta del archivo (por ejemplo "mensaje.bin").
        datos: bytes o bytearray.
    Devuelve:
        int.
    """
    with open(ruta, "wb") as archivo:
        return archivo.write(bytes(datos))


def leer_binario(ruta):
    """
    Qué es:
        Lee un archivo binario completo y devuelve su contenido como
        bytearray.

    Para qué se usa:
        Para el ejercicio 9: leer el archivo recibido del compañero y
        pasárselo a decodificar_mensaje.

    Cómo interpretar el resultado:
        - Son los mismos bytes que se guardaron; su longitud es el tamaño del
          archivo comprimido.

    Parámetros:
        ruta: nombre o ruta del archivo.
    Devuelve:
        bytearray.
    """
    with open(ruta, "rb") as archivo:
        return bytearray(archivo.read())


# ---------------------------------------------------------------------------
# Ejercicios 10 a 12: Run Length Coding (RLC)
# ---------------------------------------------------------------------------
def _rafagas(mensaje):
    rafagas = []
    for c in mensaje:
        if rafagas and rafagas[-1][0] == c:
            rafagas[-1][1] += 1
        else:
            rafagas.append([c, 1])
    return rafagas


def rlc_texto(mensaje):
    """
    Qué es:
        Representación RLC del mensaje en texto: cada ráfaga de caracteres
        iguales consecutivos se escribe como carácter + cantidad.

    Para qué se usa:
        Para verificar a mano el ejercicio 10 (por ejemplo,
        XXXYZZZZ -> X3Y1Z4).

    Cómo interpretar el resultado:
        - Cada par carácter-número es una ráfaga.
        - Muchos pares con número 1 indican que el mensaje casi no tiene
          repeticiones seguidas y que RLC no le conviene.
        - Pocos pares con números grandes indican ráfagas largas: es donde
          RLC comprime bien (imágenes binarias, faxes).

    Parámetros:
        mensaje: string.
    Devuelve:
        str.
    """
    return "".join(f"{c}{n}" for c, n in _rafagas(mensaje))


def rlc_comprimir(mensaje):
    """
    Qué es:
        Comprime un mensaje con Run Length Coding: cada ráfaga de caracteres
        iguales consecutivos se guarda con 2 bytes, el código ASCII del
        carácter y la cantidad de repeticiones.

    Para qué se usa:
        Para el ejercicio 11 y para calcular la tasa de compresión del
        ejercicio 12.

    Cómo interpretar el resultado:
        - El bytearray tiene 2 bytes por ráfaga: (carácter, cantidad),
          (carácter, cantidad), ...
        - Comprime solo si las ráfagas tienen en promedio más de 2
          caracteres; con ráfagas de 1 carácter el resultado ocupa el doble
          que el original.
        - Una ráfaga de más de 255 caracteres se guarda como varias ráfagas,
          porque un byte llega como máximo a 255.
        - Los caracteres tienen que entrar en un byte (código menor a 256).

    Parámetros:
        mensaje: string.
    Devuelve:
        bytearray.
    """
    salida = bytearray()
    for c, n in _rafagas(mensaje):
        if ord(c) > 255:
            raise ValueError(f"El carácter {c!r} no entra en un byte.")
        while n > 0:
            parte = min(n, 255)
            salida += bytes([ord(c), parte])
            n -= parte
    return salida


def rlc_descomprimir(secuencia):
    """
    Qué es:
        Descomprime una secuencia generada con rlc_comprimir.

    Para qué se usa:
        Para comprobar que RLC es sin pérdida: lo que sale tiene que ser
        idéntico al mensaje original.

    Cómo interpretar el resultado:
        - Devuelve el mensaje original.
        - Si la secuencia tiene una cantidad impar de bytes, no es un RLC
          válido y da error.

    Parámetros:
        secuencia: bytes o bytearray con pares (carácter, cantidad).
    Devuelve:
        str.
    """
    if len(secuencia) % 2:
        raise ValueError("Una secuencia RLC debe tener una cantidad par de bytes.")
    return "".join(chr(secuencia[i]) * secuencia[i + 1] for i in range(0, len(secuencia), 2))
