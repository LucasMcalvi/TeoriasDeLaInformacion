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
    return [math.log2(1/p) for p in fdp]

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

def DevuelveExtyFdp (alfabeto, fdp, N): #Dado un alfabeto, una lista de probabilidades y un orden N devuelve una lista de extension N y du distribucion de probabilidades
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
    n=len(alfabeto);
    mat=[[0 for i in range(n)] for j in range(n)]
    for k in range (len(cadena)-1):
        mat[alfabeto.index(cadena[k+1])][alfabeto.index(cadena[k])] += 1
    #divido matriz
    for j in range (n):
        total_columna = sum(mat[i][j] for i in range(n))
        for i in range (n):
            mat[i][j] = mat[i][j]/total_columna

    return alfabeto, mat ;
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


def tienememorianula(matriz,tolerancia):
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

tolerancia = 0.1
