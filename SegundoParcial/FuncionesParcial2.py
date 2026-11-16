"""
FuncionesParcial2.py
====================
TODAS las funciones para el segundo parcial en un solo archivo:
  1. Formulas.py              (entropía, extensiones, alfabeto y probabilidades)
  2. FormulasCodificacion.py  (instantáneo, Kraft, longitud media, ...)
  3. Func_clase4.py           (Huffman, Shannon-Fano, Primer Teorema, rendimiento,
                               Hamming, Levenshtein, paridad VRC/LRC/cruzada)
  4. Func_clase5.py           (alfabeto y probabilidades de un mensaje, resumen de un
                               código, tasa de compresión, RLC, codificar/decodificar)
  5. Func_clase6.py           (canal desde secuencias, entropías del canal,
                               información mutua, reducciones, capacidad, P_E)

Uso:   from FuncionesParcial2 import *
Para interpretar los resultados: Explicaciones.py (explicar(funcion, args...)).
Solo usa las librerías math y random.
"""

import math
import random



# ############################################################################
# Formulas.py (tuyo, TP1-TP3)
# ############################################################################

def CalcInfo (fdp): #dado una lista de probabilidades genera una lista con la informacion obtenida en bits
    """
    Algoritmo: calcula la cantidad de información asociada a cada suceso como
    el logaritmo en base 2 del inverso de su probabilidad.

    Interpretación del resultado: devuelve una lista medida en bits. Un valor
    alto corresponde a un suceso poco probable y sorpresivo; un valor bajo
    corresponde a un suceso frecuente y predecible.
    """
    return [math.log2(1/p) for p in fdp]

def CalcEntropia (fdp): #dado una lista de probabilidades devuelve la entropia
    """
    Algoritmo: obtiene la información de cada suceso y calcula su promedio
    ponderado usando como pesos las probabilidades de la fuente.

    Interpretación del resultado: devuelve la entropía en bits por símbolo.
    Una entropía baja indica una fuente muy predecible; una entropía alta
    indica mayor incertidumbre. El máximo se alcanza con sucesos equiprobables.
    """
    return sum([p*math.log2(1/p) for p in fdp if p > 0])



#CADENAS
def GeneraAlfabetoYProb (cadena): #dado una cadena de caracteres, devuelve dos listas paralelas de alfabeto
    """
    Algoritmo: identifica, en orden de aparición, los caracteres distintos de
    una cadena (excepto el espacio) y estima la probabilidad de cada uno como
    su frecuencia dividida por la longitud total de la cadena.

    Interpretación del resultado: devuelve el alfabeto y una lista paralela de
    probabilidades. Como los espacios cuentan en la longitud pero no se incluyen
    en el alfabeto, las probabilidades pueden sumar menos que uno.
    """
    long = len(cadena)
    alfabeto = []                 #y otra con la probabilidad de ocurrencia de cada caracter de la lista alfabeto
    probabilidades = []
    for c in cadena:
        if c not in alfabeto and c != ' ':
            alfabeto.append(c)
            probabilidades.append(cadena.count(c)/long)

    pares = sorted(zip(alfabeto, probabilidades))

    alfabeto = [simbolo for simbolo, probabilidad in pares]

    probabilidades = [probabilidad for simbolo, probabilidad in pares]

    return alfabeto, probabilidades

def GeneraPalabra (N, alfabeto, probabilidades):  #dado un int, un array alfabeto y un array paralelo con 
    """
    Algoritmo: transforma las probabilidades en intervalos acumulados y, para
    cada una de las N posiciones, genera un número aleatorio que selecciona el
    símbolo cuyo intervalo lo contiene.

    Interpretación del resultado: devuelve una palabra aleatoria de longitud N.
    Al generar muchas palabras, la frecuencia de cada símbolo debería acercarse
    a su probabilidad; una palabra individual puede desviarse por azar.
    """
    fdp = [probabilidades[0]]                     #las probabilidades de cada caracter, retorna una palabra
    lista_pal = []                                #generada segun las probabilidades
    Nalfab = len(alfabeto)
    for i in range(1,len(probabilidades)):
        fdp.append(fdp[i-1] + probabilidades[i])

    for i in range(N):
        r = random.random()
        j=0
        while (r >= fdp[j]):
            j+=1
        lista_pal.append(alfabeto[j])

    palabra = "".join(lista_pal)
    return palabra

def Equiprobables (cant): #dada la cantidad de sucesos equiprobables calcula la entropia
    """
    Algoritmo: calcula el logaritmo en base 2 de la cantidad de sucesos, que es
    la entropía de una fuente donde todos tienen la misma probabilidad.

    Interpretación del resultado: devuelve bits por símbolo. Un valor mayor
    significa más alternativas igualmente posibles y más incertidumbre; con un
    único suceso el resultado es cero.
    """
    return math.log2(cant)

def DevuelveExtyFdp (alfabeto, fdp, N): #Dado un alfabeto, una lista de probabilidades y un orden N devuelve una lista de extension N y su distribucion de probabilidades
    """
    Algoritmo: construye recursivamente la extensión de orden N de una fuente.
    Combina cada secuencia de orden N-1 con cada símbolo original y obtiene la
    probabilidad conjunta multiplicando probabilidades, suponiendo independencia.

    Interpretación del resultado: devuelve dos listas paralelas con todas las
    secuencias posibles de longitud N y sus probabilidades. Si la distribución
    original suma uno, la distribución extendida también debería hacerlo.
    """
    if N==1:
        return alfabeto.copy(),fdp.copy()

    ant_alf, ant_fdp = DevuelveExtyFdp(alfabeto, fdp, N-1)

    nuevo_alf = []
    nuevo_fdp = []

    for s1,p1 in zip(ant_alf,ant_fdp):
        for s2,p2 in zip(alfabeto, fdp):
            nuevo_alf.append(s1+s2)
            nuevo_fdp.append(p1*p2)

    return nuevo_alf, nuevo_fdp

def CalculaEntropiaMemoriaBinaria (w): #calcula entropia memoria binaria pasandole w
    """
    Algoritmo: modela dos alternativas con probabilidades w y 1-w y calcula la
    entropía binaria de esa distribución.

    Interpretación del resultado: para 0 < w < 1 devuelve hasta 1 bit; se acerca
    a 0 cuando una alternativa domina y alcanza 1 cuando ambas son equiprobables
    (w = 0.5). Aunque teóricamente los extremos valen 0, esta implementación
    requiere probabilidades estrictamente mayores que cero.
    """
    prob = [w, 1-w]
    return CalcEntropia(prob)

def generaalfabetoyTransicion(cadena):  #genera el alfabeto y la matriz de transicion con todas las probabilidades de pasar de un estado de origen a uno de llegada, considera probabilidades degun el simbolo anterior
    """
    Algoritmo: extrae los símbolos distintos y cuenta cada par consecutivo de
    la cadena. Luego normaliza los conteos por símbolo de origen para estimar
    las probabilidades condicionales del siguiente símbolo.

    Interpretación del resultado: devuelve el alfabeto y una matriz en la que
    la columna representa el símbolo actual y la fila el siguiente. Cada celda
    es la probabilidad estimada de esa transición; valores altos indican que la
    transición observada es frecuente.
    """
    alfabeto = []
    mat =[]
    for i in range(len(cadena)):
        if cadena[i] not in alfabeto:
            alfabeto.append(cadena[i]);
    alfabeto = sorted(alfabeto)
    n=len(alfabeto);
    mat=[[0 for i in range(n)] for j in range(n)]
    for k in range (len(cadena)-1):
        mat[alfabeto.index(cadena[k+1])][alfabeto.index(cadena[k])] += 1
    #divido matriz
    for j in range (n):
        total_columna = sum(mat[i][j] for i in range(n))
        for i in range (n):
            mat[i][j] = mat[i][j]/total_columna

    return alfabeto, mat 
#CALCULA VECTOR ESTACIONARIO

def transponer(matriz):
    return [list(fila) for fila in zip(*matriz)]
    
def generaVectorEstacionario(matriz,n): 
    pi = [1/n] * n
    for k in range(50):          # con 10 no llega a estabilizarse del todo, con 30 si
        piNuevo = [0] * n
        for j in range(n):                  # j = estado DESTINO
            suma = 0
            for i in range(n):              # i = estado ORIGEN
                suma += pi[i] * matriz[j][i]  # matriz[destino][origen]
            piNuevo[j] = suma
        pi = piNuevo.copy()
    return pi



def calculaInfoCondicional(probabilidad):
    """
    Calcula la información aportada por un símbolo cuando se conoce el estado
    anterior de la fuente:

        I(s_i / estado) = log2(1 / P(s_i / estado))

    La probabilidad recibida debe ser estrictamente mayor que cero y menor o
    igual que uno. El resultado se expresa en bits.
    """
    if probabilidad <= 0 or probabilidad > 1:
        raise ValueError("La probabilidad condicional debe estar en el intervalo (0, 1].")

    return math.log2(1 / probabilidad)


def calculaEntropiaMarkovOrden1(matriz, vector_estacionario=None):
    """
    Calcula la entropía por símbolo de una fuente de Markov de orden 1:

        H1 = sum_i p_i* sum_j p(j/i) log2(1 / p(j/i))

    Sigue la convención usada por ``generaalfabetoyTransicion``:
    ``matriz[destino][origen]`` representa P(destino/origen).

    Si no se proporciona el vector estacionario, se aproxima mediante
    ``generaVectorEstacionario``. Las transiciones de probabilidad cero no
    aportan a la entropía.
    """
    n = len(matriz)
    if n == 0 or any(len(fila) != n for fila in matriz):
        raise ValueError("La matriz de transición debe ser cuadrada y no vacía.")

    for origen in range(n):
        probabilidades = [matriz[destino][origen] for destino in range(n)]
        if any(p < 0 or p > 1 for p in probabilidades):
            raise ValueError("Las probabilidades de transición deben estar entre 0 y 1.")
        if not math.isclose(sum(probabilidades), 1.0, rel_tol=1e-9, abs_tol=1e-9):
            raise ValueError("Las probabilidades de cada estado de origen deben sumar 1.")

    if vector_estacionario is None:
        vector_estacionario = generaVectorEstacionario(matriz, n)

    if len(vector_estacionario) != n:
        raise ValueError("El vector estacionario debe tener una probabilidad por estado.")
    if any(p < 0 or p > 1 for p in vector_estacionario):
        raise ValueError("Las probabilidades estacionarias deben estar entre 0 y 1.")
    if not math.isclose(sum(vector_estacionario), 1.0, rel_tol=1e-9, abs_tol=1e-9):
        raise ValueError("Las probabilidades del vector estacionario deben sumar 1.")

    entropia = 0
    for origen, prob_estado in enumerate(vector_estacionario):
        probabilidades_salida = [matriz[destino][origen] for destino in range(n)]
        entropia += prob_estado * sum(
            p * math.log2(1 / p) for p in probabilidades_salida if p > 0
        )

    return entropia


def calculaEntropiaMarkovOrdenM(probabilidades_estados, probabilidades_condicionales):
    """
    Calcula la entropía de una fuente de Markov de orden m:

        H(S) = sum_estado P(estado) H(S / estado)

    ``probabilidades_estados`` contiene P(S_j1, ..., S_jm), mientras que cada
    elemento de ``probabilidades_condicionales`` es la distribución del
    próximo símbolo para el estado correspondiente. El resultado se expresa
    en bits por símbolo.

    Se pasan dos listas paralelas:
        - La probabilidad de cada estado de memoria.
        - La distribución del siguiente símbolo para cada estado.
    """
    if len(probabilidades_estados) == 0:
        raise ValueError("Debe proporcionarse al menos un estado.")
    if len(probabilidades_estados) != len(probabilidades_condicionales):
        raise ValueError("Debe haber una distribución condicional por cada estado.")
    if any(p < 0 or p > 1 for p in probabilidades_estados):
        raise ValueError("Las probabilidades de los estados deben estar entre 0 y 1.")
    if not math.isclose(sum(probabilidades_estados), 1.0, rel_tol=1e-9, abs_tol=1e-9):
        raise ValueError("Las probabilidades de los estados deben sumar 1.")

    entropia = 0
    for prob_estado, distribucion in zip(
        probabilidades_estados, probabilidades_condicionales
    ):
        if len(distribucion) == 0:
            raise ValueError("Las distribuciones condicionales no pueden estar vacías.")
        if any(p < 0 or p > 1 for p in distribucion):
            raise ValueError("Las probabilidades condicionales deben estar entre 0 y 1.")
        if not math.isclose(sum(distribucion), 1.0, rel_tol=1e-9, abs_tol=1e-9):
            raise ValueError("Cada distribución condicional debe sumar 1.")

        entropia_condicional = sum(
            p * math.log2(1 / p) for p in distribucion if p > 0
        )
        entropia += prob_estado * entropia_condicional

    return entropia


def tieneMemoriaNoNula(matriz,tolerancia):
    """
    Algoritmo: compara, para cada fila, sus probabilidades entre columnas usando
    la entrada diagonal como referencia. Si alguna diferencia supera la
    tolerancia, considera que el estado previo influye en el siguiente.

    Interpretación del resultado: devuelve True cuando detecta memoria no nula
    según la tolerancia elegida, y False cuando la fuente puede considerarse sin
    memoria. Una tolerancia mayor admite diferencias más grandes.
    """
    tienememoria=False
    i=0
    while (i< len(matriz) and not tienememoria):
            j=0
            while (j< len(matriz) and not tienememoria):
                if (abs(matriz[i][j]-matriz[i][i]) > tolerancia):
                    tienememoria=True
                j+=1
            i+=1
    return tienememoria

def esFuenteErgodica(matriz):
    """
    Funcionamiento de la funcion: recibe una matriz de transicion con la
    convencion matriz[destino][origen]. Verifica que sea cuadrada, que sus
    probabilidades sean validas y que cada columna sume uno. Devuelve un
    booleano sin modificar la matriz recibida.

    Algoritmo: interpreta como arista toda transicion con probabilidad mayor
    que cero. Primero recorre el grafo desde el estado 0, tanto en el sentido
    normal como en el inverso; si algun estado no es alcanzable en alguno de
    los dos recorridos, la cadena no es irreducible. Si es irreducible, calcula
    distancias desde el estado 0 y obtiene el maximo comun divisor de
    distancia[origen] + 1 - distancia[destino] para todas las aristas. Ese
    maximo comun divisor es el periodo de la cadena: es aperiódica si vale 1.

    Interpretacion del resultado: True indica que la fuente es irreducible y
    aperiódica y, por lo tanto, ergodica. En una fuente finita esto implica que
    existe un unico vector estacionario y que la distribucion converge hacia
    el desde cualquier estado inicial. False indica que falla al menos una de
    esas dos condiciones.
    """
    n = len(matriz)
    if n == 0 or any(len(fila) != n for fila in matriz):
        raise ValueError("La matriz de transicion debe ser cuadrada y no vacia.")

    for origen in range(n):
        probabilidades = [matriz[destino][origen] for destino in range(n)]
        if any(p < 0 or p > 1 for p in probabilidades):
            raise ValueError("Las probabilidades de transicion deben estar entre 0 y 1.")
        if not math.isclose(sum(probabilidades), 1.0, rel_tol=1e-9, abs_tol=1e-9):
            raise ValueError("Las probabilidades de cada estado de origen deben sumar 1.")

    def estadosAlcanzables(invertirAristas=False):
        visitados = [False] * n
        pendientes = [0]
        visitados[0] = True
        siguiente = 0

        while siguiente < len(pendientes):
            actual = pendientes[siguiente]
            siguiente += 1

            for estado in range(n):
                if invertirAristas:
                    hayTransicion = matriz[actual][estado] > 0
                else:
                    hayTransicion = matriz[estado][actual] > 0

                if hayTransicion and not visitados[estado]:
                    visitados[estado] = True
                    pendientes.append(estado)

        return visitados

    if not all(estadosAlcanzables()) or not all(estadosAlcanzables(True)):
        return False

    distancias = [-1] * n
    distancias[0] = 0
    pendientes = [0]
    siguiente = 0

    while siguiente < len(pendientes):
        origen = pendientes[siguiente]
        siguiente += 1

        for destino in range(n):
            if matriz[destino][origen] > 0 and distancias[destino] == -1:
                distancias[destino] = distancias[origen] + 1
                pendientes.append(destino)

    periodo = 0
    for origen in range(n):
        for destino in range(n):
            if matriz[destino][origen] > 0:
                diferencia = distancias[origen] + 1 - distancias[destino]
                periodo = math.gcd(periodo, abs(diferencia))

    return periodo == 1


def obtenerDatosSimbolo(alfabeto, probabilidades, simbolo, *listas_paralelas):
    """
    Funcionamiento de la funcion: recibe un alfabeto, su lista paralela de
    probabilidades, un simbolo o una lista de simbolos buscados y,
    opcionalmente, cualquier cantidad de listas paralelas adicionales. Para un
    solo simbolo devuelve un solo resultado; para una lista de simbolos devuelve
    una lista de resultados en el mismo orden. Si solo se proporciona la lista
    de probabilidades, cada resultado es esa probabilidad. Si se agregan otras
    listas, cada resultado es una tupla con la probabilidad y los datos
    adicionales, respetando el orden en el que se pasaron las listas.

    Algoritmo: comprueba que todas las listas tengan la misma longitud que el
    alfabeto. Luego busca la posicion de cada simbolo solicitado y usa ese
    indice para recuperar los elementos correspondientes de todas las listas
    paralelas.

    Interpretacion del resultado: para una consulta individual, un numero
    representa la probabilidad y una tupla contiene primero la probabilidad y
    luego los valores adicionales. Para una consulta multiple se devuelve una
    lista con uno de esos resultados por cada simbolo. Si algun simbolo no
    pertenece al alfabeto, la funcion informa el error mediante ValueError.
    """
    todas_las_listas = (probabilidades,) + listas_paralelas

    for lista in todas_las_listas:
        if len(lista) != len(alfabeto):
            raise ValueError(
                "Todas las listas paralelas deben tener la misma longitud que el alfabeto."
            )

    consulta_multiple = isinstance(simbolo, (list, tuple))
    simbolos_buscados = simbolo if consulta_multiple else [simbolo]
    resultados = []

    for simbolo_buscado in simbolos_buscados:
        try:
            indice = alfabeto.index(simbolo_buscado)
        except ValueError:
            raise ValueError(
                f"El simbolo {simbolo_buscado!r} no pertenece al alfabeto."
            )

        valores = tuple(lista[indice] for lista in todas_las_listas)

        if len(valores) == 1:
            resultados.append(valores[0])
        else:
            resultados.append(valores)

    if consulta_multiple:
        return resultados

    return resultados[0]



# ############################################################################
# FormulasCodificacion.py (tuyo, TP4)
# ############################################################################

#CODIFICACION
def es_noSingular(codigo): #devuelve si un codigo es no singular
    """
    Algoritmo: compara la cantidad total de palabras código con la cantidad de
    palabras distintas para comprobar si existen repeticiones.

    Interpretación del resultado: True significa que cada símbolo fuente tiene
    una palabra código diferente; False significa que al menos dos comparten la
    misma palabra y no pueden distinguirse al decodificar.
    """
    return len(codigo) == len(set(codigo))

def es_instantaneo(palabras):
    """
    Algoritmo: compara todas las palabras entre sí y comprueba que ninguna sea
    prefijo de otra palabra más larga.

    Interpretación del resultado: True indica que el código es instantáneo y
    cada palabra puede reconocerse apenas termina; False indica que hace falta
    leer más símbolos para decidir si una palabra ya terminó.
    """
    n = len(palabras)
    for i in range(n):
        for j in range(n):
            if i != j:
                if palabras[j].startswith(palabras[i]): #En Python, "cadena_larga".startswith("cadena_corta") devuelve True si la cadena corta es efectivamente el prefijo inicial de la larga.
                    return False
    return True



def calcular_restos(conjunto_a, conjunto_b):
    """
    Compara cada elemento de conjunto_a contra cada elemento de
    conjunto_b. Si uno es prefijo del otro (y no son iguales),
    guarda el resto (la parte que sobra) en un set nuevo.
    usada para sardinas-patterson

    Algoritmo: compara las palabras de ambos conjuntos y, cuando una palabra
    del primero es prefijo de una del segundo, conserva la parte que queda
    pendiente. Estos restos se usan en el algoritmo de Sardinas-Patterson.

    Interpretación del resultado: devuelve el conjunto de sufijos no vacíos que
    todavía podrían provocar una ambigüedad. Un conjunto vacío significa que
    esta comparación no produjo restos pendientes.
    """
    restos = set()
    for a in conjunto_a:
        for b in conjunto_b:
            if a == b:
                continue
            if b.startswith(a):
                resto = b[len(a):]
                if resto:  # descartamos el resto vacio (a == b ya se filtro)
                    restos.add(resto)
    return restos

def es_univocamente_decodificable(palabras, mostrar=False):
    """
    Implementa el algoritmo de Sardinas-Patterson.

    Idea: si una palabra A es prefijo de otra palabra B, el "resto"
    de B (lo que sobra despues de sacarle el prefijo A) queda como
    una secuencia "colgando". Si ese resto eventualmente coincide
    con una palabra codigo original, significa que se puede armar
    la misma secuencia de bits/simbolos de dos formas distintas
    a partir de los simbolos fuente -> el codigo NO es univoco.

    Pasos:
      1. Calculamos C1: todos los restos que salen de comparar
         las palabras originales entre si.
      2. Iteramos generando C2, C3, ... combinando los restos
         del paso anterior con las palabras originales.
      3. Cortamos si:
         - un resto coincide con una palabra original -> NO univoco
         - el conjunto de restos queda vacio -> SI univoco
         - el conjunto de restos ya aparecio antes (ciclo) -> SI univoco

    Algoritmo: aplica Sardinas-Patterson. Genera los sufijos que quedan cuando
    una palabra es prefijo de otra y los combina sucesivamente con las palabras
    originales hasta hallar una colisión, quedarse sin restos o entrar en ciclo.

    Interpretación del resultado: True significa que toda cadena codificada
    admite una única separación en palabras código. False significa que existe
    al menos una cadena que puede decodificarse de dos maneras diferentes.

    Con mostrar=True imprime cada conjunto C1, C2, ... y la razón por la que
    termina el algoritmo. Por defecto devuelve el booleano sin imprimir.
    Las palabras repetidas o vacías hacen que el código no sea unívoco.
    """

    if not es_noSingular(palabras):
        if mostrar:
            print("   Hay palabras repetidas: el codigo es singular -> NO univoco")
        return False

    palabras_set = set(palabras)
    if "" in palabras_set:
        if mostrar:
            print("   Hay una palabra vacia -> NO univoco")
        return False

    # Paso 1: C1 = restos de comparar las palabras originales entre si
    c_actual = calcular_restos(palabras, palabras)
    historial = [c_actual]
    n = 1

    while True:
        if mostrar:
            print(f"   C{n} = {sorted(c_actual) if c_actual else 'vacio'}")

        # Condicion de NO univoco: algun resto coincide con una palabra original
        if c_actual & palabras_set:
            if mostrar:
                print(f"   C{n} contiene la palabra {sorted(c_actual & palabras_set)} -> NO univoco")
            return False

        # Condicion de SI univoco: no quedan mas restos por resolver
        if not c_actual:
            if mostrar:
                print(f"   C{n} es vacio -> univoco")
            return True

        # Generamos el siguiente conjunto de restos:
        # combinamos los restos actuales con las palabras originales
        # en ambas direcciones (resto vs palabra, y palabra vs resto)
        siguiente = calcular_restos(c_actual, palabras) | calcular_restos(palabras, c_actual)

        # Condicion de SI univoco: si este conjunto ya aparecio antes,
        # estamos en un ciclo que nunca va a generar una colision real
        if siguiente in historial:
            if mostrar:
                print(f"   C{n+1} = {sorted(siguiente)} ya aparecio antes (ciclo) -> univoco")
            return True

        historial.append(siguiente)
        c_actual = siguiente
        n += 1



def get_alfabetoCodigo(palabras):
    """
    Obtiene el alfabeto codigo utilizado por las palabras recibidas.
    Recibe una lista de palabras codigo y devuelve una cadena con sus
    caracteres sin repetir y ordenados. Agrega los caracteres a un set,
    los ordena con sorted() y los une con join().

    Algoritmo: reúne todos los símbolos usados por las palabras código, elimina
    repeticiones y los ordena para formar el alfabeto del código.

    Interpretación del resultado: devuelve una cadena con cada símbolo del
    alfabeto exactamente una vez. Su longitud es la base del código; una cadena
    vacía indica que no se recibió ningún símbolo utilizable.
    """

    #update(palabra) agrega al conjunto cada carácter de la palabra, sin repetirlos. Luego sorted() los ordena y join() los une en una cadena.

    alfabeto = set()

    for palabra in palabras:
        alfabeto.update(palabra)

    return "".join(sorted(alfabeto))


def get_longitudes(palabras):
    """
    Calcula la longitud de cada palabra codigo.
    Recibe una lista de palabras codigo y devuelve una lista de enteros.
    Usa una comprension de listas para aplicar len() a cada palabra.

    Algoritmo: determina cuántos símbolos contiene cada palabra código.

    Interpretación del resultado: devuelve una lista paralela a la entrada; cada
    número es la longitud de la palabra ubicada en la misma posición. Valores
    mayores representan palabras que requieren más símbolos para transmitirse.
    """
    return [len(palabra) for palabra in palabras]


def calcular_kraft(palabras):
    """
    Calcula la sumatoria de la inecuacion de Kraft.
    Recibe una lista de palabras codigo y devuelve el valor de la suma.
    Obtiene la base r del alfabeto y suma r elevado a la longitud negativa
    de cada palabra.

    Algoritmo: obtiene la base r del alfabeto del código y suma r elevado al
    negativo de la longitud de cada palabra, según la inecuación de Kraft.

    Interpretación del resultado: una suma menor o igual que 1 cumple Kraft y
    permite que exista un código instantáneo con esas longitudes; una suma mayor
    que 1 lo hace imposible. El valor 1 indica que el árbol de código está lleno.
    """
    alfabeto = get_alfabetoCodigo(palabras)
    L = get_longitudes(palabras)
    r = len(alfabeto)

    if r == 0:
        return 0

    return sum(r ** -longitud for longitud in L)

def entropia_fuente(palabras, probabilidades):
    """
    Algoritmo: calcula el promedio de información de los símbolos fuente usando
    como base logarítmica la cantidad de símbolos del alfabeto del código.

    Interpretación del resultado: mide la incertidumbre en símbolos del alfabeto
    código por símbolo fuente. Un valor bajo describe una fuente predecible y
    uno alto una fuente menos predecible; el máximo ocurre con probabilidades
    uniformes. Las probabilidades nulas no aportan a la entropía.
    """

    #calcula la entropia de la fuente a partir de una lista de  palabras codigo de una codificacion y sus probabilidades

    set_palabras = set("".join(palabras))
    base = len(set_palabras)

    return sum([p*math.log(1/p, base) for p in probabilidades if p>0])

def get_longitudMedia(palabras, probabilidades):
    """
    Algoritmo: pondera la longitud de cada palabra código por su probabilidad de
    aparición y suma todos esos aportes.

    Interpretación del resultado: devuelve la cantidad promedio de símbolos de
    código necesarios por símbolo fuente. Cuanto menor sea el valor, más corta
    será en promedio la representación, si se comparan códigos válidos.
    """

    #calcula la longitud media del codigo

    return sum([p*len(palabra) for palabra, p in zip (palabras, probabilidades)])

def es_compacto(palabras, probabilidades):
    """
    Algoritmo: primero exige que el código sea unívocamente decodificable y luego
    verifica que la longitud de cada palabra no supere el entero superior de su
    información propia, expresada en la base del alfabeto código.

    Interpretación del resultado: True indica que el código satisface el criterio
    de compacidad implementado; False indica que es ambiguo o que al menos una
    palabra resulta más larga de lo permitido por ese criterio.
    """

    #Devuelve True si es compacto o False si no lo es

    if (es_univocamente_decodificable(palabras)):
        base = len(set("".join(palabras)))

        for palabra, p in zip(palabras, probabilidades):
            if not len(palabra) <= math.ceil(math.log(1/p, base)):
                return False

        return True
    else:
        return False

def generar_mensaje(N, palabras, probabilidades):
    """
    Algoritmo: realiza N elecciones aleatorias independientes entre las palabras
    código, usando sus probabilidades como pesos, y concatena las elegidas.

    Interpretación del resultado: devuelve un mensaje codificado formado por N
    palabras, aunque su longitud total puede variar si estas tienen longitudes
    distintas. En muchas generaciones, sus frecuencias deberían aproximarse a
    las probabilidades indicadas.
    """

    #Dado un N, una lista de palabras codigo de una codificacion y sus probabbilidades, genera aleatoriamente un posible mensaje de N símbolos codificados emitido por dicha fuente

    elegidas = random.choices(
        palabras,
        weights=probabilidades,
        k=N
    )
    return "".join(elegidas)

#A random.choises le pasas la lista con las palabras, para que tenga los elementos a elegir
# el peso de cada elemento
# Y un k que dice cuantas elecciones realiza, en este caso N
def clasifica(codigo):
    """
    Algoritmo: clasifica el código en forma jerárquica: comprueba si sus palabras
    son distintas, después si ninguna es prefijo de otra y, por último, si puede
    decodificarse de manera única mediante Sardinas-Patterson.

    Interpretación del resultado: "instantáneo" es la categoría más restrictiva;
    "unívoco" permite decodificación única pero no inmediata; "no singular" solo
    garantiza palabras distintas; y "bloque" indica que hay palabras repetidas.
    """
    if es_noSingular(codigo):
            if es_instantaneo(codigo):
                return "instantáneo"
            else:
                if es_univocamente_decodificable(codigo):
                    return "unívoco"
                else:
                    return "no singular"
    else:
            return "bloque"



# ############################################################################
# Func_clase4.py: codificación y control de errores (TP4)
# ############################################################################

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



# ############################################################################
# Func_clase5.py: compresión (TP5)
# ############################################################################

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



# ############################################################################
# Func_clase6.py: canales (TP6)
# ############################################################################

# ---------------------------------------------------------------------------
# Validaciones internas
# ---------------------------------------------------------------------------
def _validar_matriz(matriz):
    if not matriz or not matriz[0]:
        raise ValueError("La matriz del canal está vacía.")
    s = len(matriz[0])
    for i, fila in enumerate(matriz):
        if len(fila) != s:
            raise ValueError("Todas las filas de la matriz deben tener la misma cantidad de columnas.")
        if any(p < -1e-9 or p > 1 + 1e-9 for p in fila):  # tolera redondeos (1.0000000000000002)
            raise ValueError(f"La fila {i} tiene valores fuera de [0, 1].")
        if abs(sum(fila) - 1) > 1e-6:
            raise ValueError(f"La fila {i} suma {sum(fila)}; cada fila debe sumar 1.")


def _validar_canal(probs, matriz):
    _validar_matriz(matriz)
    if len(probs) != len(matriz):
        raise ValueError("Debe haber una probabilidad a priori por cada fila de la matriz.")
    if any(p < 0 for p in probs) or abs(sum(probs) - 1) > 1e-6:
        raise ValueError("Las probabilidades a priori deben ser no negativas y sumar 1.")


def _columna(matriz, j):
    return [fila[j] for fila in matriz]


# ---------------------------------------------------------------------------
# Ejercicio 2: matriz del canal a partir de secuencias
# ---------------------------------------------------------------------------
def canal_desde_secuencias(entrada, salida):
    """
    Qué es:
        A partir de una secuencia de entrada y la secuencia de salida que
        produjo el canal, obtiene todo lo que describe al canal: los
        alfabetos de entrada y salida, las probabilidades a priori y la
        matriz del canal.

    Para qué se usa:
        Para los ejercicios 1, 3, 8 y 9 y para el ejercicio 2 del parcial,
        donde el canal se conoce solo por su comportamiento observado.

    Cómo interpretar el resultado:
        Devuelve (alfabeto_A, probs, alfabeto_B, matriz):
        - alfabeto_A y alfabeto_B están ordenados; las filas de la matriz
          siguen el orden de alfabeto_A y las columnas el de alfabeto_B.
        - probs[i] es la frecuencia relativa de a_i en la entrada.
        - matriz[i][j] es la fracción de veces que, habiendo entrado a_i,
          salió b_j: P(b_j / a_i).
        - Una fila con un único valor distinto de cero indica que esa
          entrada siempre produce la misma salida; filas muy repartidas
          indican mucho ruido para esa entrada.

    Parámetros:
        entrada, salida: strings de igual longitud (el carácter k de la
                         salida es lo que salió al entrar el carácter k).
    """
    if len(entrada) != len(salida):
        raise ValueError("Las secuencias de entrada y salida deben tener la misma longitud.")
    if not entrada:
        raise ValueError("Las secuencias están vacías.")
    alfabeto_a, probs = GeneraAlfabetoYProb(entrada)
    alfabeto_b = sorted(set(salida))
    matriz = []
    for a in alfabeto_a:
        salidas_de_a = [b for x, b in zip(entrada, salida) if x == a]
        matriz.append([salidas_de_a.count(b) / len(salidas_de_a) for b in alfabeto_b])
    return alfabeto_a, probs, alfabeto_b, matriz


def matriz_canal(entrada, salida):
    """
    Qué es:
        Matriz del canal P(b_j / a_i) obtenida a partir de una secuencia de
        entrada y su secuencia de salida (ejercicio 2).

    Para qué se usa:
        Para caracterizar un canal a partir de su comportamiento observado.
        Con la matriz se calcula todo lo demás (probabilidades de salida, a
        posteriori, entropías, información mutua).

    Cómo interpretar el resultado:
        - Filas = símbolos de entrada (ordenados), columnas = símbolos de
          salida (ordenados). Cada fila suma 1.
        - matriz[i][j] es la probabilidad de que salga b_j cuando entra a_i.
        - Valores 1 en la "diagonal" y 0 en el resto: canal perfecto.
          Filas iguales entre sí: la salida no depende de la entrada (el
          canal no transmite información).
        - Para obtener también los alfabetos y las probabilidades a priori,
          usar canal_desde_secuencias.

    Parámetros:
        entrada, salida: strings de igual longitud.
    Devuelve:
        lista de listas.
    """
    return canal_desde_secuencias(entrada, salida)[3]


# ---------------------------------------------------------------------------
# Ejercicio 7: probabilidades de salida, a posteriori y simultáneas
# ---------------------------------------------------------------------------
def probabilidades_salida(probs, matriz):
    """
    Qué es:
        Probabilidad de cada símbolo de salida:
        P(b_j) = sum_i P(a_i) * P(b_j / a_i).

    Para qué se usa:
        Para conocer qué se observa a la salida del canal, y como paso previo
        para las probabilidades a posteriori y la entropía de la salida H(B).

    Cómo interpretar el resultado:
        - Lista con una probabilidad por columna de la matriz; suma 1.
        - Si el canal no tiene ruido, se parece a la distribución de
          entrada; cuanto más ruido, más se "mezcla".
        - Un valor 0 indica una salida que nunca aparece.

    Parámetros:
        probs: probabilidades a priori.
        matriz: matriz del canal.
    Devuelve:
        list.
    """
    _validar_canal(probs, matriz)
    s = len(matriz[0])
    return [sum(probs[i] * matriz[i][j] for i in range(len(probs))) for j in range(s)]


def probabilidades_simultaneas(probs, matriz):
    """
    Qué es:
        Probabilidades de los eventos simultáneos:
        P(a_i, b_j) = P(a_i) * P(b_j / a_i), es decir, la probabilidad de
        que entre a_i y salga b_j.

    Para qué se usa:
        Es la base de las entropías del canal (equivocación, pérdida,
        entropía afín, información mutua).

    Cómo interpretar el resultado:
        - Matriz con filas = entradas y columnas = salidas; la suma de TODOS
          los valores es 1.
        - Sumar una fila da P(a_i); sumar una columna da P(b_j).
        - Si cada fila y cada columna tienen un solo valor distinto de cero,
          la salida identifica exactamente a la entrada.

    Parámetros:
        probs: probabilidades a priori.
        matriz: matriz del canal.
    Devuelve:
        lista de listas.
    """
    _validar_canal(probs, matriz)
    return [[probs[i] * p for p in fila] for i, fila in enumerate(matriz)]


def probabilidades_a_posteriori(probs, matriz):
    """
    Qué es:
        Probabilidades a posteriori P(a_i / b_j): la probabilidad de que
        haya entrado a_i sabiendo que salió b_j (teorema de Bayes):
        P(a_i / b_j) = P(a_i) * P(b_j / a_i) / P(b_j).

    Para qué se usa:
        Para saber qué se puede deducir de la entrada al observar la salida.
        Es la base de las entropías a posteriori, la equivocación y la regla
        de decisión de máxima posibilidad.

    Cómo interpretar el resultado:
        - Matriz con filas = entradas y columnas = salidas; cada COLUMNA
          suma 1 (dado que salió b_j, alguna entrada tuvo que ser).
        - Una columna con un 1 y el resto 0: al ver esa salida se sabe con
          certeza qué entró.
        - Una columna igual a las probabilidades a priori: esa salida no
          aporta nada sobre la entrada.
        - Si una salida tiene P(b_j) = 0 su columna queda en 0 (no está
          definida porque nunca ocurre).

    Parámetros:
        probs: probabilidades a priori.
        matriz: matriz del canal.
    Devuelve:
        lista de listas.
    """
    conjunta = probabilidades_simultaneas(probs, matriz)
    salida = probabilidades_salida(probs, matriz)
    return [[conjunta[i][j] / salida[j] if salida[j] > 0 else 0.0
             for j in range(len(salida))] for i in range(len(probs))]


# ---------------------------------------------------------------------------
# Ejercicio 11: entropías a posteriori
# ---------------------------------------------------------------------------
def entropias_a_posteriori(probs, matriz):
    """
    Qué es:
        Entropía a posteriori de la entrada para cada símbolo de salida:
        H(A / b_j) = sum_i P(a_i / b_j) * log2(1 / P(a_i / b_j)).

    Para qué se usa:
        Para medir cuánta incertidumbre sobre la entrada queda después de
        observar cada salida, y compararla con la entropía a priori H(A)
        (se calcula con CalcEntropia(probs)).

    Cómo interpretar el resultado:
        - Lista con un valor por símbolo de salida.
        - H(A / b_j) = 0: al recibir b_j se sabe con certeza qué entró.
        - H(A / b_j) < H(A): recibir b_j reduce la incertidumbre.
        - H(A / b_j) > H(A) es posible: una salida puntual puede dejar más
          dudas que antes de recibirla. Lo que nunca puede pasar es que el
          PROMEDIO (la equivocación H(A/B)) supere a H(A).
        - Una salida con P(b_j) = 0 da 0 (nunca ocurre).

    Parámetros:
        probs: probabilidades a priori.
        matriz: matriz del canal.
    Devuelve:
        list.
    """
    post = probabilidades_a_posteriori(probs, matriz)
    return [CalcEntropia(_columna(post, j)) for j in range(len(matriz[0]))]


# ---------------------------------------------------------------------------
# Ejercicio 15: entropías del canal por definición
# ---------------------------------------------------------------------------
def equivocacion(probs, matriz):
    """
    Qué es:
        Equivocación o ruido del canal, calculada por definición:
        H(A/B) = sum_{a,b} P(a,b) * log2(1 / P(a/b)).

    Para qué se usa:
        Mide la información sobre la entrada que el canal NO deja pasar: la
        incertidumbre que queda sobre A después de observar B.

    Cómo interpretar el resultado:
        - 0: canal sin ruido; mirando la salida se sabe siempre qué entró.
        - Igual a H(A): la salida no dice nada de la entrada (entrada y
          salida independientes); no pasa información.
        - Valores intermedios: parte de la información se pierde. Cuanto
          más cerca de 0, mejor el canal.
        - Siempre 0 <= H(A/B) <= H(A).

    Parámetros:
        probs: probabilidades a priori.
        matriz: matriz del canal.
    Devuelve:
        float (bits).
    """
    conjunta = probabilidades_simultaneas(probs, matriz)
    post = probabilidades_a_posteriori(probs, matriz)
    return sum(conjunta[i][j] * math.log2(1 / post[i][j])
               for i in range(len(probs)) for j in range(len(matriz[0]))
               if conjunta[i][j] > 0)


def perdida(probs, matriz):
    """
    Qué es:
        Pérdida del canal, calculada por definición:
        H(B/A) = sum_{a,b} P(a,b) * log2(1 / P(b/a)).

    Para qué se usa:
        Mide la incertidumbre sobre la salida que queda aun conociendo la
        entrada: cuánto "dispersa" el canal cada símbolo enviado.

    Cómo interpretar el resultado:
        - 0: canal determinante; cada entrada produce siempre la misma
          salida.
        - Igual a H(B): la salida no depende de la entrada.
        - Cuanto mayor, más aleatoria es la salida para una entrada dada.
        - Siempre 0 <= H(B/A) <= H(B).

    Parámetros:
        probs: probabilidades a priori.
        matriz: matriz del canal.
    Devuelve:
        float (bits).
    """
    conjunta = probabilidades_simultaneas(probs, matriz)
    return sum(conjunta[i][j] * math.log2(1 / matriz[i][j])
               for i in range(len(probs)) for j in range(len(matriz[0]))
               if conjunta[i][j] > 0)


def entropia_afin(probs, matriz):
    """
    Qué es:
        Entropía afín o conjunta, calculada por definición:
        H(A,B) = sum_{a,b} P(a,b) * log2(1 / P(a,b)).

    Para qué se usa:
        Mide la incertidumbre total del par (entrada, salida). Es la unión
        de H(A) y H(B) en el diagrama de Venn del canal.

    Cómo interpretar el resultado:
        - Cumple H(A,B) = H(A) + H(B) - I(A,B).
        - Igual a H(A) + H(B): entrada y salida independientes (I = 0).
        - Igual a H(A) (o a H(B)): uno de los dos determina completamente
          al otro.
        - Siempre max(H(A), H(B)) <= H(A,B) <= H(A) + H(B).

    Parámetros:
        probs: probabilidades a priori.
        matriz: matriz del canal.
    Devuelve:
        float (bits).
    """
    conjunta = probabilidades_simultaneas(probs, matriz)
    return CalcEntropia([p for fila in conjunta for p in fila])


def informacion_mutua(probs, matriz):
    """
    Qué es:
        Información mutua, calculada por definición:
        I(A,B) = sum_{a,b} P(a,b) * log2( P(a,b) / (P(a) * P(b)) ).

    Para qué se usa:
        Mide cuánta información sobre la entrada atraviesa el canal: la
        incertidumbre sobre A que se resuelve al observar B. Es la medida
        principal de qué tan bueno es un canal para una fuente dada.

    Cómo interpretar el resultado:
        - 0: entrada y salida independientes; el canal no transmite nada.
        - Igual a H(A): canal sin ruido, pasa toda la información de la
          entrada.
        - Igual a H(B): canal determinante.
        - Nunca es negativa y es recíproca: I(A,B) = I(B,A).
        - Depende de las probabilidades a priori; su máximo sobre todas las
          distribuciones posibles es la capacidad del canal.

    Parámetros:
        probs: probabilidades a priori.
        matriz: matriz del canal.
    Devuelve:
        float (bits).
    """
    conjunta = probabilidades_simultaneas(probs, matriz)
    salida = probabilidades_salida(probs, matriz)
    return sum(conjunta[i][j] * math.log2(conjunta[i][j] / (probs[i] * salida[j]))
               for i in range(len(probs)) for j in range(len(salida))
               if conjunta[i][j] > 0)


def analisis_canal(probs, matriz):
    """
    Qué es:
        Calcula todas las entropías de un canal y verifica las relaciones
        entre ellas.

    Para qué se usa:
        Para resolver de una vez los ejercicios 14, 16, 17, 19 y 21 y
        comprobar los resultados hechos a mano.

    Cómo interpretar el resultado (diccionario):
        'H(A)'    entropía a priori (de la entrada).
        'H(B)'    entropía de la salida.
        'H(A/B)'  equivocación o ruido.
        'H(B/A)'  pérdida.
        'H(A,B)'  entropía afín.
        'I(A,B)'  información mutua por definición.
        'I(B,A)'  H(B) - H(B/A); tiene que coincidir con I(A,B)
                  (reciprocidad).
        'verifica_relaciones'  True si se cumplen
                  I = H(A) - H(A/B) = H(B) - H(B/A) y
                  H(A,B) = H(A) + H(B) - I.
                  False indicaría un error en los datos.

    Parámetros:
        probs: probabilidades a priori.
        matriz: matriz del canal.
    Devuelve:
        dict.
    """
    h_a = CalcEntropia(probs)
    h_b = CalcEntropia(probabilidades_salida(probs, matriz))
    h_ab = equivocacion(probs, matriz)
    h_ba = perdida(probs, matriz)
    h_conj = entropia_afin(probs, matriz)
    i_ab = informacion_mutua(probs, matriz)
    i_ba = h_b - h_ba
    tol = 1e-6
    verifica = (abs(i_ab - (h_a - h_ab)) < tol and abs(i_ab - i_ba) < tol
                and abs(h_conj - (h_a + h_b - i_ab)) < tol)
    return {
        "H(A)": h_a, "H(B)": h_b, "H(A/B)": h_ab, "H(B/A)": h_ba,
        "H(A,B)": h_conj, "I(A,B)": i_ab, "I(B,A)": i_ba,
        "verifica_relaciones": verifica,
    }


# ---------------------------------------------------------------------------
# Ejercicio 18: canales sin ruido y determinantes
# ---------------------------------------------------------------------------
def es_sin_ruido(matriz):
    """
    Qué es:
        Verifica si el canal es sin ruido: cada COLUMNA de la matriz tiene
        un único elemento distinto de cero.

    Para qué se usa:
        Para clasificar canales (ejercicio 17) y para saber si se puede usar
        la fórmula directa de capacidad C = log2(cantidad de entradas).

    Cómo interpretar el resultado:
        - True: al ver cualquier salida se sabe con certeza qué entró. La
          equivocación H(A/B) es 0 y I(A,B) = H(A): pasa toda la
          información de la entrada.
        - False: alguna salida puede venir de más de una entrada, así que
          hay incertidumbre sobre lo enviado.
        - Un canal puede ser sin ruido y a la vez repartir una entrada en
          varias salidas (no es necesariamente determinante).

    Parámetros:
        matriz: matriz del canal.
    Devuelve:
        bool.
    """
    _validar_matriz(matriz)
    return all(sum(1 for p in _columna(matriz, j) if p > _TOL) == 1
               for j in range(len(matriz[0])))


def es_determinante(matriz):
    """
    Qué es:
        Verifica si el canal es determinante: cada FILA de la matriz tiene
        un único elemento distinto de cero (que entonces vale 1).

    Para qué se usa:
        Para clasificar canales (ejercicio 17), para las reducciones (el
        canal que combina columnas es determinante) y para la fórmula de
        capacidad C = log2(cantidad de salidas).

    Cómo interpretar el resultado:
        - True: cada entrada produce siempre la misma salida. La pérdida
          H(B/A) es 0 y I(A,B) = H(B).
        - False: alguna entrada puede producir salidas distintas.
        - Un canal determinante puede llevar varias entradas a la misma
          salida (no es necesariamente sin ruido).
        - Si es determinante y sin ruido a la vez, es una permutación: la
          salida es la entrada "renombrada" y I(A,B) = H(A) = H(B).

    Parámetros:
        matriz: matriz del canal.
    Devuelve:
        bool.
    """
    _validar_matriz(matriz)
    return all(sum(1 for p in fila if p > _TOL) == 1 for fila in matriz)


# ---------------------------------------------------------------------------
# Ejercicio 20: canales en serie
# ---------------------------------------------------------------------------
def canal_serie(matriz1, matriz2):
    """
    Qué es:
        Matriz del canal compuesto por dos canales en serie: la salida del
        primero es la entrada del segundo. Es el producto de matrices
        P(c/a) = sum_b P(b/a) * P(c/b).

    Para qué se usa:
        Para el ejercicio 19 y para las reducciones de canales (una
        reducción es poner en serie un canal determinante).

    Cómo interpretar el resultado:
        - Filas = entradas del primer canal; columnas = salidas del segundo.
        - La información mutua del canal compuesto nunca supera a la del
          primer canal: I(A,C) <= I(A,B). Los procesamientos en serie no
          agregan información, a lo sumo la conservan.
        - La cantidad de columnas del primer canal tiene que coincidir con
          la cantidad de filas del segundo.

    Parámetros:
        matriz1: matriz del primer canal (r x s).
        matriz2: matriz del segundo canal (s x t).
    Devuelve:
        lista de listas (r x t).
    """
    _validar_matriz(matriz1)
    _validar_matriz(matriz2)
    if len(matriz1[0]) != len(matriz2):
        raise ValueError("Las salidas del primer canal deben ser las entradas del segundo.")
    t = len(matriz2[0])
    return [[sum(fila[k] * matriz2[k][j] for k in range(len(fila))) for j in range(t)]
            for fila in matriz1]


# ---------------------------------------------------------------------------
# Ejercicios 22 y 23: reducciones suficientes
# ---------------------------------------------------------------------------
def es_reduccion_suficiente(matriz, j, k):
    """
    Qué es:
        Verifica si las columnas j y k del canal se pueden combinar en una
        reducción suficiente: tienen que ser proporcionales,
        P(b_j/a) = constante * P(b_k/a) para toda entrada a.

    Para qué se usa:
        Para simplificar un canal (menos salidas) sin perder información
        (ejercicios 21 y 22a).

    Cómo interpretar el resultado:
        - True: combinar esas dos salidas no cambia la información mutua,
          cualesquiera sean las probabilidades a priori. Las dos salidas
          dicen exactamente lo mismo sobre la entrada.
        - False: combinarlas igual se puede, pero se pierde información
          (I(A,C) < I(A,B)).

    Parámetros:
        matriz: matriz del canal.
        j, k: índices de las columnas (desde 0), distintos.
    Devuelve:
        bool.
    """
    _validar_matriz(matriz)
    s = len(matriz[0])
    if not (0 <= j < s and 0 <= k < s) or j == k:
        raise ValueError("Los índices deben ser dos columnas distintas de la matriz.")
    cj, ck = _columna(matriz, j), _columna(matriz, k)
    sj, sk = sum(cj), sum(ck)
    return all(abs(x * sk - y * sj) < 1e-9 for x, y in zip(cj, ck))


def matriz_determinante_reduccion(matriz, j, k):
    """
    Qué es:
        Matriz del canal determinante que, puesto en serie a continuación
        del canal, combina las columnas j y k en una sola salida.

    Para qué se usa:
        Para realizar la reducción (ejercicio 22b):
        canal_serie(matriz, matriz_determinante_reduccion(matriz, j, k)).

    Cómo interpretar el resultado:
        - Es una matriz de s filas (salidas originales) y s-1 columnas
          (salidas del canal reducido), con un único 1 por fila.
        - Las salidas j y k van a la misma columna, ubicada en la posición
          de la menor de las dos; el resto mantiene su orden.
        - No verifica si la reducción es suficiente; para eso está
          es_reduccion_suficiente.

    Parámetros:
        matriz: matriz del canal.
        j, k: índices de las columnas a combinar (desde 0), distintos.
    Devuelve:
        lista de listas (s x (s-1)).
    """
    _validar_matriz(matriz)
    s = len(matriz[0])
    if not (0 <= j < s and 0 <= k < s) or j == k:
        raise ValueError("Los índices deben ser dos columnas distintas de la matriz.")
    menor, mayor = min(j, k), max(j, k)
    determinante = []
    for b in range(s):
        destino = menor if b == mayor else (b if b < mayor else b - 1)
        determinante.append([1.0 if c == destino else 0.0 for c in range(s - 1)])
    return determinante


def reducir_canal(matriz, pasos=False):
    """
    Qué es:
        Aplica todas las reducciones suficientes posibles: mientras haya dos
        columnas proporcionales, las combina (con las funciones de los
        ejercicios 20 y 22). Siempre combina el primer par encontrado.

    Para qué se usa:
        Para obtener el canal más simple que transmite la misma información
        (ejercicios 21 y 23).

    Cómo interpretar el resultado:
        - Devuelve la matriz del canal reducido. Con pasos=True devuelve la
          lista de matrices de cada paso (la primera es la original).
        - La información mutua es la misma en todos los pasos (para
          cualquier distribución a priori): por eso son reducciones
          suficientes.
        - Si el canal reducido es determinante (es_determinante), la salida
          ya no tiene ruido "extra": toda su variación depende de la
          entrada.
        - Si la matriz no cambia, el canal no admite reducciones suficientes.

    Parámetros:
        matriz: matriz del canal.
        pasos: si es True devuelve todas las matrices intermedias.
    Devuelve:
        lista de listas, o lista de matrices si pasos es True.
    """
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


# ---------------------------------------------------------------------------
# Ejercicios 25 y 26: capacidad
# ---------------------------------------------------------------------------
def _es_permutacion(a, b):
    return all(abs(x - y) < 1e-9 for x, y in zip(sorted(a), sorted(b)))


def es_uniforme(matriz):
    """
    Qué es:
        Verifica si el canal es uniforme: todas las filas tienen los mismos
        valores (en distinto orden) y todas las columnas también.

    Para qué se usa:
        Para saber si se puede calcular la capacidad con la fórmula directa
        C = log2(cantidad de salidas) - H(fila) (ejercicio 25). El canal
        binario simétrico (BSC) es el caso más conocido.

    Cómo interpretar el resultado:
        - True: el canal trata a todas las entradas "de la misma manera";
          la capacidad se alcanza con entradas equiprobables.
        - False: hay que buscar la capacidad de otra forma (por ejemplo,
          con capacidad_binaria si el canal tiene 2 entradas).
        - Se exige también que las columnas sean permutaciones entre sí:
          si solo las filas lo fueran, la fórmula daría un valor mayor que
          la capacidad real.

    Parámetros:
        matriz: matriz del canal.
    Devuelve:
        bool.
    """
    _validar_matriz(matriz)
    filas_ok = all(_es_permutacion(fila, matriz[0]) for fila in matriz)
    columnas = [_columna(matriz, j) for j in range(len(matriz[0]))]
    columnas_ok = all(len(c) == len(columnas[0]) and _es_permutacion(c, columnas[0]) for c in columnas)
    return filas_ok and columnas_ok


def capacidad_canal(matriz):
    """
    Qué es:
        Capacidad C del canal (máxima información mutua posible, en bits),
        para los casos con fórmula directa:
          - Canal determinante: C = log2(cantidad de salidas usadas).
          - Canal sin ruido:    C = log2(cantidad de entradas).
          - Canal uniforme:     C = log2(cantidad de salidas) - H(fila).

    Para qué se usa:
        Para los ejercicios 24 y 25b. Según el Segundo Teorema de Shannon,
        una fuente con entropía H <= C se puede transmitir por el canal con
        una probabilidad de error tan chica como se quiera.

    Cómo interpretar el resultado:
        - Devuelve (C, tipo), donde tipo dice qué fórmula se usó.
        - C = 0: el canal no transmite información.
        - C = log2(r) con r entradas: es el máximo posible; el canal no
          pierde nada.
        - Si el canal no es de ninguno de los tres tipos devuelve
          (None, 'sin fórmula directa'): para canales binarios usar
          capacidad_binaria.

    Parámetros:
        matriz: matriz del canal.
    Devuelve:
        tupla (float o None, str).
    """
    if es_determinante(matriz):
        usadas = sum(1 for j in range(len(matriz[0])) if any(p > _TOL for p in _columna(matriz, j)))
        return math.log2(usadas), "determinante"
    if es_sin_ruido(matriz):
        return math.log2(len(matriz)), "sin ruido"
    if es_uniforme(matriz):
        return math.log2(len(matriz[0])) - CalcEntropia(matriz[0]), "uniforme"
    return None, "sin fórmula directa"


def capacidad_binaria(matriz, paso):
    """
    Qué es:
        Estima la capacidad de un canal con 2 entradas calculando la
        información mutua para P(a1) = 0, paso, 2*paso, ..., 1 (con
        P(a2) = 1 - P(a1)) y quedándose con el máximo.

    Para qué se usa:
        Para los canales binarios que no tienen fórmula directa
        (ejercicios 26 y 27) y para el ejercicio 2 del parcial (se le pasa
        el canal reducido, que tiene la misma capacidad que el original).

    Cómo interpretar el resultado:
        - Devuelve (C, p): C es la capacidad estimada y p la probabilidad
          a priori P(a1) con la que se alcanza. La distribución óptima es
          {p, 1 - p}: P(0) = p y P(1) = 1 - p.
        - Cuanto más chico el paso, más precisa la estimación (con
          paso = 0.0001 se obtienen 4 decimales).
        - p cerca de 0.5: al canal le convienen entradas casi equiprobables
          (pasa en canales casi simétricos).
        - C cerca de 0: el canal es muy ruidoso; ninguna distribución de
          entrada logra pasar mucha información.

    Parámetros:
        matriz: matriz del canal (2 filas).
        paso: incremento de P(a1), entre 0 y 1.
    Devuelve:
        tupla (capacidad, probabilidad).
    """
    _validar_matriz(matriz)
    if len(matriz) != 2:
        raise ValueError("El canal debe tener exactamente 2 entradas.")
    if not 0 < paso <= 1:
        raise ValueError("El paso debe estar entre 0 y 1.")
    cantidad = int(1 / paso + 1e-9)
    mejor_c, mejor_p = -1.0, 0.0
    for i in range(cantidad + 1):
        p = min(i * paso, 1.0)
        c = informacion_mutua([p, 1 - p], matriz)
        if c > mejor_c + 1e-12:
            mejor_c, mejor_p = c, p
    return mejor_c, mejor_p


# ---------------------------------------------------------------------------
# Ejercicio 30: probabilidad de error
# ---------------------------------------------------------------------------
def probabilidad_error(probs, matriz, a_posteriori=False):
    """
    Qué es:
        Probabilidad de error del canal con una regla de decisión: para cada
        salida b_j el receptor decide qué entrada a* se envió, y
        P_E = 1 - sum_j P(a*, b_j).

        Hay dos reglas posibles:
          - Máxima posibilidad (por defecto, es la que usan los resultados
            de la guía): a* es la entrada con mayor P(b_j / a*), la mayor
            probabilidad de la columna j de la matriz. No tiene en cuenta
            las probabilidades a priori al decidir.
          - Máxima probabilidad a posteriori (a_posteriori=True, es la que
            describe la diapositiva de la teoría): a* es la entrada con
            mayor P(a* / b_j), es decir, mayor P(a*) * P(b_j / a*).

    Para qué se usa:
        Para medir qué tan seguido se equivoca el receptor al adivinar la
        entrada a partir de la salida (ejercicios 28 a 30).

    Cómo interpretar el resultado:
        - 0: el receptor nunca se equivoca (canal sin ruido).
        - Cuanto más grande, peor.
        - Depende de las probabilidades a priori: el mismo canal puede
          tener distinta P_E según qué tan probable sea cada entrada.
        - Con entradas equiprobables las dos reglas dan lo mismo.
        - Con entradas no equiprobables la regla a posteriori da una P_E
          menor o igual: es la mínima posible decidiendo símbolo a símbolo.
          Ejemplo, ejercicio 29b: 0.425 con máxima posibilidad y 0.35 con
          la regla a posteriori.
        - Si hay empate en el máximo de una columna, se elige la primera
          entrada.

    Parámetros:
        probs: probabilidades a priori.
        matriz: matriz del canal.
        a_posteriori: False = máxima posibilidad; True = máxima
                      probabilidad a posteriori.
    Devuelve:
        float.
    """
    conjunta = probabilidades_simultaneas(probs, matriz)
    aciertos = 0.0
    for j in range(len(matriz[0])):
        criterio = _columna(conjunta, j) if a_posteriori else _columna(matriz, j)
        elegida = criterio.index(max(criterio))
        aciertos += conjunta[elegida][j]
    return 1 - aciertos
