"""
Func_clase6.py
==============
Funciones de Python para el TP6 de Teoría de la Información (clase 6):
Canales para la transmisión de información.

Cada función tiene un docstring con: qué es, para qué se usa y cómo
interpretar el resultado. Se puede ver con help(nombre_funcion).

Convención para todas las funciones
-----------------------------------
- probs: lista de probabilidades a priori P(a_i) de los símbolos de entrada.
- matriz: matriz del canal como lista de filas. matriz[i][j] = P(b_j / a_i):
  cada fila es una entrada a_i, cada columna una salida b_j, y cada fila
  suma 1.
- Las matrices que se devuelven (a posteriori, eventos simultáneos) tienen
  la misma forma: filas = entradas, columnas = salidas.
- Los índices de columnas empiezan en 0 (como en Python).
- Todas las entropías se expresan en bits.

Índice (ejercicio de la guía -> función)
-----------------------------------------
Ej. 2   matriz_canal                  (+ canal_desde_secuencias)
Ej. 7a  probabilidades_salida
Ej. 7b  probabilidades_a_posteriori
Ej. 7c  probabilidades_simultaneas
Ej. 11  entropias_a_posteriori
Ej. 15a equivocacion
Ej. 15b perdida
Ej. 15c entropia_afin
Ej. 15d informacion_mutua
Ej. 18a es_sin_ruido
Ej. 18b es_determinante
Ej. 20  canal_serie
Ej. 22a es_reduccion_suficiente
Ej. 22b matriz_determinante_reduccion
Ej. 23  reducir_canal
Ej. 25a es_uniforme
Ej. 25b capacidad_canal
Ej. 26  capacidad_binaria
Ej. 30  probabilidad_error

Herramienta de apoyo para los ejercicios teóricos
-------------------------------------------------
Ej. 14, 16, 17, 19, 21  analisis_canal (todas las entropías y sus relaciones)

Reutiliza funciones ya desarrolladas (tienen que estar en la misma carpeta):
  Formulas.py  CalcEntropia, GeneraAlfabetoYProb
Solo se usan las librerías math y random (esta última, a través de Formulas).
"""

import math
from Formulas import CalcEntropia, GeneraAlfabetoYProb

_TOL = 1e-9


# ---------------------------------------------------------------------------
# Validaciones internas
# ---------------------------------------------------------------------------
def _validar_matriz(matriz):
    if not matriz or not matriz[0]:
        raise ValueError("La matriz del canal está vacía.")
    s = len(matriz[0])
    for i, fila in enumerate(matriz):
        if len(fila) != s:
            raise ValueError("Todas las filas de la matriz deben tener la misma cantidad de columnas.")
        if any(p < -1e-9 or p > 1 + 1e-9 for p in fila):  # tolera redondeos (1.0000000000000002)
            raise ValueError(f"La fila {i} tiene valores fuera de [0, 1].")
        if abs(sum(fila) - 1) > 1e-6:
            raise ValueError(f"La fila {i} suma {sum(fila)}; cada fila debe sumar 1.")


def _validar_canal(probs, matriz):
    _validar_matriz(matriz)
    if len(probs) != len(matriz):
        raise ValueError("Debe haber una probabilidad a priori por cada fila de la matriz.")
    if any(p < 0 for p in probs) or abs(sum(probs) - 1) > 1e-6:
        raise ValueError("Las probabilidades a priori deben ser no negativas y sumar 1.")


def _columna(matriz, j):
    return [fila[j] for fila in matriz]


# ---------------------------------------------------------------------------
# Ejercicio 2: matriz del canal a partir de secuencias
# ---------------------------------------------------------------------------
def canal_desde_secuencias(entrada, salida):
    """
    Qué es:
        A partir de una secuencia de entrada y la secuencia de salida que
        produjo el canal, obtiene todo lo que describe al canal: los
        alfabetos de entrada y salida, las probabilidades a priori y la
        matriz del canal.

    Para qué se usa:
        Para los ejercicios 1, 3, 8 y 9 y para el ejercicio 2 del parcial,
        donde el canal se conoce solo por su comportamiento observado.

    Cómo interpretar el resultado:
        Devuelve (alfabeto_A, probs, alfabeto_B, matriz):
        - alfabeto_A y alfabeto_B están ordenados; las filas de la matriz
          siguen el orden de alfabeto_A y las columnas el de alfabeto_B.
        - probs[i] es la frecuencia relativa de a_i en la entrada.
        - matriz[i][j] es la fracción de veces que, habiendo entrado a_i,
          salió b_j: P(b_j / a_i).
        - Una fila con un único valor distinto de cero indica que esa
          entrada siempre produce la misma salida; filas muy repartidas
          indican mucho ruido para esa entrada.

    Parámetros:
        entrada, salida: strings de igual longitud (el carácter k de la
                         salida es lo que salió al entrar el carácter k).
    """
    if len(entrada) != len(salida):
        raise ValueError("Las secuencias de entrada y salida deben tener la misma longitud.")
    if not entrada:
        raise ValueError("Las secuencias están vacías.")
    alfabeto_a, probs = GeneraAlfabetoYProb(entrada)
    alfabeto_b = sorted(set(salida))
    matriz = []
    for a in alfabeto_a:
        salidas_de_a = [b for x, b in zip(entrada, salida) if x == a]
        matriz.append([salidas_de_a.count(b) / len(salidas_de_a) for b in alfabeto_b])
    return alfabeto_a, probs, alfabeto_b, matriz


def matriz_canal(entrada, salida):
    """
    Qué es:
        Matriz del canal P(b_j / a_i) obtenida a partir de una secuencia de
        entrada y su secuencia de salida (ejercicio 2).

    Para qué se usa:
        Para caracterizar un canal a partir de su comportamiento observado.
        Con la matriz se calcula todo lo demás (probabilidades de salida, a
        posteriori, entropías, información mutua).

    Cómo interpretar el resultado:
        - Filas = símbolos de entrada (ordenados), columnas = símbolos de
          salida (ordenados). Cada fila suma 1.
        - matriz[i][j] es la probabilidad de que salga b_j cuando entra a_i.
        - Valores 1 en la "diagonal" y 0 en el resto: canal perfecto.
          Filas iguales entre sí: la salida no depende de la entrada (el
          canal no transmite información).
        - Para obtener también los alfabetos y las probabilidades a priori,
          usar canal_desde_secuencias.

    Parámetros:
        entrada, salida: strings de igual longitud.
    Devuelve:
        lista de listas.
    """
    return canal_desde_secuencias(entrada, salida)[3]


# ---------------------------------------------------------------------------
# Ejercicio 7: probabilidades de salida, a posteriori y simultáneas
# ---------------------------------------------------------------------------
def probabilidades_salida(probs, matriz):
    """
    Qué es:
        Probabilidad de cada símbolo de salida:
        P(b_j) = sum_i P(a_i) * P(b_j / a_i).

    Para qué se usa:
        Para conocer qué se observa a la salida del canal, y como paso previo
        para las probabilidades a posteriori y la entropía de la salida H(B).

    Cómo interpretar el resultado:
        - Lista con una probabilidad por columna de la matriz; suma 1.
        - Si el canal no tiene ruido, se parece a la distribución de
          entrada; cuanto más ruido, más se "mezcla".
        - Un valor 0 indica una salida que nunca aparece.

    Parámetros:
        probs: probabilidades a priori.
        matriz: matriz del canal.
    Devuelve:
        list.
    """
    _validar_canal(probs, matriz)
    s = len(matriz[0])
    return [sum(probs[i] * matriz[i][j] for i in range(len(probs))) for j in range(s)]


def probabilidades_simultaneas(probs, matriz):
    """
    Qué es:
        Probabilidades de los eventos simultáneos:
        P(a_i, b_j) = P(a_i) * P(b_j / a_i), es decir, la probabilidad de
        que entre a_i y salga b_j.

    Para qué se usa:
        Es la base de las entropías del canal (equivocación, pérdida,
        entropía afín, información mutua).

    Cómo interpretar el resultado:
        - Matriz con filas = entradas y columnas = salidas; la suma de TODOS
          los valores es 1.
        - Sumar una fila da P(a_i); sumar una columna da P(b_j).
        - Si cada fila y cada columna tienen un solo valor distinto de cero,
          la salida identifica exactamente a la entrada.

    Parámetros:
        probs: probabilidades a priori.
        matriz: matriz del canal.
    Devuelve:
        lista de listas.
    """
    _validar_canal(probs, matriz)
    return [[probs[i] * p for p in fila] for i, fila in enumerate(matriz)]


def probabilidades_a_posteriori(probs, matriz):
    """
    Qué es:
        Probabilidades a posteriori P(a_i / b_j): la probabilidad de que
        haya entrado a_i sabiendo que salió b_j (teorema de Bayes):
        P(a_i / b_j) = P(a_i) * P(b_j / a_i) / P(b_j).

    Para qué se usa:
        Para saber qué se puede deducir de la entrada al observar la salida.
        Es la base de las entropías a posteriori, la equivocación y la regla
        de decisión de máxima posibilidad.

    Cómo interpretar el resultado:
        - Matriz con filas = entradas y columnas = salidas; cada COLUMNA
          suma 1 (dado que salió b_j, alguna entrada tuvo que ser).
        - Una columna con un 1 y el resto 0: al ver esa salida se sabe con
          certeza qué entró.
        - Una columna igual a las probabilidades a priori: esa salida no
          aporta nada sobre la entrada.
        - Si una salida tiene P(b_j) = 0 su columna queda en 0 (no está
          definida porque nunca ocurre).

    Parámetros:
        probs: probabilidades a priori.
        matriz: matriz del canal.
    Devuelve:
        lista de listas.
    """
    conjunta = probabilidades_simultaneas(probs, matriz)
    salida = probabilidades_salida(probs, matriz)
    return [[conjunta[i][j] / salida[j] if salida[j] > 0 else 0.0
             for j in range(len(salida))] for i in range(len(probs))]


# ---------------------------------------------------------------------------
# Ejercicio 11: entropías a posteriori
# ---------------------------------------------------------------------------
def entropias_a_posteriori(probs, matriz):
    """
    Qué es:
        Entropía a posteriori de la entrada para cada símbolo de salida:
        H(A / b_j) = sum_i P(a_i / b_j) * log2(1 / P(a_i / b_j)).

    Para qué se usa:
        Para medir cuánta incertidumbre sobre la entrada queda después de
        observar cada salida, y compararla con la entropía a priori H(A)
        (se calcula con CalcEntropia(probs)).

    Cómo interpretar el resultado:
        - Lista con un valor por símbolo de salida.
        - H(A / b_j) = 0: al recibir b_j se sabe con certeza qué entró.
        - H(A / b_j) < H(A): recibir b_j reduce la incertidumbre.
        - H(A / b_j) > H(A) es posible: una salida puntual puede dejar más
          dudas que antes de recibirla. Lo que nunca puede pasar es que el
          PROMEDIO (la equivocación H(A/B)) supere a H(A).
        - Una salida con P(b_j) = 0 da 0 (nunca ocurre).

    Parámetros:
        probs: probabilidades a priori.
        matriz: matriz del canal.
    Devuelve:
        list.
    """
    post = probabilidades_a_posteriori(probs, matriz)
    return [CalcEntropia(_columna(post, j)) for j in range(len(matriz[0]))]


# ---------------------------------------------------------------------------
# Ejercicio 15: entropías del canal por definición
# ---------------------------------------------------------------------------
def equivocacion(probs, matriz):
    """
    Qué es:
        Equivocación o ruido del canal, calculada por definición:
        H(A/B) = sum_{a,b} P(a,b) * log2(1 / P(a/b)).

    Para qué se usa:
        Mide la información sobre la entrada que el canal NO deja pasar: la
        incertidumbre que queda sobre A después de observar B.

    Cómo interpretar el resultado:
        - 0: canal sin ruido; mirando la salida se sabe siempre qué entró.
        - Igual a H(A): la salida no dice nada de la entrada (entrada y
          salida independientes); no pasa información.
        - Valores intermedios: parte de la información se pierde. Cuanto
          más cerca de 0, mejor el canal.
        - Siempre 0 <= H(A/B) <= H(A).

    Parámetros:
        probs: probabilidades a priori.
        matriz: matriz del canal.
    Devuelve:
        float (bits).
    """
    conjunta = probabilidades_simultaneas(probs, matriz)
    post = probabilidades_a_posteriori(probs, matriz)
    return sum(conjunta[i][j] * math.log2(1 / post[i][j])
               for i in range(len(probs)) for j in range(len(matriz[0]))
               if conjunta[i][j] > 0)


def perdida(probs, matriz):
    """
    Qué es:
        Pérdida del canal, calculada por definición:
        H(B/A) = sum_{a,b} P(a,b) * log2(1 / P(b/a)).

    Para qué se usa:
        Mide la incertidumbre sobre la salida que queda aun conociendo la
        entrada: cuánto "dispersa" el canal cada símbolo enviado.

    Cómo interpretar el resultado:
        - 0: canal determinante; cada entrada produce siempre la misma
          salida.
        - Igual a H(B): la salida no depende de la entrada.
        - Cuanto mayor, más aleatoria es la salida para una entrada dada.
        - Siempre 0 <= H(B/A) <= H(B).

    Parámetros:
        probs: probabilidades a priori.
        matriz: matriz del canal.
    Devuelve:
        float (bits).
    """
    conjunta = probabilidades_simultaneas(probs, matriz)
    return sum(conjunta[i][j] * math.log2(1 / matriz[i][j])
               for i in range(len(probs)) for j in range(len(matriz[0]))
               if conjunta[i][j] > 0)


def entropia_afin(probs, matriz):
    """
    Qué es:
        Entropía afín o conjunta, calculada por definición:
        H(A,B) = sum_{a,b} P(a,b) * log2(1 / P(a,b)).

    Para qué se usa:
        Mide la incertidumbre total del par (entrada, salida). Es la unión
        de H(A) y H(B) en el diagrama de Venn del canal.

    Cómo interpretar el resultado:
        - Cumple H(A,B) = H(A) + H(B) - I(A,B).
        - Igual a H(A) + H(B): entrada y salida independientes (I = 0).
        - Igual a H(A) (o a H(B)): uno de los dos determina completamente
          al otro.
        - Siempre max(H(A), H(B)) <= H(A,B) <= H(A) + H(B).

    Parámetros:
        probs: probabilidades a priori.
        matriz: matriz del canal.
    Devuelve:
        float (bits).
    """
    conjunta = probabilidades_simultaneas(probs, matriz)
    return CalcEntropia([p for fila in conjunta for p in fila])


def informacion_mutua(probs, matriz):
    """
    Qué es:
        Información mutua, calculada por definición:
        I(A,B) = sum_{a,b} P(a,b) * log2( P(a,b) / (P(a) * P(b)) ).

    Para qué se usa:
        Mide cuánta información sobre la entrada atraviesa el canal: la
        incertidumbre sobre A que se resuelve al observar B. Es la medida
        principal de qué tan bueno es un canal para una fuente dada.

    Cómo interpretar el resultado:
        - 0: entrada y salida independientes; el canal no transmite nada.
        - Igual a H(A): canal sin ruido, pasa toda la información de la
          entrada.
        - Igual a H(B): canal determinante.
        - Nunca es negativa y es recíproca: I(A,B) = I(B,A).
        - Depende de las probabilidades a priori; su máximo sobre todas las
          distribuciones posibles es la capacidad del canal.

    Parámetros:
        probs: probabilidades a priori.
        matriz: matriz del canal.
    Devuelve:
        float (bits).
    """
    conjunta = probabilidades_simultaneas(probs, matriz)
    salida = probabilidades_salida(probs, matriz)
    return sum(conjunta[i][j] * math.log2(conjunta[i][j] / (probs[i] * salida[j]))
               for i in range(len(probs)) for j in range(len(salida))
               if conjunta[i][j] > 0)


def analisis_canal(probs, matriz):
    """
    Qué es:
        Calcula todas las entropías de un canal y verifica las relaciones
        entre ellas.

    Para qué se usa:
        Para resolver de una vez los ejercicios 14, 16, 17, 19 y 21 y
        comprobar los resultados hechos a mano.

    Cómo interpretar el resultado (diccionario):
        'H(A)'    entropía a priori (de la entrada).
        'H(B)'    entropía de la salida.
        'H(A/B)'  equivocación o ruido.
        'H(B/A)'  pérdida.
        'H(A,B)'  entropía afín.
        'I(A,B)'  información mutua por definición.
        'I(B,A)'  H(B) - H(B/A); tiene que coincidir con I(A,B)
                  (reciprocidad).
        'verifica_relaciones'  True si se cumplen
                  I = H(A) - H(A/B) = H(B) - H(B/A) y
                  H(A,B) = H(A) + H(B) - I.
                  False indicaría un error en los datos.

    Parámetros:
        probs: probabilidades a priori.
        matriz: matriz del canal.
    Devuelve:
        dict.
    """
    h_a = CalcEntropia(probs)
    h_b = CalcEntropia(probabilidades_salida(probs, matriz))
    h_ab = equivocacion(probs, matriz)
    h_ba = perdida(probs, matriz)
    h_conj = entropia_afin(probs, matriz)
    i_ab = informacion_mutua(probs, matriz)
    i_ba = h_b - h_ba
    tol = 1e-6
    verifica = (abs(i_ab - (h_a - h_ab)) < tol and abs(i_ab - i_ba) < tol
                and abs(h_conj - (h_a + h_b - i_ab)) < tol)
    return {
        "H(A)": h_a, "H(B)": h_b, "H(A/B)": h_ab, "H(B/A)": h_ba,
        "H(A,B)": h_conj, "I(A,B)": i_ab, "I(B,A)": i_ba,
        "verifica_relaciones": verifica,
    }


# ---------------------------------------------------------------------------
# Ejercicio 18: canales sin ruido y determinantes
# ---------------------------------------------------------------------------
def es_sin_ruido(matriz):
    """
    Qué es:
        Verifica si el canal es sin ruido: cada COLUMNA de la matriz tiene
        un único elemento distinto de cero.

    Para qué se usa:
        Para clasificar canales (ejercicio 17) y para saber si se puede usar
        la fórmula directa de capacidad C = log2(cantidad de entradas).

    Cómo interpretar el resultado:
        - True: al ver cualquier salida se sabe con certeza qué entró. La
          equivocación H(A/B) es 0 y I(A,B) = H(A): pasa toda la
          información de la entrada.
        - False: alguna salida puede venir de más de una entrada, así que
          hay incertidumbre sobre lo enviado.
        - Un canal puede ser sin ruido y a la vez repartir una entrada en
          varias salidas (no es necesariamente determinante).

    Parámetros:
        matriz: matriz del canal.
    Devuelve:
        bool.
    """
    _validar_matriz(matriz)
    return all(sum(1 for p in _columna(matriz, j) if p > _TOL) == 1
               for j in range(len(matriz[0])))


def es_determinante(matriz):
    """
    Qué es:
        Verifica si el canal es determinante: cada FILA de la matriz tiene
        un único elemento distinto de cero (que entonces vale 1).

    Para qué se usa:
        Para clasificar canales (ejercicio 17), para las reducciones (el
        canal que combina columnas es determinante) y para la fórmula de
        capacidad C = log2(cantidad de salidas).

    Cómo interpretar el resultado:
        - True: cada entrada produce siempre la misma salida. La pérdida
          H(B/A) es 0 y I(A,B) = H(B).
        - False: alguna entrada puede producir salidas distintas.
        - Un canal determinante puede llevar varias entradas a la misma
          salida (no es necesariamente sin ruido).
        - Si es determinante y sin ruido a la vez, es una permutación: la
          salida es la entrada "renombrada" y I(A,B) = H(A) = H(B).

    Parámetros:
        matriz: matriz del canal.
    Devuelve:
        bool.
    """
    _validar_matriz(matriz)
    return all(sum(1 for p in fila if p > _TOL) == 1 for fila in matriz)


# ---------------------------------------------------------------------------
# Ejercicio 20: canales en serie
# ---------------------------------------------------------------------------
def canal_serie(matriz1, matriz2):
    """
    Qué es:
        Matriz del canal compuesto por dos canales en serie: la salida del
        primero es la entrada del segundo. Es el producto de matrices
        P(c/a) = sum_b P(b/a) * P(c/b).

    Para qué se usa:
        Para el ejercicio 19 y para las reducciones de canales (una
        reducción es poner en serie un canal determinante).

    Cómo interpretar el resultado:
        - Filas = entradas del primer canal; columnas = salidas del segundo.
        - La información mutua del canal compuesto nunca supera a la del
          primer canal: I(A,C) <= I(A,B). Los procesamientos en serie no
          agregan información, a lo sumo la conservan.
        - La cantidad de columnas del primer canal tiene que coincidir con
          la cantidad de filas del segundo.

    Parámetros:
        matriz1: matriz del primer canal (r x s).
        matriz2: matriz del segundo canal (s x t).
    Devuelve:
        lista de listas (r x t).
    """
    _validar_matriz(matriz1)
    _validar_matriz(matriz2)
    if len(matriz1[0]) != len(matriz2):
        raise ValueError("Las salidas del primer canal deben ser las entradas del segundo.")
    t = len(matriz2[0])
    return [[sum(fila[k] * matriz2[k][j] for k in range(len(fila))) for j in range(t)]
            for fila in matriz1]


# ---------------------------------------------------------------------------
# Ejercicios 22 y 23: reducciones suficientes
# ---------------------------------------------------------------------------
def es_reduccion_suficiente(matriz, j, k):
    """
    Qué es:
        Verifica si las columnas j y k del canal se pueden combinar en una
        reducción suficiente: tienen que ser proporcionales,
        P(b_j/a) = constante * P(b_k/a) para toda entrada a.

    Para qué se usa:
        Para simplificar un canal (menos salidas) sin perder información
        (ejercicios 21 y 22a).

    Cómo interpretar el resultado:
        - True: combinar esas dos salidas no cambia la información mutua,
          cualesquiera sean las probabilidades a priori. Las dos salidas
          dicen exactamente lo mismo sobre la entrada.
        - False: combinarlas igual se puede, pero se pierde información
          (I(A,C) < I(A,B)).

    Parámetros:
        matriz: matriz del canal.
        j, k: índices de las columnas (desde 0), distintos.
    Devuelve:
        bool.
    """
    _validar_matriz(matriz)
    s = len(matriz[0])
    if not (0 <= j < s and 0 <= k < s) or j == k:
        raise ValueError("Los índices deben ser dos columnas distintas de la matriz.")
    cj, ck = _columna(matriz, j), _columna(matriz, k)
    sj, sk = sum(cj), sum(ck)
    return all(abs(x * sk - y * sj) < 1e-9 for x, y in zip(cj, ck))


def matriz_determinante_reduccion(matriz, j, k):
    """
    Qué es:
        Matriz del canal determinante que, puesto en serie a continuación
        del canal, combina las columnas j y k en una sola salida.

    Para qué se usa:
        Para realizar la reducción (ejercicio 22b):
        canal_serie(matriz, matriz_determinante_reduccion(matriz, j, k)).

    Cómo interpretar el resultado:
        - Es una matriz de s filas (salidas originales) y s-1 columnas
          (salidas del canal reducido), con un único 1 por fila.
        - Las salidas j y k van a la misma columna, ubicada en la posición
          de la menor de las dos; el resto mantiene su orden.
        - No verifica si la reducción es suficiente; para eso está
          es_reduccion_suficiente.

    Parámetros:
        matriz: matriz del canal.
        j, k: índices de las columnas a combinar (desde 0), distintos.
    Devuelve:
        lista de listas (s x (s-1)).
    """
    _validar_matriz(matriz)
    s = len(matriz[0])
    if not (0 <= j < s and 0 <= k < s) or j == k:
        raise ValueError("Los índices deben ser dos columnas distintas de la matriz.")
    menor, mayor = min(j, k), max(j, k)
    determinante = []
    for b in range(s):
        destino = menor if b == mayor else (b if b < mayor else b - 1)
        determinante.append([1.0 if c == destino else 0.0 for c in range(s - 1)])
    return determinante


def reducir_canal(matriz, pasos=False):
    """
    Qué es:
        Aplica todas las reducciones suficientes posibles: mientras haya dos
        columnas proporcionales, las combina (con las funciones de los
        ejercicios 20 y 22). Siempre combina el primer par encontrado.

    Para qué se usa:
        Para obtener el canal más simple que transmite la misma información
        (ejercicios 21 y 23).

    Cómo interpretar el resultado:
        - Devuelve la matriz del canal reducido. Con pasos=True devuelve la
          lista de matrices de cada paso (la primera es la original).
        - La información mutua es la misma en todos los pasos (para
          cualquier distribución a priori): por eso son reducciones
          suficientes.
        - Si el canal reducido es determinante (es_determinante), la salida
          ya no tiene ruido "extra": toda su variación depende de la
          entrada.
        - Si la matriz no cambia, el canal no admite reducciones suficientes.

    Parámetros:
        matriz: matriz del canal.
        pasos: si es True devuelve todas las matrices intermedias.
    Devuelve:
        lista de listas, o lista de matrices si pasos es True.
    """
    _validar_matriz(matriz)
    actual = [list(fila) for fila in matriz]
    historial = [actual]
    hubo_cambio = True
    while hubo_cambio and len(actual[0]) > 1:
        hubo_cambio = False
        s = len(actual[0])
        for j in range(s):
            for k in range(j + 1, s):
                if es_reduccion_suficiente(actual, j, k):
                    actual = canal_serie(actual, matriz_determinante_reduccion(actual, j, k))
                    historial.append(actual)
                    hubo_cambio = True
                    break
            if hubo_cambio:
                break
    return historial if pasos else actual


# ---------------------------------------------------------------------------
# Ejercicios 25 y 26: capacidad
# ---------------------------------------------------------------------------
def _es_permutacion(a, b):
    return all(abs(x - y) < 1e-9 for x, y in zip(sorted(a), sorted(b)))


def es_uniforme(matriz):
    """
    Qué es:
        Verifica si el canal es uniforme: todas las filas tienen los mismos
        valores (en distinto orden) y todas las columnas también.

    Para qué se usa:
        Para saber si se puede calcular la capacidad con la fórmula directa
        C = log2(cantidad de salidas) - H(fila) (ejercicio 25). El canal
        binario simétrico (BSC) es el caso más conocido.

    Cómo interpretar el resultado:
        - True: el canal trata a todas las entradas "de la misma manera";
          la capacidad se alcanza con entradas equiprobables.
        - False: hay que buscar la capacidad de otra forma (por ejemplo,
          con capacidad_binaria si el canal tiene 2 entradas).
        - Se exige también que las columnas sean permutaciones entre sí:
          si solo las filas lo fueran, la fórmula daría un valor mayor que
          la capacidad real.

    Parámetros:
        matriz: matriz del canal.
    Devuelve:
        bool.
    """
    _validar_matriz(matriz)
    filas_ok = all(_es_permutacion(fila, matriz[0]) for fila in matriz)
    columnas = [_columna(matriz, j) for j in range(len(matriz[0]))]
    columnas_ok = all(len(c) == len(columnas[0]) and _es_permutacion(c, columnas[0]) for c in columnas)
    return filas_ok and columnas_ok


def capacidad_canal(matriz):
    """
    Qué es:
        Capacidad C del canal (máxima información mutua posible, en bits),
        para los casos con fórmula directa:
          - Canal determinante: C = log2(cantidad de salidas usadas).
          - Canal sin ruido:    C = log2(cantidad de entradas).
          - Canal uniforme:     C = log2(cantidad de salidas) - H(fila).

    Para qué se usa:
        Para los ejercicios 24 y 25b. Según el Segundo Teorema de Shannon,
        una fuente con entropía H <= C se puede transmitir por el canal con
        una probabilidad de error tan chica como se quiera.

    Cómo interpretar el resultado:
        - Devuelve (C, tipo), donde tipo dice qué fórmula se usó.
        - C = 0: el canal no transmite información.
        - C = log2(r) con r entradas: es el máximo posible; el canal no
          pierde nada.
        - Si el canal no es de ninguno de los tres tipos devuelve
          (None, 'sin fórmula directa'): para canales binarios usar
          capacidad_binaria.

    Parámetros:
        matriz: matriz del canal.
    Devuelve:
        tupla (float o None, str).
    """
    if es_determinante(matriz):
        usadas = sum(1 for j in range(len(matriz[0])) if any(p > _TOL for p in _columna(matriz, j)))
        return math.log2(usadas), "determinante"
    if es_sin_ruido(matriz):
        return math.log2(len(matriz)), "sin ruido"
    if es_uniforme(matriz):
        return math.log2(len(matriz[0])) - CalcEntropia(matriz[0]), "uniforme"
    return None, "sin fórmula directa"


def capacidad_binaria(matriz, paso):
    """
    Qué es:
        Estima la capacidad de un canal con 2 entradas calculando la
        información mutua para P(a1) = 0, paso, 2*paso, ..., 1 (con
        P(a2) = 1 - P(a1)) y quedándose con el máximo.

    Para qué se usa:
        Para los canales binarios que no tienen fórmula directa
        (ejercicios 26 y 27) y para el ejercicio 2 del parcial (se le pasa
        el canal reducido, que tiene la misma capacidad que el original).

    Cómo interpretar el resultado:
        - Devuelve (C, p): C es la capacidad estimada y p la probabilidad
          a priori P(a1) con la que se alcanza. La distribución óptima es
          {p, 1 - p}: P(0) = p y P(1) = 1 - p.
        - Cuanto más chico el paso, más precisa la estimación (con
          paso = 0.0001 se obtienen 4 decimales).
        - p cerca de 0.5: al canal le convienen entradas casi equiprobables
          (pasa en canales casi simétricos).
        - C cerca de 0: el canal es muy ruidoso; ninguna distribución de
          entrada logra pasar mucha información.

    Parámetros:
        matriz: matriz del canal (2 filas).
        paso: incremento de P(a1), entre 0 y 1.
    Devuelve:
        tupla (capacidad, probabilidad).
    """
    _validar_matriz(matriz)
    if len(matriz) != 2:
        raise ValueError("El canal debe tener exactamente 2 entradas.")
    if not 0 < paso <= 1:
        raise ValueError("El paso debe estar entre 0 y 1.")
    cantidad = int(1 / paso + 1e-9)
    mejor_c, mejor_p = -1.0, 0.0
    for i in range(cantidad + 1):
        p = min(i * paso, 1.0)
        c = informacion_mutua([p, 1 - p], matriz)
        if c > mejor_c + 1e-12:
            mejor_c, mejor_p = c, p
    return mejor_c, mejor_p


# ---------------------------------------------------------------------------
# Ejercicio 30: probabilidad de error
# ---------------------------------------------------------------------------
def probabilidad_error(probs, matriz, a_posteriori=False):
    """
    Qué es:
        Probabilidad de error del canal con una regla de decisión: para cada
        salida b_j el receptor decide qué entrada a* se envió, y
        P_E = 1 - sum_j P(a*, b_j).

        Hay dos reglas posibles:
          - Máxima posibilidad (por defecto, es la que usan los resultados
            de la guía): a* es la entrada con mayor P(b_j / a*), la mayor
            probabilidad de la columna j de la matriz. No tiene en cuenta
            las probabilidades a priori al decidir.
          - Máxima probabilidad a posteriori (a_posteriori=True, es la que
            describe la diapositiva de la teoría): a* es la entrada con
            mayor P(a* / b_j), es decir, mayor P(a*) * P(b_j / a*).

    Para qué se usa:
        Para medir qué tan seguido se equivoca el receptor al adivinar la
        entrada a partir de la salida (ejercicios 28 a 30).

    Cómo interpretar el resultado:
        - 0: el receptor nunca se equivoca (canal sin ruido).
        - Cuanto más grande, peor.
        - Depende de las probabilidades a priori: el mismo canal puede
          tener distinta P_E según qué tan probable sea cada entrada.
        - Con entradas equiprobables las dos reglas dan lo mismo.
        - Con entradas no equiprobables la regla a posteriori da una P_E
          menor o igual: es la mínima posible decidiendo símbolo a símbolo.
          Ejemplo, ejercicio 29b: 0.425 con máxima posibilidad y 0.35 con
          la regla a posteriori.
        - Si hay empate en el máximo de una columna, se elige la primera
          entrada.

    Parámetros:
        probs: probabilidades a priori.
        matriz: matriz del canal.
        a_posteriori: False = máxima posibilidad; True = máxima
                      probabilidad a posteriori.
    Devuelve:
        float.
    """
    conjunta = probabilidades_simultaneas(probs, matriz)
    aciertos = 0.0
    for j in range(len(matriz[0])):
        criterio = _columna(conjunta, j) if a_posteriori else _columna(matriz, j)
        elegida = criterio.index(max(criterio))
        aciertos += conjunta[elegida][j]
    return 1 - aciertos
