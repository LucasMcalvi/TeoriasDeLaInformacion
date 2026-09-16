import math
import random

cadena = "La entropia representa la incertidumbre"
def GeneraAlfabetoYProb (cadena): #dado una cadena de caracteres, devuelve dos listas paralelas de alfabeto
    long = len(cadena)
    alfabeto = []                 #y otra con la probabilidad de ocurrencia de cada caracter de la lista alfabeto
    probabilidades = []
    for c in cadena:
        if c not in alfabeto and c != ' ':
            alfabeto.append(c)
            probabilidades.append(cadena.count(c)/long)
    
    return alfabeto, probabilidades

if __name__ == "__main__":
    print(GeneraAlfabetoYProb(cadena))

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