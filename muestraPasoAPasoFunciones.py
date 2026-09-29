"""Versiones didácticas de las funciones del proyecto.

Todas muestran el desarrollo por defecto y conservan el tipo de resultado de
las funciones originales. Pasar mostrar=False permite ocultar la explicación.
La convención de las matrices es matriz[destino][origen]: suman las columnas.

Uso:
    import muestraPasoAPasoFunciones as pasos
    pasos.es_univocamente_decodificable(["0", "01", "10"])
    pasos.generaVectorEstacionario([[0.4, 0.75], [0.6, 0.25]], 2)

Ejecutar este archivo directamente muestra ejemplos. Importarlo no imprime.
"""

import math


def _imprimir(mostrar, mensaje):
    if mostrar:
        print(mensaje)


def _mostrar_matriz(matriz, alfabeto, mostrar):
    if mostrar:
        print("  destino / origen:", [repr(s) for s in alfabeto])
        for simbolo, fila in zip(alfabeto, matriz):
            print(f"  {simbolo!r}: {fila}")


def _validar_matriz(matriz):
    n = len(matriz)
    if n == 0 or any(len(fila) != n for fila in matriz):
        raise ValueError("La matriz de transicion debe ser cuadrada y no vacia.")
    for origen in range(n):
        columna = [matriz[destino][origen] for destino in range(n)]
        if any(p < 0 or p > 1 for p in columna):
            raise ValueError("Las probabilidades deben estar entre 0 y 1.")
        if not math.isclose(sum(columna), 1.0, rel_tol=1e-9, abs_tol=1e-9):
            raise ValueError("Las probabilidades de cada columna deben sumar 1.")
    return n


def generaalfabetoyTransicion(cadena, mostrar=True):
    """Muestra cada par, sus conteos y la normalización por origen.

    Devuelve (alfabeto, matriz). Cada símbolo debe tener una transición de
    salida observada; de lo contrario no puede estimarse su columna.
    """
    _imprimir(mostrar, "\nMATRIZ DE TRANSICION")
    alfabeto = sorted(set(cadena))
    n = len(alfabeto)
    indices = {simbolo: i for i, simbolo in enumerate(alfabeto)}
    matriz = [[0 for _ in range(n)] for _ in range(n)]
    _imprimir(mostrar, f"Alfabeto ordenado: {alfabeto}")
    _imprimir(mostrar, "Convencion: fila = destino; columna = origen.")
    for k in range(len(cadena) - 1):
        origen, destino = cadena[k], cadena[k + 1]
        i, j = indices[destino], indices[origen]
        matriz[i][j] += 1
        _imprimir(
            mostrar,
            f"Par {k + 1}: {origen!r} -> {destino!r}; "
            f"conteo[{i}][{j}] = {matriz[i][j]}",
        )
    _imprimir(mostrar, "Matriz de conteos:")
    _mostrar_matriz(matriz, alfabeto, mostrar)
    for j, origen in enumerate(alfabeto):
        total = sum(matriz[i][j] for i in range(n))
        _imprimir(mostrar, f"Total de salidas desde {origen!r}: {total}")
        if total == 0:
            raise ValueError(
                f"No se observaron salidas desde {origen!r}; "
                "no puede estimarse su distribucion de transicion."
            )
        for i, destino in enumerate(alfabeto):
            conteo = matriz[i][j]
            matriz[i][j] = conteo / total
            _imprimir(
                mostrar,
                f"  P({destino!r} | {origen!r}) = "
                f"{conteo}/{total} = {matriz[i][j]:.12g}",
            )
    _imprimir(mostrar, "Matriz de probabilidades:")
    _mostrar_matriz(matriz, alfabeto, mostrar)
    return alfabeto, matriz


def generaVectorEstacionario(matriz, n, mostrar=True):
    """Muestra las 30 iteraciones originales y comprueba el residuo final.

    Devuelve la misma aproximación que la función original. No interrumpe
    antes las iteraciones ni supone que 30 pasos garanticen convergencia.
    """
    if _validar_matriz(matriz) != n:
        raise ValueError("n debe coincidir con el numero de estados de la matriz.")
    _imprimir(mostrar, "\nVECTOR ESTACIONARIO")
    pi = [1 / n] * n
    _imprimir(mostrar, f"Vector inicial pi(0) = {pi}")
    _imprimir(mostrar, "Regla: pi_nuevo[j] = suma_i pi[i] * matriz[j][i].")
    for k in range(30):
        nuevo = [0] * n
        _imprimir(mostrar, f"Iteracion {k + 1}:")
        for j in range(n):
            suma = 0
            terminos = []
            for i in range(n):
                suma += pi[i] * matriz[j][i]
                terminos.append(f"({pi[i]:.12g} * {matriz[j][i]:.12g})")
            nuevo[j] = suma
            _imprimir(mostrar, f"  pi[{j}] = {' + '.join(terminos)} = {suma:.12g}")
        diferencia = max(abs(a - b) for a, b in zip(nuevo, pi))
        pi = nuevo.copy()
        _imprimir(mostrar, f"  Vector: {pi}; cambio maximo = {diferencia:.12g}")
    producto = [sum(pi[i] * matriz[j][i] for i in range(n)) for j in range(n)]
    residuo = max(abs(a - b) for a, b in zip(producto, pi))
    _imprimir(mostrar, f"Resultado tras 30 iteraciones: {pi}")
    _imprimir(mostrar, f"Suma del vector: {sum(pi):.12g}")
    _imprimir(mostrar, f"M * pi = {producto}")
    _imprimir(mostrar, f"Residuo maximo |M*pi - pi| = {residuo:.12g}")
    _imprimir(
        mostrar,
        "Cumple M*pi aproximadamente igual a pi con tolerancia 1e-9."
        if residuo <= 1e-9
        else "No cumple la comprobacion con tolerancia 1e-9; la aproximacion requiere revision.",
    )
    return pi


def tieneMemoriaNoNula(matriz, tolerancia, mostrar=True):
    """Muestra las comparaciones contra la diagonal y la tolerancia usada."""
    _validar_matriz(matriz)
    if tolerancia < 0:
        raise ValueError("La tolerancia no puede ser negativa.")
    _imprimir(mostrar, "\nMEMORIA DE LA FUENTE")
    _imprimir(mostrar, f"Tolerancia: {tolerancia}")
    for i in range(len(matriz)):
        referencia = matriz[i][i]
        for j in range(len(matriz)):
            diferencia = abs(matriz[i][j] - referencia)
            _imprimir(
                mostrar,
                f"Fila {i}, columna {j}: |{matriz[i][j]:.12g} - "
                f"{referencia:.12g}| = {diferencia:.12g}; "
                f"supera la tolerancia: {diferencia > tolerancia}",
            )
            if diferencia > tolerancia:
                _imprimir(mostrar, "Resultado: fuente CON memoria segun la tolerancia utilizada.")
                return True
    _imprimir(mostrar, "Resultado: memoria NULA segun la tolerancia utilizada.")
    return False


def es_noSingular(codigo, mostrar=True):
    """Muestra las palabras distintas y las repeticiones."""
    vistas = set()
    repetidas = set()
    for palabra in codigo:
        if palabra in vistas:
            repetidas.add(palabra)
        vistas.add(palabra)
    _imprimir(mostrar, f"Palabras: {list(codigo)}")
    _imprimir(mostrar, f"Total: {len(codigo)}; distintas: {len(vistas)}")
    _imprimir(mostrar, f"Palabras repetidas: {sorted(repetidas)}")
    resultado = len(codigo) == len(vistas)
    _imprimir(mostrar, f"Codigo no singular: {resultado}")
    return resultado


def es_instantaneo(palabras, mostrar=True):
    """Muestra cada comparación de prefijos hasta encontrar una o agotar pares."""
    _imprimir(mostrar, "\nCODIGO INSTANTANEO")
    for i, prefijo in enumerate(palabras):
        for j, palabra in enumerate(palabras):
            if i == j:
                continue
            coincide = palabra.startswith(prefijo)
            _imprimir(mostrar, f"¿{prefijo!r} es prefijo de {palabra!r}? {coincide}")
            if coincide:
                _imprimir(mostrar, "Resultado: NO es instantaneo.")
                return False
    _imprimir(mostrar, "Ninguna palabra es prefijo de otra: es instantaneo.")
    return True


def calcular_restos(conjunto_a, conjunto_b, mostrar=True):
    """Muestra los prefijos propios encontrados y devuelve los restos no vacíos."""
    restos = set()
    for a in sorted(conjunto_a):
        for b in sorted(conjunto_b):
            if a != b and b.startswith(a):
                resto = b[len(a):]
                restos.add(resto)
                _imprimir(mostrar, f"  {b!r} = {a!r} + {resto!r}; resto: {resto!r}")
    _imprimir(mostrar, f"  Restos obtenidos: {sorted(restos) if restos else 'vacio'}")
    return restos


def es_univocamente_decodificable(palabras, mostrar=True):
    """Muestra Sardinas–Patterson, los prefijos que generan cada C_i y el corte."""
    _imprimir(mostrar, "\nSARDINAS-PATTERSON")
    if not es_noSingular(palabras, mostrar):
        _imprimir(mostrar, "Hay palabras repetidas: NO es univoco.")
        return False
    originales = set(palabras)
    if "" in originales:
        _imprimir(mostrar, "Hay una palabra vacia: NO es univoco.")
        return False
    _imprimir(mostrar, "Paso 1: comparar las palabras originales entre si.")
    actual = calcular_restos(originales, originales, mostrar)
    historial = [actual]
    n = 1
    while True:
        _imprimir(mostrar, f"C{n} = {sorted(actual) if actual else 'vacio'}")
        colisiones = actual & originales
        if colisiones:
            _imprimir(mostrar, f"C{n} contiene palabras del codigo: {sorted(colisiones)}.")
            _imprimir(mostrar, "Resultado: NO es univocamente decodificable.")
            return False
        if not actual:
            _imprimir(mostrar, "No quedan restos: es univocamente decodificable.")
            return True
        _imprimir(mostrar, f"Paso {n + 1}: restos de C{n} como prefijos de palabras originales.")
        primera_direccion = calcular_restos(actual, originales, mostrar)
        _imprimir(mostrar, f"Paso {n + 1}: palabras originales como prefijos de restos de C{n}.")
        segunda_direccion = calcular_restos(originales, actual, mostrar)
        siguiente = primera_direccion | segunda_direccion
        if siguiente in historial:
            anterior = historial.index(siguiente) + 1
            _imprimir(mostrar, f"C{n + 1} = {sorted(siguiente)} = C{anterior}.")
            _imprimir(mostrar, "Se repite un conjunto sin colision: es univocamente decodificable.")
            return True
        historial.append(siguiente)
        actual = siguiente
        n += 1


def es_compacto(palabras, probabilidades, mostrar=True):
    """Muestra univocidad y longitud <= techo(log_r(1/p)), como en el proyecto.

    Aplica el criterio de la función original; no construye ni compara códigos
    alternativos para comprobar optimalidad global.
    """
    _imprimir(mostrar, "\nCOMPACIDAD: CRITERIO IMPLEMENTADO EN EL PROYECTO")
    if len(palabras) != len(probabilidades):
        raise ValueError("Debe haber una probabilidad por cada palabra.")
    if not es_univocamente_decodificable(palabras, mostrar):
        _imprimir(mostrar, "Resultado: NO es compacto porque no es univoco.")
        return False
    base = len(set("".join(palabras)))
    _imprimir(mostrar, f"Alfabeto codigo: {sorted(set(''.join(palabras)))}; base r = {base}")
    if palabras and base < 2:
        raise ValueError("El criterio logaritmico requiere una base r mayor que 1.")
    for palabra, p in zip(palabras, probabilidades):
        if not 0 < p <= 1:
            raise ValueError("Las probabilidades deben estar en el intervalo (0, 1].")
        informacion = math.log(1 / p, base)
        tope = math.ceil(informacion)
        cumple = len(palabra) <= tope
        _imprimir(
            mostrar,
            f"Palabra {palabra!r}, p = {p}: log_{base}(1/p) = {informacion:.12g}; "
            f"techo = {tope}; longitud = {len(palabra)}; cumple: {cumple}",
        )
        if not cumple:
            _imprimir(mostrar, "Resultado: NO es compacto; esta palabra supera el tope.")
            return False
    _imprimir(mostrar, "Resultado: es compacto segun el criterio implementado.")
    return True


def esFuenteErgodica(matriz, mostrar=True):
    """Muestra alcanzabilidad, distancias y cálculo del período mediante MCD.

    Como la función original, exige irreducibilidad y aperiodicidad.
    """
    n = _validar_matriz(matriz)
    _imprimir(mostrar, "\nERGODICIDAD")
    _imprimir(mostrar, "Matriz valida: cuadrada, probabilidades validas y columnas que suman 1.")
    aristas = [(i, j) for i in range(n) for j in range(n) if matriz[j][i] > 0]
    _imprimir(mostrar, f"Transiciones posibles (origen, destino): {aristas}")

    def alcanzables(invertir=False):
        visitados = {0}
        pendientes = [0]
        _imprimir(mostrar, f"Recorrido {'inverso' if invertir else 'normal'} desde el estado 0:")
        for actual in pendientes:
            _imprimir(mostrar, f"  Visitar estado {actual}.")
            for estado in range(n):
                probabilidad = matriz[actual][estado] if invertir else matriz[estado][actual]
                if probabilidad > 0 and estado not in visitados:
                    visitados.add(estado)
                    pendientes.append(estado)
                    _imprimir(mostrar, f"  Se alcanza {estado} desde {actual}; pendientes: {pendientes}")
        _imprimir(mostrar, f"  Estados alcanzados: {sorted(visitados)}")
        return len(visitados) == n

    if not alcanzables() or not alcanzables(invertir=True):
        _imprimir(mostrar, "No todos los estados se comunican: NO es irreducible ni ergodica.")
        return False
    _imprimir(mostrar, "Todos los estados se comunican: la cadena es irreducible.")
    distancias = [-1] * n
    distancias[0] = 0
    pendientes = [0]
    for origen in pendientes:
        for destino in range(n):
            if matriz[destino][origen] > 0 and distancias[destino] == -1:
                distancias[destino] = distancias[origen] + 1
                pendientes.append(destino)
                _imprimir(mostrar, f"Distancia a {destino}: {distancias[destino]} (desde {origen}).")
    _imprimir(mostrar, f"Distancias desde el estado 0: {distancias}")
    periodo = 0
    for origen, destino in aristas:
        diferencia = distancias[origen] + 1 - distancias[destino]
        anterior = periodo
        periodo = math.gcd(periodo, abs(diferencia))
        _imprimir(
            mostrar,
            f"Arista {origen} -> {destino}: d[{origen}] + 1 - d[{destino}] "
            f"= {diferencia}; MCD({anterior}, {abs(diferencia)}) = {periodo}",
        )
    _imprimir(mostrar, f"Periodo de la cadena: {periodo}")
    resultado = periodo == 1
    _imprimir(
        mostrar,
        "Es irreducible y aperiodica: ES ergodica."
        if resultado else "El periodo es mayor que 1: NO es ergodica segun este criterio.",
    )
    return resultado


if __name__ == "__main__":
    cadena = "AABAABBABA"
    print(f"Ejemplo de fuente: {cadena!r}")
    alfabeto, matriz = generaalfabetoyTransicion(cadena)
    tieneMemoriaNoNula(matriz, 0.01)
    esFuenteErgodica(matriz)
    generaVectorEstacionario(matriz, len(alfabeto))

    codigo_a = ["/+", "*", "+-", "-", "*/"]
    codigo_b = ["(]", "]", "[)", ")", "(["]
    probabilidades = [0.15, 0.25, 0.05, 0.45, 0.10]
    print(f"\nEjemplo de codigo A: {codigo_a}")
    es_instantaneo(codigo_a)
    es_univocamente_decodificable(codigo_a)
    print(f"\nEjemplo de codigo B: {codigo_b}")
    es_instantaneo(codigo_b)
    es_compacto(codigo_b, probabilidades)
