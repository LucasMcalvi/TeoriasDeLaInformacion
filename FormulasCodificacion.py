#CODIFICACION
import math
def es_noSingular(codigo): #devuelve si un codigo es no singular
    return len(codigo) == len(set(codigo))

def es_instantaneo(palabras):
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
    """
    return [len(palabra) for palabra in palabras]


def calcular_kraft(palabras):
    """
    Calcula la sumatoria de la inecuacion de Kraft.
    Recibe una lista de palabras codigo y devuelve el valor de la suma.
    Obtiene la base r del alfabeto y suma r elevado a la longitud negativa
    de cada palabra.
    """
    alfabeto = get_alfabetoCodigo(palabras)
    L = get_longitudes(palabras)
    r = len(alfabeto)

    if r == 0:
        return 0

    return sum(r ** -longitud for longitud in L)

def entropia_fuente(palabras, probabilidades):

    #calcula la entropia de la fuente a partir de una lista de  palabras codigo de una codificacion y sus probabilidades

    set_palabras = set("".join(palabras))
    base = len(set_palabras)

    return sum([p*math.log(1/p, base) for p in probabilidades if p>0])

def get_longitudMedia(palabras, probabilidades):

    #calcula la longitud media del codigo

    return sum([p*len(palabra) for palabra, p in zip (palabras, probabilidades)])

def es_compacto(palabras, probabilidades):

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