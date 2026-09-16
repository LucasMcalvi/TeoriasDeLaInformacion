import math
import random

fdp = [0.4, 0.3, 0.3]


def CalcInfo (fdp): #dado una lista de probabilidades genera una lista con la informacion obtenida en bits
    return [math.log2(1/p) for p in fdp]

info = CalcInfo(fdp)
if __name__ == "__main__":
    print(info)

def CalcEntropia (fdp): #dado una lista de probabilidades devuelve la entropia
    info = CalcInfo(fdp)
    return sum([p*i for p,i in zip(fdp,info)])

entropia = CalcEntropia(fdp)
if __name__ == "__main__":
    print(entropia)