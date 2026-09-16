import math
import ej1



def CalculaEntropia (w): #calcula entropia memoria binaria pasandole w
    prob = [w, 1-w]
    return ej1.CalcEntropia(prob)

print(CalculaEntropia(1))