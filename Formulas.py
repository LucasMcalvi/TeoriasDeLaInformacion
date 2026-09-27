import math
import random

def CalcInfo (fdp): #dado una lista de probabilidades genera una lista con la informacion obtenida en bits
    """
    Algoritmo: calcula la cantidad de información asociada a cada suceso como
    el logaritmo en base 2 del inverso de su probabilidad.

    Interpretación del resultado: devuelve una lista medida en bits. Un valor
    alto corresponde a un suceso poco probable y sorpresivo; un valor bajo
    corresponde a un suceso frecuente y predecible.
    """
    return [math.log2(1/p) for p in fdp if p>0]

def CalcEntropia (fdp): #dado una lista de probabilidades devuelve la entropia
    """
    Algoritmo: obtiene la información de cada suceso y calcula su promedio
    ponderado usando como pesos las probabilidades de la fuente.

    Interpretación del resultado: devuelve la entropía en bits por símbolo.
    Una entropía baja indica una fuente muy predecible; una entropía alta
    indica mayor incertidumbre. El máximo se alcanza con sucesos equiprobables.
    """
    info = CalcInfo(fdp)
    return sum([p*i for p,i in zip(fdp,info)])



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
    for k in range(30):          # con 10 no llega a estabilizarse del todo, con 30 si
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
