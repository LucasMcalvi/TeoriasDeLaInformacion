
import math
import random

probabilidades =[0.15,0.25,0.05,0.45,0.1]
palabras= ["/+","*","+-","-","*/"]
palabras2 =["(]","]","[)",")","(["]
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
def get_longitudes(palabras):
    """
    Calcula la longitud de cada palabra codigo.
    Recibe una lista de palabras codigo y devuelve una lista de enteros.
    Usa una comprension de listas para aplicar len() a cada palabra.

    Algoritmo: determina cuántos símbolos contiene cada palabra código.

    Interpretación del resultado: devuelve una lista paralela a la entrada; cada
    número es la longitud de la palabra ubicada en la misma posición. Valores
    mayores representan palabras que requieren más símbolos para transmitirse.
    """
    return [len(palabra) for palabra in palabras]
def get_alfabetoCodigo(palabras):
    """
    Obtiene el alfabeto codigo utilizado por las palabras recibidas.
    Recibe una lista de palabras codigo y devuelve una cadena con sus
    caracteres sin repetir y ordenados. Agrega los caracteres a un set,
    los ordena con sorted() y los une con join().

    Algoritmo: reúne todos los símbolos usados por las palabras código, elimina
    repeticiones y los ordena para formar el alfabeto del código.

    Interpretación del resultado: devuelve una cadena con cada símbolo del
    alfabeto exactamente una vez. Su longitud es la base del código; una cadena
    vacía indica que no se recibió ningún símbolo utilizable.
    """

    #update(palabra) agrega al conjunto cada carácter de la palabra, sin repetirlos. Luego sorted() los ordena y join() los une en una cadena.

    alfabeto = set()

    for palabra in palabras:
        alfabeto.update(palabra)

    return "".join(sorted(alfabeto))



def get_longitudMedia(palabras, probabilidades):
    """
    Algoritmo: pondera la longitud de cada palabra código por su probabilidad de
    aparición y suma todos esos aportes.

    Interpretación del resultado: devuelve la cantidad promedio de símbolos de
    código necesarios por símbolo fuente. Cuanto menor sea el valor, más corta
    será en promedio la representación, si se comparan códigos válidos.
    """

    #calcula la longitud media del codigo

    return sum([p*len(palabra) for palabra, p in zip (palabras, probabilidades)])
def calcular_kraft(palabras):
    """
    Calcula la sumatoria de la inecuacion de Kraft.
    Recibe una lista de palabras codigo y devuelve el valor de la suma.
    Obtiene la base r del alfabeto y suma r elevado a la longitud negativa
    de cada palabra.

    Algoritmo: obtiene la base r del alfabeto del código y suma r elevado al
    negativo de la longitud de cada palabra, según la inecuación de Kraft.

    Interpretación del resultado: una suma menor o igual que 1 cumple Kraft y
    permite que exista un código instantáneo con esas longitudes; una suma mayor
    que 1 lo hace imposible. El valor 1 indica que el árbol de código está lleno.
    """
    alfabeto = get_alfabetoCodigo(palabras)
    L = get_longitudes(palabras)
    r = len(alfabeto)

    if r == 0:
        return 0

    return sum(r ** -longitud for longitud in L)

def es_noSingular(codigo): #devuelve si un codigo es no singular
    """
    Algoritmo: compara la cantidad total de palabras código con la cantidad de
    palabras distintas para comprobar si existen repeticiones.

    Interpretación del resultado: True significa que cada símbolo fuente tiene
    una palabra código diferente; False significa que al menos dos comparten la
    misma palabra y no pueden distinguirse al decodificar.
    """
    return len(codigo) == len(set(codigo))

def es_instantaneo(palabras):
    """
    Algoritmo: compara todas las palabras entre sí y comprueba que ninguna sea
    prefijo de otra palabra más larga.

    Interpretación del resultado: True indica que el código es instantáneo y
    cada palabra puede reconocerse apenas termina; False indica que hace falta
    leer más símbolos para decidir si una palabra ya terminó.
    """
    n = len(palabras)
    for i in range(n):
        for j in range(n):
            if i != j:
                if palabras[j].startswith(palabras[i]): #En Python, "cadena_larga".startswith("cadena_corta") devuelve True si la cadena corta es efectivamente el prefijo inicial de la larga.
                    return False
    return True





def calcular_restos(conjunto_a, conjunto_b):
    """
    Compara cada elemento de conjunto_a contra cada elemento de
    conjunto_b. Si uno es prefijo del otro (y no son iguales),
    guarda el resto (la parte que sobra) en un set nuevo.
    usada para sardinas-patterson

    Algoritmo: compara las palabras de ambos conjuntos y, cuando una palabra
    del primero es prefijo de una del segundo, conserva la parte que queda
    pendiente. Estos restos se usan en el algoritmo de Sardinas-Patterson.

    Interpretación del resultado: devuelve el conjunto de sufijos no vacíos que
    todavía podrían provocar una ambigüedad. Un conjunto vacío significa que
    esta comparación no produjo restos pendientes.
    """
    restos = set()
    for a in conjunto_a:
        for b in conjunto_b:
            if a == b:
                continue
            if b.startswith(a):
                resto = b[len(a):]
                if resto:  # descartamos el resto vacio (a == b ya se filtro)
                    restos.add(resto)
    return restos

def es_univocamente_decodificable(palabras,mostrar = False):
    """
    Implementa el algoritmo de Sardinas-Patterson.

    Idea: si una palabra A es prefijo de otra palabra B, el "resto"
    de B (lo que sobra despues de sacarle el prefijo A) queda como
    una secuencia "colgando". Si ese resto eventualmente coincide
    con una palabra codigo original, significa que se puede armar
    la misma secuencia de bits/simbolos de dos formas distintas
    a partir de los simbolos fuente -> el codigo NO es univoco.

    Pasos:
      1. Calculamos C1: todos los restos que salen de comparar
         las palabras originales entre si.
      2. Iteramos generando C2, C3, ... combinando los restos
         del paso anterior con las palabras originales.
      3. Cortamos si:
         - un resto coincide con una palabra original -> NO univoco
         - el conjunto de restos queda vacio -> SI univoco
         - el conjunto de restos ya aparecio antes (ciclo) -> SI univoco

    Algoritmo: aplica Sardinas-Patterson. Genera los sufijos que quedan cuando
    una palabra es prefijo de otra y los combina sucesivamente con las palabras
    originales hasta hallar una colisión, quedarse sin restos o entrar en ciclo.

    Interpretación del resultado: True significa que toda cadena codificada
    admite una única separación en palabras código. False significa que existe
    al menos una cadena que puede decodificarse de dos maneras diferentes.
    """
    
    if not es_noSingular(palabras):
        if mostrar:
            print("   Hay palabras repetidas: el codigo es singular -> NO univoco")
        return False

    palabras_set = set(palabras)
    c_actual = calcular_restos(palabras, palabras)   # C1
    historial = [c_actual]
    n = 1

    while True:
        if mostrar:
            print(f"   C{n} = {sorted(c_actual) if c_actual else 'vacio'}")

        if c_actual & palabras_set:
            if mostrar:
                print(f"   C{n} contiene la palabra {sorted(c_actual & palabras_set)} -> NO univoco")
            return False

        if not c_actual:
            if mostrar:
                print(f"   C{n} es vacio -> univoco")
            return True

        siguiente = calcular_restos(c_actual, palabras) | calcular_restos(palabras, c_actual)

        if siguiente in historial:
            if mostrar:
                print(f"   C{n+1} = {sorted(siguiente)} ya aparecio antes (ciclo) -> univoco")
            return True

        historial.append(siguiente)
        c_actual = siguiente
        n += 1
        
def entropia_fuente(palabras, probabilidades):
    """
    Algoritmo: calcula el promedio de información de los símbolos fuente usando
    como base logarítmica la cantidad de símbolos del alfabeto del código.

    Interpretación del resultado: mide la incertidumbre en símbolos del alfabeto
    código por símbolo fuente. Un valor bajo describe una fuente predecible y
    uno alto una fuente menos predecible; el máximo ocurre con probabilidades
    uniformes. Las probabilidades nulas no aportan a la entropía.
    """

    #calcula la entropia de la fuente a partir de una lista de  palabras codigo de una codificacion y sus probabilidades

    set_palabras = set("".join(palabras))
    base = len(set_palabras)

    return sum([p*math.log(1/p, base) for p in probabilidades if p>0])

def es_compacto(palabras, probabilidades):
    """
    Algoritmo: primero exige que el código sea unívocamente decodificable y luego
    verifica que la longitud de cada palabra no supere el entero superior de su
    información propia, expresada en la base del alfabeto código.

    Interpretación del resultado: True indica que el código satisface el criterio
    de compacidad implementado; False indica que es ambiguo o que al menos una
    palabra resulta más larga de lo permitido por ese criterio.
    """

    #Devuelve True si es compacto o False si no lo es

    if (es_univocamente_decodificable(palabras)):
        base = len(set("".join(palabras)))

        for palabra, p in zip(palabras, probabilidades):
            if not len(palabra) <= math.ceil(math.log(1/p, base)):
                return False

        return True
    else:
        return False
def entropia_fuente(palabras, probabilidades):
    """
    Algoritmo: calcula el promedio de información de los símbolos fuente usando
    como base logarítmica la cantidad de símbolos del alfabeto del código.

    Interpretación del resultado: mide la incertidumbre en símbolos del alfabeto
    código por símbolo fuente. Un valor bajo describe una fuente predecible y
    uno alto una fuente menos predecible; el máximo ocurre con probabilidades
    uniformes. Las probabilidades nulas no aportan a la entropía.
    """

    #calcula la entropia de la fuente a partir de una lista de  palabras codigo de una codificacion y sus probabilidades

    set_palabras = set("".join(palabras))
    base = len(set_palabras)

    return sum([p*math.log(1/p, base) for p in probabilidades if p>0])


def clasifica(codigo):
    """
    Algoritmo: clasifica el código en forma jerárquica: comprueba si sus palabras
    son distintas, después si ninguna es prefijo de otra y, por último, si puede
    decodificarse de manera única mediante Sardinas-Patterson.

    Interpretación del resultado: "instantáneo" es la categoría más restrictiva;
    "unívoco" permite decodificación única pero no inmediata; "no singular" solo
    garantiza palabras distintas; y "bloque" indica que hay palabras repetidas.
    """
    if es_noSingular(codigo):
            if es_instantaneo(codigo):
                return "instantáneo"
            else:
                if es_univocamente_decodificable(codigo):
                    return "unívoco"
                else:
                    return "no singular"
    else:
            return "bloque"

"""""
print("longitud media",get_longitudMedia(palabras,probabilidades))
print (" el codigo es ",clasifica(palabras))
print("entropia fuente con base r ",entropia_fuente(palabras,probabilidades))
print("Inecuacion de Kraft",calcular_kraft(palabras))
if es_univocamente_decodificable(palabras,True):  #True para mostrar
    if es_compacto(palabras, probabilidades):
        print("es compacto")
    else:
        print("no es compacto")
else:
    print("no es compacto porque no es univoco")
"""
alfabeto = get_alfabetoCodigo(palabras)
kraft = calcular_kraft(palabras)
print("===== Codigo", palabras, "=====")
print("Alfabeto codigo:", list(alfabeto), " r =", len(alfabeto))
print("Longitudes:", get_longitudes(palabras))
print("Entropia de la fuente (base r):", round(entropia_fuente(palabras, probabilidades), 4))
print("Longitud media:", round(get_longitudMedia(palabras, probabilidades), 4))
print("Inecuacion de Kraft-McMillan:", round(kraft, 4), "<= 1, se cumple" if kraft <= 1 else "> 1, no se cumple")
print("Clasificacion:", clasifica(palabras))
print("Sardinas-Patterson:")
univoco = es_univocamente_decodificable(palabras, True)
if not univoco:
    print("Compacto: no, porque no es univocamente decodificable")
elif es_compacto(palabras, probabilidades):
    print("Compacto: si")
else:
    print("Compacto: no, alguna palabra supera techo(log_r(1/p))")
print()