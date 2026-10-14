# Explicaciones de las funciones para el examen

Esta guía contiene textos breves que se pueden adaptar a la entrada y al
resultado de cada ejercicio. Conviene copiar solamente la explicación de las
funciones que realmente se utilizaron y agregar al final el resultado numérico
obtenido.

## Decisiones rápidas

- Para una fuente de memoria nula, la entropía en bits se calcula con
  `CalcEntropia`.
- Para una fuente de Markov de orden 1, se utiliza
  `calculaEntropiaMarkovOrden1`.
- Para una fuente de Markov de orden m, se utiliza
  `calculaEntropiaMarkovOrdenM`.
- `entropia_fuente` se usa en problemas de codificación: expresa la entropía
  en base r, donde r es la cantidad de símbolos del alfabeto código.
- Las matrices de transición de `Formulas.py` usan la convención
  `matriz[destino][origen]`; por eso cada columna debe sumar 1.
- En una extensión de una fuente de memoria nula se multiplican las
  probabilidades de sus símbolos. La entropía de la extensión se debe calcular
  a partir de la lista resultante; después puede verificarse el teorema
  `H(S^n) = n H(S)`.

---

# Funciones de `Formulas.py`

## `CalcInfo(fdp)`

### Explicación para el examen

Para obtener la información propia de cada símbolo recorrí su distribución de
probabilidades y apliqué la definición

\[
I(s_i)=\log_2\left(\frac{1}{P(s_i)}\right).
\]

La función devuelve una lista paralela con la información de cada símbolo en
bits. Un valor mayor significa que el símbolo es menos probable y, por lo
tanto, más sorpresivo. Las probabilidades nulas no se incluyen porque el
logaritmo de su inversa no está definido.

## `CalcEntropia(fdp)`

### Explicación para el examen

Para calcular la entropía obtuve primero la información propia de cada símbolo
y luego calculé su promedio ponderado mediante

\[
H(S)=\sum_i P(s_i)I(s_i)
=-\sum_iP(s_i)\log_2P(s_i).
\]

El resultado se expresa en bits por símbolo y representa la incertidumbre
promedio de la fuente. Se utiliza directamente cuando la fuente es de memoria
nula. Cuanto mayor es la entropía, menos predecible es el símbolo emitido.

## `GeneraAlfabetoYProb(cadena)`

### Explicación para el examen

Para obtener el alfabeto recorrí el mensaje e identifiqué sus caracteres
distintos, sin considerar los espacios. Para cada símbolo conté su cantidad de
apariciones y la dividí por la longitud total del mensaje:

\[
P(s_i)=\frac{N(s_i)}{N}.
\]

Finalmente ordené conjuntamente los símbolos y sus probabilidades para no
perder la correspondencia entre ambas listas. La función devuelve el alfabeto
ordenado y una lista paralela con las probabilidades estimadas.

### Precaución

La implementación excluye el espacio del alfabeto, pero lo cuenta dentro de la
longitud total. En los mensajes del parcial que no contienen espacios esto no
produce ningún inconveniente.

## `GeneraPalabra(N, alfabeto, probabilidades)`

### Explicación para el examen

Para generar una palabra aleatoria construí primero la distribución acumulada
de probabilidades. Para cada una de las N posiciones generé un número aleatorio
uniforme entre 0 y 1 y seleccioné el símbolo cuyo intervalo acumulado contenía
ese número. De esta forma, al repetir el procedimiento muchas veces, las
frecuencias de los símbolos tienden a aproximarse a las probabilidades dadas.
La función devuelve los N símbolos seleccionados concatenados en una cadena.

## `Equiprobables(cant)`

### Explicación para el examen

Cuando todos los sucesos son equiprobables, cada uno tiene probabilidad
`1/cant`. Al reemplazar esa distribución en la definición de entropía se
obtiene

\[
H(S)=\log_2(cant).
\]

La función devuelve esa entropía máxima en bits por símbolo. Una mayor cantidad
de alternativas equiprobables produce una mayor incertidumbre.

## `DevuelveExtyFdp(alfabeto, fdp, N)`

### Explicación para el examen

Para construir la extensión de orden N utilicé recursividad. El caso base de
orden 1 es el alfabeto original. Para cada orden posterior combiné cada palabra
de la extensión anterior con cada símbolo del alfabeto. Como la función se usa
para una fuente de memoria nula, la probabilidad de cada secuencia se obtiene
multiplicando las probabilidades de sus componentes:

\[
P(s_{i_1}\ldots s_{i_N})=
P(s_{i_1})\cdots P(s_{i_N}).
\]

La función devuelve el alfabeto extendido y su lista paralela de
probabilidades. Para calcular la entropía pedida a partir de esas probabilidades
se aplica `CalcEntropia` a la nueva lista. Después se puede verificar que

\[
H(S^N)=N H(S).
\]

No debe utilizarse esta multiplicación para una fuente con memoria, porque en
ese caso los símbolos no son independientes.

## `CalculaEntropiaMemoriaBinaria(w)`

### Explicación para el examen

La función representa una fuente binaria cuyas probabilidades son `w` y
`1-w`. Luego aplica la definición de entropía:

\[
H_b(w)=-w\log_2w-(1-w)\log_2(1-w).
\]

El resultado se expresa en bits por símbolo. La entropía es máxima e igual a 1
cuando ambas alternativas son equiprobables y disminuye cuando una de ellas se
vuelve más probable que la otra.

## `generaalfabetoyTransicion(cadena)`

### Explicación para el examen

Primero obtuve y ordené el alfabeto del mensaje. Luego construí una matriz
cuadrada de ceros y recorrí todos los pares consecutivos. Para cada par
incrementé la celda

`matriz[símbolo siguiente][símbolo actual]`.

Finalmente normalicé cada columna dividiendo sus conteos por la cantidad total
de transiciones desde ese estado. De esta forma,

\[
M_{ij}=P(X_{n+1}=i\mid X_n=j),
\]

donde la fila representa el destino y la columna el origen. Por ese motivo
cada columna de la matriz resultante suma 1.

## `transponer(matriz)`

### Explicación para el examen

Para transponer la matriz agrupé los elementos que ocupaban la misma posición
en cada fila y los convertí en nuevas filas. Así intercambié filas por columnas:

\[
(M^T)_{ij}=M_{ji}.
\]

Esta función se utiliza cuando una matriz fue escrita con la convención
`matriz[origen][destino]` y debe convertirse a la convención del proyecto,
`matriz[destino][origen]`.

## `generaVectorEstacionario(matriz, n)`

### Explicación para el examen

Para aproximar el vector estacionario comencé con una distribución uniforme,
es decir, con probabilidad `1/n` en cada estado. Luego apliqué repetidamente la
matriz de transición:

\[
\boldsymbol{\pi}_{k+1}=M\boldsymbol{\pi}_k.
\]

La implementación realiza 30 iteraciones. Si la cadena converge, el resultado
se aproxima a un vector que cumple

\[
M\boldsymbol{\pi}=\boldsymbol{\pi},
\qquad
\sum_i\pi_i=1.
\]

Cada componente representa la probabilidad de encontrar la fuente en ese
estado a largo plazo. Las pequeñas diferencias decimales respecto del valor
exacto se deben al método iterativo y al punto flotante.

## `calculaInfoCondicional(probabilidad)`

### Explicación para el examen

Para calcular la información de un símbolo cuando se conoce el estado anterior
apliqué

\[
I(s_i\mid e_j)=
\log_2\left(\frac{1}{P(s_i\mid e_j)}\right).
\]

La función recibe una probabilidad condicional mayor que cero y devuelve el
resultado en bits. Una transición menos probable aporta más información que
una transición frecuente.

## `calculaEntropiaMarkovOrden1(matriz, vector_estacionario=None)`

### Explicación para el examen

Para una fuente de Markov de orden 1 calculé primero la entropía de las
transiciones que salen de cada estado y luego ponderé cada una por la
probabilidad estacionaria de ese estado:

\[
H(S)=\sum_j\pi_j
\left[-\sum_iP(i\mid j)\log_2P(i\mid j)\right].
\]

La matriz utiliza filas como destinos y columnas como orígenes. Las
transiciones de probabilidad cero no aportan a la sumatoria. Si no se pasa un
vector estacionario, la función lo aproxima con `generaVectorEstacionario`.
El resultado se expresa en bits por símbolo y mide la incertidumbre restante
cuando se conoce el símbolo anterior.

Esta función, y no la entropía marginal calculada solamente con las frecuencias
de los símbolos, es la que corresponde cuando la fuente tiene memoria de orden
1.

## `calculaEntropiaMarkovOrdenM(probabilidades_estados, probabilidades_condicionales)`

### Explicación para el examen

Para una fuente de Markov de orden m consideré como estado de memoria cada
secuencia formada por los últimos m símbolos. Para cada estado calculé la
entropía de la distribución del próximo símbolo y la ponderé por la
probabilidad de encontrarse en ese estado:

\[
H(S)=\sum_eP(e)
\left[-\sum_iP(s_i\mid e)\log_2P(s_i\mid e)\right].
\]

La primera lista contiene las probabilidades de los estados de memoria y la
segunda contiene una distribución condicional por cada estado. El resultado se
expresa en bits por símbolo.

## `tieneMemoriaNoNula(matriz, tolerancia)`

### Explicación para el examen

Una fuente es de memoria nula cuando la distribución del próximo símbolo no
depende del símbolo actual. Con la convención utilizada, eso significa que las
columnas de la matriz son iguales o aproximadamente iguales. Para estimarlo,
la función recorre cada fila y compara sus probabilidades entre columnas,
tomando el elemento diagonal de la fila como referencia. Si alguna diferencia
absoluta supera la tolerancia, devuelve `True`, indicando que existe evidencia
de memoria. Si ninguna la supera, devuelve `False` y la fuente puede
considerarse de memoria nula.

Una tolerancia demasiado grande puede ocultar memoria real y una demasiado
pequeña puede interpretar como memoria las variaciones producidas por una
muestra finita. Si el enunciado no fija un valor, debe indicarse y justificarse
el utilizado; para los mensajes trabajados se puede utilizar `0.01`.

### Interpretación rápida

- `True`: fuente con memoria según la tolerancia elegida.
- `False`: fuente compatible con memoria nula según esa tolerancia.

## `esFuenteErgodica(matriz)`

### Explicación para el examen

Para determinar si una fuente finita es ergódica verifiqué que fuera
irreducible y aperiódica. Primero interpreté cada probabilidad positiva como
una arista del grafo. Recorrí el grafo desde un estado tanto en el sentido
normal como con las aristas invertidas. Si no se alcanzan todos los estados en
ambos recorridos, no todos se comunican y la cadena no es irreducible.

Si es irreducible, calculé distancias desde un estado y obtuve el máximo común
divisor de las diferencias asociadas a todas las aristas. Ese valor representa
el período de la cadena. Si el período es 1, la cadena es aperiódica. La función
devuelve `True` solamente cuando se cumplen ambas condiciones.

Un resultado `True` significa que existe un único vector estacionario y que la
distribución converge hacia él desde cualquier estado inicial. Un resultado
`False` indica que la cadena no es irreducible o no es aperiódica.

## `obtenerDatosSimbolo(alfabeto, probabilidades, simbolo, *listas_paralelas)`

### Explicación para el examen

Para consultar los datos de uno o varios símbolos busqué su posición dentro
del alfabeto y utilicé ese mismo índice en todas las listas paralelas. Antes de
hacer la búsqueda verifiqué que todas las listas tuvieran la misma longitud que
el alfabeto, evitando asociar datos incorrectos.

Si se consulta un solo símbolo, la función devuelve su probabilidad o una
tupla con todos sus datos. Si se consulta una lista de símbolos, devuelve una
lista de resultados en el mismo orden. Las listas adicionales permiten
recuperar, por ejemplo, información propia, longitudes u otros valores
asociados sin buscar manualmente sus posiciones.

---

# Funciones de `FormulasCodificacion.py`

## `es_noSingular(codigo)`

### Explicación para el examen

Para determinar si el código es no singular comparé la cantidad total de
palabras con la cantidad de palabras diferentes. Si ambas cantidades son
iguales, cada símbolo fuente tiene una palabra código distinta y la función
devuelve `True`. Si hay alguna palabra repetida, devuelve `False` y el código
es singular.

Ser no singular solamente garantiza que los símbolos individuales tienen
representaciones diferentes; no garantiza que las concatenaciones puedan
decodificarse de manera única.

## `es_instantaneo(palabras)`

### Explicación para el examen

Para verificar si el código es instantáneo comparé todas las palabras entre sí
y comprobé que ninguna fuera prefijo de otra palabra distinta. Si una palabra
es prefijo de otra, el receptor necesita leer más símbolos para decidir si la
palabra ya terminó y la función devuelve `False`. Si no existe ninguna relación
de prefijo, devuelve `True` y cada palabra puede reconocerse apenas finaliza.

Todo código instantáneo es unívocamente decodificable y no singular.

## `calcular_restos(conjunto_a, conjunto_b)`

### Explicación para el examen

Esta función auxiliar compara las palabras de dos conjuntos. Cuando una
palabra del primer conjunto es prefijo de una palabra del segundo, elimina ese
prefijo y guarda el sufijo no vacío que queda. Esos sufijos representan partes
pendientes que podrían producir dos descomposiciones diferentes de una misma
cadena y se utilizan en el algoritmo de Sardinas-Patterson.

Un conjunto vacío significa que esa comparación no generó nuevos restos
pendientes.

## `es_univocamente_decodificable(palabras)`

### Explicación para el examen

Para decidir si el código es unívocamente decodificable apliqué el algoritmo de
Sardinas-Patterson. Primero obtuve los restos producidos cuando una palabra es
prefijo de otra. Luego combiné sucesivamente esos restos con las palabras
originales en ambos sentidos.

Si un resto coincide con una palabra código, existe una cadena que admite dos
decodificaciones y la función devuelve `False`. Si el conjunto de restos queda
vacío o se repite un conjunto anterior sin producir una colisión, el proceso no
puede generar una ambigüedad y devuelve `True`.

Un resultado `True` garantiza que cualquier concatenación de palabras código
puede separarse de una única manera, aunque el código no sea necesariamente
instantáneo.

## `get_alfabetoCodigo(palabras)`

### Explicación para el examen

Para obtener el alfabeto código recorrí todos los caracteres utilizados en las
palabras, los agregué a un conjunto para eliminar repeticiones y finalmente los
ordené. La cantidad de caracteres obtenidos es la base r del código. Por
ejemplo, los símbolos `0` y `1` forman un alfabeto binario de base 2.

## `get_longitudes(palabras)`

### Explicación para el examen

Para obtener las longitudes recorrí la lista de palabras código y conté la
cantidad de caracteres de cada una. La función devuelve una lista paralela en
la que cada elemento es la longitud de la palabra ubicada en la misma posición.

## `calcular_kraft(palabras)`

### Explicación para el examen

Primero obtuve la base r contando los símbolos diferentes del alfabeto código y
calculé la longitud de cada palabra. Luego evalué la sumatoria de Kraft:

\[
K=\sum_i r^{-l_i}.
\]

Si `K > 1`, no puede existir un código unívocamente decodificable ni
instantáneo con esas longitudes. Si `K <= 1`, las longitudes permiten construir
algún código instantáneo, pero esto por sí solo no demuestra que las palabras
concretas recibidas formen un código unívoco. Si un código instantáneo tiene
`K = 1`, su árbol está completo; si tiene `K < 1`, queda capacidad disponible.

## `entropia_fuente(palabras, probabilidades)`

### Explicación para el examen

Para calcular la entropía en unidades del alfabeto código obtuve primero su base
r a partir de los caracteres diferentes utilizados en las palabras. Después
apliqué

\[
H_r(S)=\sum_iP(s_i)
\log_r\left(\frac{1}{P(s_i)}\right).
\]

El resultado representa la información promedio por símbolo fuente medida en
símbolos del alfabeto código. Para un código binario se expresa en bits; para
uno ternario se expresa en trits. Las palabras se utilizan únicamente para
determinar la base: la entropía depende de las probabilidades de la fuente.

Esta función corresponde a problemas de codificación de fuentes de memoria
nula. Si el ejercicio solamente presenta un mensaje sin palabras código, se
utiliza `CalcEntropia` para obtener bits.

## `get_longitudMedia(palabras, probabilidades)`

### Explicación para el examen

Para calcular la longitud media ponderé la longitud de cada palabra por la
probabilidad del símbolo fuente que representa:

\[
\overline{L}=\sum_iP(s_i)l_i.
\]

El resultado indica cuántos símbolos del alfabeto código se emiten, en
promedio, por cada símbolo fuente. No se utiliza un promedio simple porque los
símbolos fuente pueden tener probabilidades diferentes.

## `es_compacto(palabras, probabilidades)`

### Explicación para el examen

Primero verifiqué que el código fuera unívocamente decodificable. Si no lo es,
la función devuelve `False` directamente. Si es unívoco, obtuve la base r del
alfabeto código y comprobé para cada símbolo que su longitud cumpliera

\[
l_i\leq
\left\lceil\log_r\left(\frac{1}{P(s_i)}\right)\right\rceil.
\]

La función devuelve `True` únicamente si se cumple la decodificación única y
todas las palabras respetan su cota. Un resultado `False` puede deberse a una
ambigüedad de decodificación o a que alguna palabra sea más larga que lo
permitido por este criterio.

## `generar_mensaje(N, palabras, probabilidades)`

### Explicación para el examen

Para generar un mensaje codificado seleccioné N palabras de manera aleatoria e
independiente utilizando las probabilidades de la fuente como pesos. Luego
concatené las palabras elegidas. El resultado contiene N símbolos fuente
codificados, aunque su cantidad total de caracteres puede variar cuando las
palabras tienen longitudes diferentes.

Al realizar muchas generaciones, la frecuencia con la que se selecciona cada
palabra tiende a aproximarse a su probabilidad.

## `clasifica(codigo)`

### Explicación para el examen

La clasificación se realiza de manera jerárquica. Primero se comprueba si todas
las palabras son diferentes. Si además ninguna palabra es prefijo de otra, el
código se clasifica como instantáneo. Si existen prefijos, se aplica
Sardinas-Patterson: si las concatenaciones se decodifican de manera única se
clasifica como unívoco y, en caso contrario, solamente como no singular. Si hay
palabras repetidas, el código es singular.

La jerarquía utilizada es

\[
\text{instantáneo}
\Rightarrow
\text{unívocamente decodificable}
\Rightarrow
\text{no singular}.
\]

### Advertencia sobre la implementación actual

Cuando encuentra palabras repetidas, la función devuelve el texto `"bloque"`.
La propiedad matemática detectada en ese caso es `"singular"`. Un código de
bloque es otra cosa: es un código cuyas palabras tienen todas la misma
longitud. Por lo tanto, si aparece ese resultado, en la explicación teórica se
debe indicar que el código es singular, salvo que además se haya verificado por
separado que todas sus palabras tienen igual longitud.

---

# Modelos breves de conclusión

## Fuente de memoria nula

Las columnas de la matriz de transición resultaron iguales o sus diferencias
no superaron la tolerancia elegida. Por lo tanto, la distribución del siguiente
símbolo no depende del anterior y la fuente se estimó como de memoria nula. Su
entropía se calculó directamente a partir de las probabilidades marginales con
`CalcEntropia`.

## Fuente con memoria

Las columnas de la matriz presentaron diferencias superiores a la tolerancia,
por lo que la distribución del siguiente símbolo depende del estado actual. La
fuente se estimó como una fuente con memoria de orden 1. Se obtuvo su vector
estacionario y se calculó la entropía condicional promedio con
`calculaEntropiaMarkovOrden1`.

## Código instantáneo

Ninguna palabra resultó prefijo de otra, por lo que cada palabra puede
reconocerse apenas termina. En consecuencia, el código es instantáneo y también
es unívocamente decodificable y no singular.

## Código unívoco pero no instantáneo

Se encontraron relaciones de prefijo, por lo que el código no es instantáneo.
Sin embargo, el algoritmo de Sardinas-Patterson no encontró ambigüedades y por
eso el código es unívocamente decodificable.

## Código no singular pero no unívoco

Todas las palabras código son diferentes, por lo que el código es no singular.
Sin embargo, Sardinas-Patterson detectó que alguna concatenación admite dos
decodificaciones distintas; por eso no es unívocamente decodificable ni
instantáneo.

## Código singular

Al menos dos símbolos fuente tienen asignada la misma palabra código. Por lo
tanto, no es posible distinguirlos ni siquiera al codificar un solo símbolo y
el código es singular. En consecuencia, tampoco es unívocamente decodificable
ni instantáneo.

