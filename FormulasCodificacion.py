#CODIFICACION
import math
import random
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

def es_univocamente_decodificable(palabras):
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

    palabras_set = set(palabras)



    # Paso 1: C1 = restos de comparar las palabras originales entre si
    c_actual = calcular_restos(palabras, palabras)

    historial = [c_actual]

    while True:
        # Condicion de NO univoco: algun resto coincide con una palabra original
        if c_actual & palabras_set:
            return False

        # Condicion de SI univoco: no quedan mas restos por resolver
        if not c_actual:
            return True

        # Generamos el siguiente conjunto de restos:
        # combinamos los restos actuales con las palabras originales
        # en ambas direcciones (resto vs palabra, y palabra vs resto)
        siguiente = calcular_restos(c_actual, palabras) | calcular_restos(palabras, c_actual)

        # Condicion de SI univoco: si este conjunto ya aparecio antes,
        # estamos en un ciclo que nunca va a generar una colision real
        if siguiente in historial:
            return True

        historial.append(siguiente)
        c_actual = siguiente



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

def generar_mensaje(N, palabras, probabilidades):
    """
    Algoritmo: realiza N elecciones aleatorias independientes entre las palabras
    código, usando sus probabilidades como pesos, y concatena las elegidas.

    Interpretación del resultado: devuelve un mensaje codificado formado por N
    palabras, aunque su longitud total puede variar si estas tienen longitudes
    distintas. En muchas generaciones, sus frecuencias deberían aproximarse a
    las probabilidades indicadas.
    """

    #Dado un N, una lista de palabras codigo de una codificacion y sus probabbilidades, genera aleatoriamente un posible mensaje de N símbolos codificados emitido por dicha fuente

    elegidas = random.choices(
        palabras,
        weights=probabilidades,
        k=N
    )
    return "".join(elegidas)

#A random.choises le pasas la lista con las palabras, para que tenga los elementos a elegir
# el peso de cada elemento
# Y un k que dice cuantas elecciones realiza, en este caso N
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
