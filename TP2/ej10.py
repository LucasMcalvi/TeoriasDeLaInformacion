import math
import random
import ej1

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


a,p = DevuelveExtyFdp(['x','y','z'], [0.5,0.1,0.4], 2)
print(a,p,sum(p),ej1.CalcEntropia(p),2*ej1.CalcEntropia([0.5,0.1,0.4]))