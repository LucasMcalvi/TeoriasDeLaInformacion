import math
import PrimerParcial.FormulasCodificacion as FormulasCodificacion
import PrimerParcial.Formulas as Formulas

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

def entropia_fuente(palabras, probabilidades):

    #calcula la entropia de la fuente a partir de una lista de  palabras codigo de una codificacion y sus probabilidades

    set_palabras = set("".join(palabras))
    base = len(set_palabras)

    return sum([p*math.log(1/p, base) for p in probabilidades if p>0])

def calcular_kraft(palabras):

    alfabeto = get_alfabetoCodigo(palabras)
    L = get_longitudes(palabras)
    r = len(alfabeto)

    if r == 0:
        return 0

    return sum(r ** -longitud for longitud in L)

def get_longitudes(palabras):

    return [len(palabra) for palabra in palabras]

def get_alfabetoCodigo(palabras):

    #update(palabra) agrega al conjunto cada carácter de la palabra, sin repetirlos. Luego sorted() los ordena y join() los une en una cadena.

    alfabeto = set()

    for palabra in palabras:
        alfabeto.update(palabra)

    return "".join(sorted(alfabeto))

def es_univocamente_decodificable(palabras, mostrar=False):

    if not es_noSingular(palabras):
        if mostrar:
            print("   Hay palabras repetidas: el codigo es singular -> NO univoco")
        return False

    palabras_set = set(palabras)
    if "" in palabras_set:
        if mostrar:
            print("   Hay una palabra vacia -> NO univoco")
        return False

    # Paso 1: C1 = restos de comparar las palabras originales entre si
    c_actual = calcular_restos(palabras, palabras)
    historial = [c_actual]
    n = 1

    while True:
        if mostrar:
            print(f"   C{n} = {sorted(c_actual) if c_actual else 'vacio'}")

        # Condicion de NO univoco: algun resto coincide con una palabra original
        if c_actual & palabras_set:
            if mostrar:
                print(f"   C{n} contiene la palabra {sorted(c_actual & palabras_set)} -> NO univoco")
            return False

        # Condicion de SI univoco: no quedan mas restos por resolver
        if not c_actual:
            if mostrar:
                print(f"   C{n} es vacio -> univoco")
            return True

        # Generamos el siguiente conjunto de restos:
        # combinamos los restos actuales con las palabras originales
        # en ambas direcciones (resto vs palabra, y palabra vs resto)
        siguiente = calcular_restos(c_actual, palabras) | calcular_restos(palabras, c_actual)

        # Condicion de SI univoco: si este conjunto ya aparecio antes,
        # estamos en un ciclo que nunca va a generar una colision real
        if siguiente in historial:
            if mostrar:
                print(f"   C{n+1} = {sorted(siguiente)} ya aparecio antes (ciclo) -> univoco")
            return True

        historial.append(siguiente)
        c_actual = siguiente
        n += 1

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

codigo = ["CA", "C", "AB", "BC", "A"]
prob = [1/9, 1/3, 1/9, 1/9, 1/3]

kraft = calcular_kraft(codigo)
entropia = entropia_fuente(codigo, prob)
longitudMedia = get_longitudMedia(codigo, prob)
compacto = es_compacto(codigo, prob)

print(kraft)
print(entropia)
print(longitudMedia)
print("Compacto: ", compacto)
print(es_univocamente_decodificable(codigo, False))

codigocompacto = ["BA", "C", "BB", "BC", "A"]
probC = [1/9, 1/3, 1/9, 1/9, 1/3]

print("Compacto: ", es_compacto(codigocompacto, probC))
print("univoco: ", es_univocamente_decodificable(codigocompacto, False))