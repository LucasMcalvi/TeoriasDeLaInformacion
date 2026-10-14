import math
from Formulas import CalcEntropia, DevuelveExtyFdp
from FormulasCodificacion import get_longitudMedia, get_alfabetoCodigo

# Primer Teorema de Shannon:   H(S)  <=  Ln/N  <  H(S) + 1/N
#   H(S) = entropia de la fuente (en la base del codigo)
#   Ln   = longitud media de las palabras codigo de la extension
#   N    = orden de la extension

def cumple_shannon(probabilidades, palabras, N):
    # 1) Probabilidades de la extension de orden N.
    #    Cada simbolo de la extension es una combinacion de N simbolos de la fuente,
    #    y su probabilidad es el producto de las probabilidades de cada uno.
    prob_ext = [1]
    for i in range(N):
        prob_ext = [pe * p for pe in prob_ext for p in probabilidades]

    if len(palabras) != len(prob_ext):
        return False
    r = len(get_alfabetoCodigo(palabras))
    H = CalcEntropia(probabilidades) / math.log2(r)
    Ln = get_longitudMedia(palabras, prob_ext)
    return H <= Ln / N < H + 1 / N


def codigo_huffman(probabilidades): #devuelve una lista de palabras codigo binario
    """
    Algoritmo: cada simbolo arranca como un grupo. Se toman los dos grupos de
    menor probabilidad, al de menor probabilidad se le agrega un 0 y al otro un 1
    delante de los codigos de sus simbolos, y se los junta en un grupo nuevo cuya
    probabilidad es la suma. Se repite hasta que queda un solo grupo.

    Interpretación del resultado: devuelve una lista de palabras codigo binarias,
    una por cada probabilidad y en el mismo orden. Es un codigo instantaneo y
    compacto: los simbolos mas probables quedan con las palabras mas cortas.
    """

    #cada grupo es [probabilidad, [posiciones de los simbolos del grupo]]
    grupos = [[p, [i]] for i, p in enumerate(probabilidades)]
    codigos = ["" for p in probabilidades]

    while len(grupos) > 1:
        grupos.sort(key=lambda g: g[0])      #ordena de menor a mayor probabilidad
        menor = grupos.pop(0)                #los dos grupos de menor probabilidad
        siguiente = grupos.pop(0)

        for i in menor[1]:                   #agrega el bit adelante: 0 al menor, 1 al otro
            codigos[i] = "0" + codigos[i]
        for i in siguiente[1]:
            codigos[i] = "1" + codigos[i]

        grupos.append([menor[0] + siguiente[0], menor[1] + siguiente[1]])

    return codigos


def codigo_shannon_fano(probs): #devuelve una lista de palabras codigo binario
    """
    Algoritmo: cada simbolo es un item [probabilidad, codigo] con codigo vacio.
    Se ordenan los items de menor a mayor probabilidad y codificar() los va
    completando. Como los items son listas, los cambios se ven en la lista original.

    Interpretación del resultado: devuelve una lista de palabras codigo binarias,
    una por cada probabilidad y en el mismo orden. Es un codigo instantaneo pero
    no siempre optimo (puede quedar mas largo que el de Huffman).
    """
    items = [[p, ""] for p in probs]
    codificar(sorted(items))
    return [code for _, code in items]


def codificar(items):
    """
    Algoritmo: recibe items ordenados de menor a mayor probabilidad. Prueba todos
    los cortes posibles y se queda con el que deja menor diferencia entre la suma
    de probabilidades de los dos grupos. Al grupo de menor probabilidad le agrega
    un 0 al codigo y al de mayor probabilidad un 1, y se llama a si misma con
    cada grupo hasta que quede un solo item.

    Interpretación del resultado: no devuelve nada, completa el codigo de cada item.
    """
    if len(items) <= 1:
        return

    mejor_corte = 1
    mejor_diferencia = None

    for corte in range(1, len(items)):
        abajo = sum([p for p, _ in items[:corte]])
        arriba = sum([p for p, _ in items[corte:]])
        diferencia = abs(arriba - abajo)

        if mejor_diferencia is None or diferencia < mejor_diferencia:
            mejor_diferencia = diferencia
            mejor_corte = corte

    grupo_abajo = items[:mejor_corte]
    grupo_arriba = items[mejor_corte:]

    for item in grupo_abajo:
        item[1] += "0"
    for item in grupo_arriba:
        item[1] += "1"

    codificar(grupo_abajo)
    codificar(grupo_arriba)


if __name__ == "__main__":
    """
    P = [0.3, 0.1, 0.4, 0.2]
    codigo = ["BA", "CAB", "A", "CBA"]
    codigo_ext2, _ = DevuelveExtyFdp(codigo, P, 2)
    print(cumple_shannon(P, codigo, 1))           # True
    print(cumple_shannon(P, codigo_ext2, 2))    # False
    """
    P = [0.8, 0.2]
    codext3, prob_ext3 = DevuelveExtyFdp(["0", "1"], P, 3)
    codBin = codigo_huffman(prob_ext3)
    print(cumple_shannon(P, codBin, 3))
    print(dict(zip(codext3, codBin)))
