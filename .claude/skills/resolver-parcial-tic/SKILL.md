---
name: resolver-parcial-tic
description: Resuelve un ejercicio del parcial de Teoría de la Información (U4-U6) con las funciones de Lucas en SegundoParcial/: resultados, cómo se obtuvieron y conclusiones.
---

# Resolver el parcial de Teoría de la Información (unidades 4, 5 y 6)

Lucas te pasa el enunciado (texto o captura) con los datos (mensaje, entrada/salida de un canal, probabilidades, códigos, matrices...) y lo que piden. Tu trabajo: resolverlo **usando solo sus funciones** y devolverle, por cada ejercicio, los resultados, la explicación de cómo se obtuvieron y el análisis con conclusiones. Respondé en español rioplatense, corto, claro y conciso.

## Archivos (carpeta `SegundoParcial/` de este repo)

- `FuncionesParcial2.py`: TODAS las funciones (Formulas, FormulasCodificacion, Func_clase4/5/6).
- `Explicaciones.py`: `explicar(funcion, args...)` corre la función e imprime RESULTADO, QUÉ SIGNIFICA, CÓMO SE OBTUVO, CÓMO LEERLO (caso marcado con `>>`) y FRASE. También `explicar_extension(probs, n)`, `explicacion_ej1/2(...)`, `conclusiones_ej1/2(...)`.
- `ResolverParcial.py`: bloque `DATOS DEL PARCIAL` arriba (MENSAJE, N, ENTRADA, SALIDA y opcionales PROBS, N_PROBS, CODIGO, CADENA_A_DECODIFICAR, MATRIZ, PRIORI, MATRIZ2, CODIGO_HAMMING, LEVENSHTEIN, TEXTO_PARIDAD, BITS_PARIDAD, RLC). Al correrlo imprime todo y lo guarda en `resultado_parcial.txt`.
- `Parcial_Ej1.py` / `Parcial_Ej2.py`: plantillas autocontenidas del formato del parcial 2025.
- `Guia_Interpretacion_Parcial2.pdf`: respuestas modelo y chequeos.

Si no encontrás la carpeta, preguntale a Lucas dónde está antes de seguir.

## Reglas que no se rompen

1. **Solo sus funciones.** Todo número sale de una función de `FuncionesParcial2.py`. No escribas algoritmos nuevos ni calcules a mano. Si algo pedido no tiene función, decilo y proponé qué faltaría.
2. **Solo `math` y `random`.** Cualquier `.py` que generes importa únicamente `math`, `random` y sus propios módulos. Nada de `sys`, `os`, `itertools`, `fractions`, etc.
3. **Nada inventado.** Los números y las frases salen de la salida real de los programas, con 4 decimales.
4. **No modifiques** `FuncionesParcial2.py` ni `Explicaciones.py`.

## Pasos

1. **Leer el enunciado.** Listá cada ejercicio con sus incisos (a, b, c...) y los datos exactos. Copiá los datos carácter por carácter; si una captura no se lee bien, preguntá.
2. **Mapear cada inciso a una función** (tabla de abajo).
3. **Correr.** Completá el bloque `DATOS DEL PARCIAL` de `ResolverParcial.py` (los datos que no aplican van vacíos), corré `python ResolverParcial.py` desde `SegundoParcial/` y leé `resultado_parcial.txt`. Para lo que no cubra, escribí `extra_parcial.py` con `from Explicaciones import *` y las llamadas `explicar(...)` necesarias, y corrélo.
4. **Armar el archivo de entrega** `Entrega_EjN.py` por ejercicio: un único archivo que corra solo. Copiá textualmente (leyendo `FuncionesParcial2.py`) cada función usada y las auxiliares que llama (`_validar_probs`, `_TOL`, `CalcEntropia`, etc.), y abajo las invocaciones imprimiendo cada resultado con su inciso. Verificá: copialo solo a una carpeta temporal vacía, corrélo y comprobá que da lo mismo que el paso 3; revisá que no importe nada más que `math` y `random`. Si el ejercicio tiene el formato del parcial 2025, alcanza con `Parcial_Ej1.py` / `Parcial_Ej2.py` cambiando los datos.
5. **Chequear coherencia** (abajo) antes de responder.
6. **Responder** con el formato de abajo.

## Qué función usar

| Piden | Función (en `FuncionesParcial2.py`) |
|---|---|
| probabilidades de un mensaje | `alfabeto_y_probabilidades(mensaje)` |
| entropía | `CalcEntropia(probs)` |
| código óptimo | `huffman(probs)` |
| Shannon-Fano | `shannon_fano(probs)` |
| L, η, R | `resumen_codigo(probs, codigos)` / `rendimiento_redundancia` |
| extensión de orden n | `extension_fuente(probs, n)` + `huffman`; explicar con `explicar_extension(probs, n)` |
| Primer Teorema | `detalle_primer_teorema(probs, codigos, n)` |
| clasificar código / Kraft | `clasifica(codigo)`, `calcular_kraft(codigo)` |
| tasa de compresión | `tasa_compresion_codigo(mensaje, alfabeto, codigos)` (sin bytes extra) |
| decodificar | `decodificar_cadena(cadena, simbolos, codigos)` |
| RLC | `rlc_texto`, `rlc_comprimir` |
| distancia de Hamming de un código | `analizar_codigo_hamming(codigos)` |
| Levenshtein | `distancia_levenshtein(a, b)` |
| paridad VRC/LRC/cruzada | `generar_mensaje_con_paridad(texto)`; corregir: `analizar_matriz_paridad(filas_de_bits(bits))` (fila 1 = LRC) |
| a priori y matriz desde secuencias | `canal_desde_secuencias(entrada, salida)` |
| sin ruido / determinante | `es_sin_ruido(m)`, `es_determinante(m)` |
| P(b), P(a,b), P(a/b), H(A/bj) | `probabilidades_salida`, `probabilidades_simultaneas`, `probabilidades_a_posteriori`, `entropias_a_posteriori` |
| H(A/B), H(B/A), H(A,B), I | `equivocacion`, `perdida`, `entropia_afin`, `informacion_mutua`, `analisis_canal` |
| reducciones suficientes | `reducir_canal(m)` |
| canales en serie | `canal_serie(m1, m2)` |
| capacidad | 2 entradas: `capacidad_binaria(reducido, 0.0001)` (P(a1) que maximiza); con fórmula: `capacidad_canal(m)` |
| probabilidad de error | `probabilidad_error(probs, m)` (máxima posibilidad); `a_posteriori=True` la otra regla |

## Chequeos antes de responder

- Probabilidades y cada fila de la matriz suman 1.
- H <= L; 0 < η <= 1; R = 1 - η. En la extensión, η = n·H/L_n (L_n es por bloque).
- Huffman siempre cumple el Primer Teorema.
- 0 <= H(A/B) <= H(A); I = H(A) - H(A/B) = H(B) - H(B/A); I del canal reducido = I del original; I <= C.
- Las P de la capacidad son las que maximizan I, no las a priori ni 0,5/0,5.
- P_E <= 1 - max P(a) con la regla a posteriori.
- El mensaje corregido se escribe como texto (ej. SOL), no como bits.

## Formato de la respuesta (por ejercicio)

**Resultados**: inciso por inciso, el número con 4 decimales (y la matriz/código si corresponde).

**Explicación de cómo se obtuvieron**: una o dos líneas por inciso, sacadas de "CÓMO SE OBTUVO" o de `explicacion_ejN`: método y fórmula, no el código.

**Análisis y conclusiones**: viñetas cortas que interpreten los valores (comparando cada uno con su mínimo/máximo) y relacionen los conceptos. Basate en las FRASES y en `conclusiones_ejN`, adaptadas a lo que se pidió. En fuentes/códigos tocá siempre: Shannon y la longitud media, códigos compactos y extensiones. En canales: cuánto de H(A) atraviesa (I), qué salidas identifican la entrada, reducción, capacidad vs. H(A) (Segundo Teorema), P_E y la corrección de paridad.

Al final, nombrá el archivo de entrega generado y confirmá que corre solo y que solo importa `math` y `random`.

## Lo que se marcó mal en el parcial 2025 (no repetir)

No explicar cómo se obtuvo el código; L de la extensión contradictoria con η y R; conclusión mínima (faltó Shannon-L-compactos-extensiones); "no explica" en el ejercicio de canales; fila de la matriz que no sumaba 1; P de la capacidad 0,5/0,5; P_E demasiado alta; mensaje corregido sin decodificar; un .py que importaba un módulo propio no entregado.
