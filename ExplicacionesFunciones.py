"""
Guia de explicaciones para el examen.

Este archivo no realiza los calculos de los ejercicios. Cada funcion
`explicar_...` contiene, en su docstring, una explicacion lista para adaptar al
resultado obtenido. Al final se incluye `mostrarExplicacion`, que permite
imprimir cualquiera de los textos desde la terminal.

Convenciones importantes:
- Las matrices usan matriz[destino][origen] y cada columna suma 1.
- Las entropias de Formulas.py se expresan en bits.
- entropia_fuente expresa el resultado en base r del alfabeto codigo.
- Para una fuente con memoria de orden 1 corresponde usar su entropia de
  Markov, no solamente la entropia de las probabilidades marginales.
"""


# ============================================================================
# FORMULAS.PY
# ============================================================================


def explicar_CalcInfo():
    """
    Para obtener la informacion propia de cada simbolo recorri su distribucion
    de probabilidades y aplique I(si) = log2(1/P(si)). La funcion devuelve una
    lista paralela con los resultados en bits. Un valor mayor corresponde a un
    simbolo menos probable y, por lo tanto, mas sorpresivo. Las probabilidades
    nulas no se incluyen porque su informacion no puede calcularse mediante
    ese logaritmo.
    """


def explicar_CalcEntropia():
    """
    Para calcular la entropia obtuve la informacion propia de cada simbolo y
    calcule su promedio ponderado: H(S) = sumatoria P(si) log2(1/P(si)). El
    resultado se expresa en bits por simbolo y representa la incertidumbre
    promedio de la fuente. Esta funcion se utiliza directamente cuando la
    fuente es de memoria nula.
    """


def explicar_GeneraAlfabetoYProb():
    """
    Para obtener el alfabeto recorri el mensaje e identifique sus caracteres
    diferentes. Para cada simbolo conte sus apariciones y dividi el resultado
    por la longitud del mensaje: P(si) = N(si)/N. Finalmente ordene
    conjuntamente el alfabeto y las probabilidades para conservar la
    correspondencia entre las dos listas. La funcion devuelve ambas listas en
    paralelo.

    La implementacion no incluye el espacio en el alfabeto, aunque lo cuenta
    dentro de la longitud del mensaje. Esto no afecta a los mensajes que no
    contienen espacios.
    """


def explicar_GeneraPalabra():
    """
    Para generar una palabra construi la distribucion acumulada de
    probabilidades. En cada una de las N posiciones genere un numero aleatorio
    uniforme entre 0 y 1 y seleccione el simbolo cuyo intervalo acumulado lo
    contenia. Al repetir muchas veces el procedimiento, las frecuencias de los
    simbolos tienden a sus probabilidades. La funcion devuelve los simbolos
    seleccionados concatenados.
    """


def explicar_Equiprobables():
    """
    Si existen n sucesos equiprobables, cada uno tiene probabilidad 1/n. Al
    reemplazarla en la definicion de entropia se obtiene H(S) = log2(n). La
    funcion devuelve esa entropia maxima en bits por simbolo. Cuantas mas
    alternativas equiprobables existan, mayor sera la incertidumbre.
    """


def explicar_DevuelveExtyFdp():
    """
    Para construir la extension de orden N utilice recursion. El caso base de
    orden 1 es el alfabeto original. Para cada orden posterior combine cada
    palabra de la extension anterior con cada simbolo original. Como se trata
    de una fuente de memoria nula, calcule la probabilidad de cada secuencia
    multiplicando las probabilidades de sus componentes.

    La funcion devuelve el alfabeto extendido y sus probabilidades. Para
    calcular su entropia a partir de ellas se debe aplicar CalcEntropia a la
    nueva lista. Despues puede verificarse H(S^N) = N H(S). La funcion no debe
    usarse de esta forma para una fuente con memoria, porque sus simbolos no son
    independientes.
    """


def explicar_CalculaEntropiaMemoriaBinaria():
    """
    La funcion representa una fuente binaria con probabilidades w y 1-w y
    calcula H(w) = -w log2(w) - (1-w) log2(1-w). El resultado se expresa en
    bits por simbolo. Es maximo e igual a 1 cuando w = 0.5 y disminuye cuando
    una alternativa se vuelve mas probable que la otra.
    """


def explicar_generaalfabetoyTransicion():
    """
    Primero obtuve y ordene el alfabeto. Luego cree una matriz cuadrada de
    ceros y recorri todos los pares consecutivos del mensaje. Para cada par
    incremente matriz[simbolo siguiente][simbolo actual]. Finalmente normalice
    cada columna por la cantidad de transiciones desde su estado de origen.

    De esta forma, M[i][j] representa P(siguiente=i | actual=j): las filas son
    destinos, las columnas son origenes y cada columna suma 1.
    """


def explicar_transponer():
    """
    Para transponer la matriz intercambie filas por columnas, de modo que el
    elemento M[i][j] pase a la posicion M[j][i]. Esto permite convertir una
    matriz escrita como matriz[origen][destino] a la convencion utilizada por
    el proyecto: matriz[destino][origen].
    """


def explicar_generaVectorEstacionario():
    """
    Para aproximar el vector estacionario comence con una distribucion
    uniforme, con probabilidad 1/n en cada estado. Luego aplique treinta veces
    la relacion pi_nuevo = M pi. Si la cadena converge, el resultado se acerca
    a un vector que cumple M pi = pi y cuya suma es 1.

    Cada componente representa la probabilidad de encontrar la fuente en ese
    estado a largo plazo. Las pequeñas diferencias respecto de las fracciones
    exactas se deben al metodo iterativo y al uso de punto flotante.
    """


def explicar_calculaInfoCondicional():
    """
    Para obtener la informacion de una transicion aplique
    I(si | estado) = log2(1/P(si | estado)). El resultado se expresa en bits.
    Una transicion poco probable aporta mas informacion que una transicion
    frecuente. La probabilidad recibida debe ser mayor que cero y menor o igual
    que uno.
    """


def explicar_calculaEntropiaMarkovOrden1():
    """
    Para una fuente de Markov de orden 1 calcule la entropia de las
    transiciones que salen de cada estado y la pondere por la probabilidad
    estacionaria de ese estado:

        H(S) = sumatoria_j pi[j] H(siguiente | estado j).

    La matriz usa filas como destinos y columnas como origenes. Las
    transiciones de probabilidad cero no aportan. Si no se proporciona el
    vector estacionario, la funcion lo aproxima automaticamente. El resultado
    se expresa en bits por simbolo y considera que el simbolo siguiente depende
    del actual.

    Esta es la funcion que corresponde para una fuente con memoria de orden 1;
    no alcanza con calcular la entropia de sus probabilidades marginales.
    """


def explicar_calculaEntropiaMarkovOrdenM():
    """
    Para una fuente de orden m considere como estado de memoria cada secuencia
    formada por los ultimos m simbolos. Calcule la entropia de la distribucion
    del siguiente simbolo para cada estado y la pondere por la probabilidad de
    encontrarse en ese estado:

        H(S) = sumatoria_e P(e) H(siguiente | e).

    La primera lista contiene las probabilidades de los estados y la segunda
    una distribucion condicional por estado. El resultado se expresa en bits
    por simbolo.
    """


def explicar_tieneMemoriaNoNula():
    """
    Una fuente es de memoria nula si la distribucion del siguiente simbolo no
    depende del actual. Con la convencion usada, esto significa que las
    columnas de la matriz son iguales o aproximadamente iguales. La funcion
    recorre cada fila y compara sus valores entre columnas usando el elemento
    diagonal como referencia. Si alguna diferencia absoluta supera la
    tolerancia, devuelve True; de lo contrario devuelve False.

    True indica evidencia de memoria y False indica una fuente compatible con
    memoria nula. Una tolerancia grande puede ocultar memoria y una demasiado
    pequeña puede detectar variaciones muestrales. Si el enunciado no la fija,
    se debe indicar y justificar el valor elegido; para los mensajes trabajados
    puede utilizarse 0.01.
    """


def explicar_esFuenteErgodica():
    """
    Para determinar si la fuente es ergodica verifique que la cadena fuera
    irreducible y aperiodica. Interprete cada transicion positiva como una
    arista y recorri el grafo en sentido normal e inverso. Si no se alcanzan
    todos los estados en ambos recorridos, la cadena no es irreducible.

    Si es irreducible, la funcion calcula el periodo mediante el maximo comun
    divisor de las diferencias obtenidas a partir de las distancias y las
    aristas. El periodo debe ser 1 para que sea aperiodica. Devuelve True solo
    si se cumplen ambas condiciones. En una cadena finita, esto implica que el
    vector estacionario es unico y se alcanza desde cualquier estado inicial.
    """


def explicar_obtenerDatosSimbolo():
    """
    Para consultar uno o varios simbolos busque sus posiciones en el alfabeto y
    use los mismos indices en las listas paralelas. Antes verifique que todas
    las listas tuvieran la misma longitud para evitar asociaciones incorrectas.

    Para un simbolo devuelve su probabilidad o una tupla con los datos
    adicionales. Para una lista de simbolos devuelve una lista de resultados
    en el mismo orden. Las listas adicionales pueden contener informacion,
    longitudes u otros valores asociados.
    """


# ============================================================================
# FORMULASCODIFICACION.PY
# ============================================================================


def explicar_es_noSingular():
    """
    Para determinar si el codigo es no singular compare la cantidad total de
    palabras con la cantidad de palabras diferentes. Si coinciden, cada simbolo
    fuente tiene una palabra distinta y la funcion devuelve True. Si existe una
    palabra repetida, devuelve False y el codigo es singular.

    Ser no singular no garantiza decodificacion unica de concatenaciones; solo
    garantiza palabras distintas para simbolos individuales.
    """


def explicar_es_instantaneo():
    """
    Para verificar si el codigo es instantaneo compare todas sus palabras y
    comprobe que ninguna fuera prefijo de otra. Si existe un prefijo, es
    necesario seguir leyendo para reconocer el final de una palabra y la
    funcion devuelve False. Si no existe ninguno, devuelve True y cada palabra
    puede reconocerse apenas termina. Todo codigo instantaneo es tambien
    univocamente decodificable y no singular.
    """


def explicar_calcular_restos():
    """
    La funcion compara las palabras de dos conjuntos. Cuando una palabra del
    primero es prefijo de una del segundo, elimina ese prefijo y guarda el
    sufijo no vacio restante. Esos restos representan partes pendientes que
    podrian causar dos decodificaciones y se utilizan en Sardinas-Patterson. Un
    conjunto vacio indica que esa comparacion no genero nuevos restos.
    """


def explicar_es_univocamente_decodificable():
    """
    Para comprobar la decodificacion unica aplique Sardinas-Patterson. Primero
    obtuve los restos generados cuando una palabra es prefijo de otra. Luego
    combine sucesivamente esos restos con las palabras originales en ambos
    sentidos.

    Si un resto coincide con una palabra codigo, existe una cadena con dos
    decodificaciones y la funcion devuelve False. Si los restos se vacian o se
    repite una situacion anterior sin colision, devuelve True. Un resultado
    True garantiza separacion unica, aunque el codigo no sea necesariamente
    instantaneo.
    """


def explicar_get_alfabetoCodigo():
    """
    Para obtener el alfabeto codigo recorri todos los caracteres de las
    palabras, los agregue a un conjunto para eliminar repeticiones y finalmente
    los ordene. La cantidad de simbolos diferentes obtenida es la base r del
    codigo. Por ejemplo, el alfabeto {0, 1} tiene base 2.
    """


def explicar_get_longitudes():
    """
    Para obtener las longitudes recorri las palabras codigo y conte la cantidad
    de caracteres de cada una. La funcion devuelve una lista paralela: cada
    longitud ocupa la misma posicion que su palabra correspondiente.
    """


def explicar_calcular_kraft():
    """
    Primero obtuve la base r del alfabeto codigo y la longitud de cada palabra.
    Luego calcule K = sumatoria r^(-li). Si K > 1, no puede existir un codigo
    univocamente decodificable ni instantaneo con esas longitudes. Si K <= 1,
    las longitudes permiten construir algun codigo instantaneo, pero esto no
    demuestra que las palabras concretas recibidas lo sean.

    Para un codigo instantaneo, K = 1 indica un arbol completo y K < 1 indica
    que queda capacidad disponible.
    """


def explicar_entropia_fuente():
    """
    Para calcular la entropia en unidades del alfabeto codigo obtuve primero su
    base r a partir de los caracteres diferentes de las palabras. Luego
    aplique H_r(S) = sumatoria P(si) log_r(1/P(si)). Para un codigo binario el
    resultado esta en bits y para uno ternario esta en trits.

    Las palabras solamente se usan para determinar r; la entropia depende de
    las probabilidades. Esta funcion corresponde a problemas de codificacion de
    una fuente de memoria nula. Si solo se presenta un mensaje sin palabras
    codigo, se utiliza CalcEntropia para obtener bits.
    """


def explicar_get_longitudMedia():
    """
    Para obtener la longitud media pondere la longitud de cada palabra por la
    probabilidad del simbolo fuente que representa:

        L_media = sumatoria P(si) li.

    El resultado indica cuantos simbolos del alfabeto codigo se emiten, en
    promedio, por cada simbolo fuente. No se usa un promedio simple porque los
    simbolos pueden tener probabilidades diferentes.
    """


def explicar_es_compacto():
    """
    Primero verifique que el codigo fuera univocamente decodificable. Si no lo
    es, la funcion devuelve False. Si es univoco, obtuve la base r y comprobe
    para cada palabra que li <= techo(log_r(1/P(si))). Devuelve True solamente
    si se cumplen la decodificacion unica y todas las cotas de longitud.

    Un resultado False puede deberse a una ambiguedad o a que alguna palabra
    sea mas larga de lo permitido por el criterio de compacidad.
    """


def explicar_generar_mensaje():
    """
    Para generar el mensaje seleccione N palabras de manera aleatoria e
    independiente usando sus probabilidades como pesos. Luego concatene las
    palabras elegidas. El resultado representa N simbolos fuente codificados,
    aunque la cantidad de caracteres puede variar si las palabras tienen
    longitudes diferentes. En muchas generaciones, las frecuencias tienden a
    las probabilidades dadas.
    """


def explicar_clasifica():
    """
    La clasificacion es jerarquica. Primero comprobe que todas las palabras
    fueran distintas. Si ademas ninguna es prefijo de otra, el codigo se
    clasifica como instantaneo. Si hay prefijos, aplique Sardinas-Patterson: si
    no encuentra ambiguedades se clasifica como univoco y, en caso contrario,
    como no singular. Si existen palabras repetidas, el codigo es singular.

    La relacion es: instantaneo implica univocamente decodificable, que a su vez
    implica no singular.

    ADVERTENCIA: la implementacion actual devuelve el texto "bloque" cuando
    detecta palabras repetidas. La propiedad matematica detectada es
    "singular". Un codigo de bloque es uno cuyas palabras tienen igual longitud
    y es una propiedad diferente.
    """


# ============================================================================
# CONCLUSIONES GENERALES LISTAS PARA ADAPTAR
# ============================================================================


def explicar_resultado_memoria_nula():
    """
    Las columnas de la matriz resultaron iguales o sus diferencias no superaron
    la tolerancia elegida. Por lo tanto, la distribucion del siguiente simbolo
    no depende del anterior y la fuente se estimo como de memoria nula. Su
    entropia se calculo directamente desde las probabilidades marginales con
    CalcEntropia.
    """


def explicar_resultado_con_memoria():
    """
    Las columnas de la matriz presentaron diferencias superiores a la
    tolerancia. Por lo tanto, la distribucion del siguiente simbolo depende del
    actual y la fuente se estimo como de memoria de orden 1. Se obtuvo su vector
    estacionario y se calculo la entropia condicional promedio con
    calculaEntropiaMarkovOrden1.
    """


def explicar_resultado_codigo_instantaneo():
    """
    Ninguna palabra resulto prefijo de otra, por lo que cada una puede
    reconocerse apenas termina. El codigo es instantaneo y, en consecuencia,
    tambien es univocamente decodificable y no singular.
    """


def explicar_resultado_codigo_univoco():
    """
    Se encontraron relaciones de prefijo, por lo que el codigo no es
    instantaneo. Sin embargo, Sardinas-Patterson no encontro ambiguedades y por
    eso el codigo es univocamente decodificable.
    """


def explicar_resultado_codigo_no_singular():
    """
    Todas las palabras son diferentes, por lo que el codigo es no singular.
    Sin embargo, Sardinas-Patterson encontro una concatenacion con dos
    decodificaciones; por eso no es univocamente decodificable ni instantaneo.
    """


def explicar_resultado_codigo_singular():
    """
    Al menos dos simbolos fuente tienen asignada la misma palabra. Por lo
    tanto, no es posible distinguirlos ni siquiera al codificar un solo simbolo
    y el codigo es singular. En consecuencia, tampoco es univocamente
    decodificable ni instantaneo.
    """


def mostrarExplicacion(nombre_funcion):
    """
    Imprime la explicacion asociada a una funcion real.

    Ejemplo:
        mostrarExplicacion("CalcEntropia")
        mostrarExplicacion("calcular_kraft")
    """
    nombre_explicacion = "explicar_" + nombre_funcion
    funcion = globals().get(nombre_explicacion)

    if funcion is None or not callable(funcion):
        raise ValueError(
            f"No existe una explicacion para {nombre_funcion!r}."
        )

    print(funcion.__doc__.strip())


def listarExplicaciones():
    """Devuelve los nombres de todas las explicaciones disponibles."""
    prefijo = "explicar_"
    return sorted(
        nombre[len(prefijo):]
        for nombre, valor in globals().items()
        if nombre.startswith(prefijo) and callable(valor)
    )

