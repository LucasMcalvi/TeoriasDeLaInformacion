import math


def GeneraAlfabetoYProb (cadena): #dado una cadena de caracteres, devuelve dos listas paralelas de alfabeto
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


def generaalfabetoyTransicion(cadena):  #genera el alfabeto y la matriz de transicion con todas las probabilidades de pasar de un estado de origen a uno de llegada, considera probabilidades degun el simbolo anterior
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

def tieneMemoriaNoNula(matriz,tolerancia):

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

def calculaEntropiaMarkovOrden1(matriz, vector_estacionario=None):
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

def DevuelveExt2ConMemoria(alfabeto, matriz, vector):
    alfext2 = []
    probext2 = []

    for i, origen in enumerate(alfabeto):
        for j, destino in enumerate(alfabeto):
            alfext2.append(origen + destino)
            probext2.append(vector[i] * matriz[j][i])

    return alfext2, probext2

mensaje = "BBCCAABBCCAABBCCAABBCCAABBCCAA"

alfabeto, prob = GeneraAlfabetoYProb(mensaje)
alfabeto, matriz = generaalfabetoyTransicion(mensaje)
n = len(alfabeto)
memoriaNoNula = tieneMemoriaNoNula(matriz, 0.01)
#alfext2, probext2 = Formulas.DevuelveExtyFdp(alfabeto, prob, 2)
if memoriaNoNula:
    vector = generaVectorEstacionario(matriz, n)
    entropia = calculaEntropiaMarkovOrden1(matriz, vector)
    entropiaextension = 2 * entropia

print(matriz)
print(memoriaNoNula)
print(vector)
print(entropia)
print(entropiaextension)

alfext2, probext2 = DevuelveExt2ConMemoria(alfabeto, matriz, vector)

print(alfext2)
print(probext2)

