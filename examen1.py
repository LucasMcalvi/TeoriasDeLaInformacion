
import math
import random
cadena = ")[))[([()))()[[]](([[)))])))][))(][)[[[)()]))[)[])"
cadena2 =".;.:.:.::;:,::.;:,::,;,:;.:.;.;;:,.::.:,.:.;:::::."


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
            alfabeto.append(cadena[i])
    alfabeto.sort() 
    n=len(alfabeto)
    mat=[[0 for i in range(n)] for j in range(n)]
    for k in range (len(cadena)-1):
        mat[alfabeto.index(cadena[k+1])][alfabeto.index(cadena[k])] += 1
    #divido matriz
    for j in range (n):
        total_columna = sum(mat[i][j] for i in range(n))
        for i in range (n):
            mat[i][j] = mat[i][j]/total_columna
    
    return alfabeto, mat ;

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
def transponer(matriz):
    return [list(fila) for fila in zip(*matriz)]
    

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

tolerancia =0.01
alfabeto, probabilidades = GeneraAlfabetoYProb(cadena2)
alfabeto, matriz = generaalfabetoyTransicion(cadena2)

print(cadena2)
print("Alfabeto y probabilidades:")
imprimirProbabilidades(alfabeto, probabilidades)
print("Matriz de transicion (columna = origen, fila = llegada):")
imprimirMatriz(alfabeto, matriz)
if tienememoria(matriz, tolerancia):
    print("Memoria: fuente CON memoria (tolerancia utilizada:", tolerancia, ")")
    vector = generaVectorEstacionario(matriz, len(alfabeto))
    print("Entropia de la fuente (Markov):", round(entropiaFuenteMarkov(matriz, vector), 4))
    print("Entropia de la fuente afin (si no tuviera memoria):", round(CalcEntropia(vector), 4))
    print("Vector estacionario:")
    imprimirProbabilidades(alfabeto, vector)
else:
    print("Memoria: fuente de memoria NULA (tolerancia utilizada:", tolerancia, ")")
    H = CalcEntropia(probabilidades)
    print("Entropia de la fuente:", round(H, 4))
    ext, probsExt = DevuelveExtyFdp(alfabeto, probabilidades, 2)
    print("Extension de orden 2:")
    imprimirProbabilidades(ext, probsExt)
    print("Entropia de la extension:", round(CalcEntropia(probsExt), 4), " = 2 * H(S) =", round(2*H, 4))
print()