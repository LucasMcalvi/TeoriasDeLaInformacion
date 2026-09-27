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


def CalcEntropia (fdp):
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
    pares = sorted(zip(alfabeto, probabilidades))    # ordena por simbolo, sin separar cada par
    alfabeto = [s for s, p in pares]
    probabilidades = [p for s, p in pares]
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
    alfabeto.sort() 
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
    for k in range(50):          # con 10 no llega a estabilizarse del todo, con 30 si
        piNuevo = [0] * n
        for j in range(n):                  # j = estado DESTINO
            suma = 0
            for i in range(n):              # i = estado ORIGEN
                suma += pi[i] * matriz[j][i]  # matriz[destino][origen]
            piNuevo[j] = suma
        pi = piNuevo.copy()
    return pi


def tienememoria(matriz,tolerancia):
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


def entropiaFuenteMarkov(matriz, pi):   # NUEVA
    """
    Algoritmo: para cada estado de origen toma su columna (la distribucion
    del simbolo siguiente dado ese origen), calcula su entropia, y promedia
    esas entropias ponderando por pi (vector estacionario):
        H(S) = suma_j  pi[j] * H(columna j)
 
    Interpretación del resultado: bits por simbolo de la fuente CON memoria.
    En teoria es <= que la entropia calculada como si fuera de memoria nula
    (CalcEntropia de las probabilidades del mensaje). La diferencia entre
    ambas mide cuanto ayuda conocer el simbolo anterior para predecir el
    siguiente: cuanto mas grande, mas fuerte es la memoria.
    En una fuente SIN memoria las dos dan igual (o casi, por ruido de
    muestreo en mensajes cortos).
    """
    columnas = transponer(matriz)   # fila j de la transpuesta = columna j (origen j)
    H = 0
    for j in range(len(columnas)):
        H += pi[j] * CalcEntropia(columnas[j])   # CalcEntropia ya ignora los ceros
    return H
 
 


def imprimirMatriz(alfabeto, matriz):
    n = len(alfabeto)
    print("llegada \\ origen", end="")
    for j in range(n):
        print(f"{alfabeto[j]:>8}", end="")          # encabezado: un simbolo por columna
    print()
    for i in range(n):
        print(f"{alfabeto[i]:>16}", end="")         # nombre de la fila
        for j in range(n):
            print(f"{matriz[i][j]:8.3f}", end="")   # 3 decimales, ancho 8
        print()
    print(f"{'suma columna':>16}", end="")
    for j in range(n):
        print(f"{sum(matriz[i][j] for i in range(n)):8.3f}", end="")
    print()
def imprimirProbabilidades(alfabeto, probs):
    porLinea=1
    for k in range(len(alfabeto)):
        print(f'P("{alfabeto[k]}") = {probs[k]:.4f}', end="    ")
        if (k + 1) % porLinea == 0:
            print()                        # salto de renglon cada porLinea pares
    if len(alfabeto) % porLinea != 0:
        print()
    print(f"Suma = {sum(probs):.4f}")

tolerancia = 0.01
""""
a) Recorri el mensaje y tome cada simbolo distinto como alfabeto de la fuente, ordenados como en el enunciado. La probabilidad de cada simbolo es su cantidad de apariciones dividida por el largo del mensaje (50 simbolos). Por ejemplo, ")" aparece 22 veces: 22/50 = 0.44.

b) Recorri el mensaje de a pares consecutivos (simbolo actual, simbolo siguiente), que son 49 pares, y conte cada par en la celda de la matriz con columna = simbolo actual (origen) y fila = simbolo siguiente (llegada). Despues dividi cada celda por el total de su columna, es decir por la cantidad de veces que ese simbolo aparece seguido de otro, y no por el total de pares. Asi cada columna es la distribucion P(siguiente | actual) y suma 1.

c) Si la fuente no tiene memoria, el simbolo anterior no cambia la probabilidad del siguiente, entonces todas las columnas de la matriz tienen que ser iguales. Para cada fila compare los valores de las distintas columnas con una tolerancia de 0.01: si alguna diferencia la supera, la fuente tiene memoria. En el mensaje 1 las columnas son iguales (diferencia 0), por lo que es de memoria nula. En el mensaje 2 difieren hasta 0.33 (por ejemplo, P("." | ",") = 0.33 pero P("." | ".") = 0), por lo que tiene memoria.

d) Para la fuente de memoria nula use H(S) = suma de p.log2(1/p) con las probabilidades del inciso a. Para la fuente con memoria calcule la entropia de cada columna de la matriz (la incertidumbre sobre el siguiente simbolo sabiendo el actual) y las promedie ponderando con el vector estacionario: H(S) = suma de pi_j . H(columna j).

e) Solo para la fuente de memoria nula: arme los 16 pares posibles combinando cada simbolo con cada uno de los 4. Como los simbolos son independientes, la probabilidad de cada par es el producto de las probabilidades individuales, por ejemplo P("()") = 0.14 . 0.44 = 0.061. La entropia de la extension se calcula con la misma formula sobre esas 16 probabilidades.

f) Solo para la fuente con memoria: parti de un vector con la misma probabilidad para cada estado () y lo multiplique repetidamente por la matriz de transicion, pi_nuevo(i) = suma de P(i | j) . pi(j), hasta que dejo de cambiar. El vector final cumple pi = M . pi y suma 1.

"""