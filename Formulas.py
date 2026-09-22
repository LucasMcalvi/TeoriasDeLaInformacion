import math
import random

def CalcInfo (fdp): #dado una lista de probabilidades genera una lista con la informacion obtenida en bits
    return [math.log2(1/p) for p in fdp]

def CalcEntropia (fdp): #dado una lista de probabilidades devuelve la entropia
    info = CalcInfo(fdp)
    return sum([p*i for p,i in zip(fdp,info)])



#CADENAS
def GeneraAlfabetoYProb (cadena): #dado una cadena de caracteres, devuelve dos listas paralelas de alfabeto
    long = len(cadena)
    alfabeto = []                 #y otra con la probabilidad de ocurrencia de cada caracter de la lista alfabeto
    probabilidades = []
    for c in cadena:
        if c not in alfabeto and c != ' ':
            alfabeto.append(c)
            probabilidades.append(cadena.count(c)/long)
    
    return alfabeto, probabilidades

def GeneraPalabra (N, alfabeto, probabilidades):  #dado un int, un array alfabeto y un array paralelo con 
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
    return math.log2(cant)

def DevuelveExtyFdp (alfabeto, fdp, N): #Dado un alfabeto, una lista de probabilidades y un orden N devuelve una lista de extension N y du distribucion de probabilidades
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
    prob = [w, 1-w]
    return CalcEntropia(prob)