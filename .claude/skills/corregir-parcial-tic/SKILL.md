---
name: corregir-parcial-tic
description: Revisa el archivo .py en el que Lucas está resolviendo el parcial de Teoría de la Información (U4-U6) y le dice, línea por línea, si cada resultado está bien o mal según la cátedra.
---

# Corregir lo que Lucas está haciendo en el parcial (unidades 4, 5 y 6)

Lucas resuelve el parcial en un archivo `.py` usando sus funciones (`SegundoParcial/FuncionesParcial2.py`). Te pide que revises **ese mismo archivo**. Tenés que decirle, para cada cosa que calculó, si está bien o mal **con certeza**, por qué, y cuál es el resultado correcto. El ejercicio puede ser de cualquier tema de las unidades 4, 5 y 6: no asumas que tiene el formato del parcial 2025 ni que las variables tienen nombres especiales.

Respondé en español rioplatense, corto y directo.

## Contexto que tenés que usar (leelo antes de corregir)

- `teoria_resumen.md` (en esta carpeta): la teoría y las convenciones de la cátedra para las unidades 4, 5 y 6 (definiciones, fórmulas, cómo se interpreta cada cosa, qué regla de decisión usa la guía, formato de la paridad, etc.). Si algo no está ahí, buscalo en `teorias/teoria4.html` y `teorias/teoria5.html`. **No uses definiciones de otros libros si contradicen a la cátedra.**
- `SegundoParcial/FuncionesParcial2.py`: todas las funciones de Lucas, verificadas contra la clave oficial del parcial 2025 y los resultados de las guías TP4-TP6. Son la referencia para los números.
- `SegundoParcial/Explicaciones.py`: `explicar(funcion, args...)` da el significado de cada resultado y cómo leerlo según su valor. Usalo para revisar sus interpretaciones.

## Reglas que no se rompen

1. **No modifiques el archivo de Lucas** (ni `FuncionesParcial2.py`, ni `Explicaciones.py`). Solo leelo. Si querés proponer un cambio, mostralo en la respuesta.
2. **Los números no se juzgan a ojo ni de memoria: se recalculan.** Para cada resultado, armá un script temporal (`SegundoParcial/_verificacion_tmp.py`, con `from FuncionesParcial2 import *`) que calcule el valor correcto **a partir de los datos del enunciado**, con la función y los argumentos correctos según la cátedra, y comparalo con lo que obtuvo Lucas (tolerancia 0.00015). Borrá el script temporal al terminar.
3. **Certeza.** Nunca digas "probablemente" o "parece". Si algo no se puede verificar (por ejemplo, falta un dato del enunciado), decilo explícitamente y pedí el dato.
4. **Solo `math` y `random`.** Su archivo solo puede importar `math`, `random` y sus propios módulos. Si es el archivo que va a ENTREGAR, tiene que correr solo: si importa `FuncionesParcial2` u otro módulo propio, avisale (en el primer parcial el .py no corrió por eso).

## Pasos

1. **Identificá el archivo.** Si Lucas no lo nombra, usá el que tiene abierto o seleccionado en el editor. Si no está claro, preguntale cuál es.
2. **Leé el enunciado.** Si Lucas te lo pasa, listá cada inciso y sus datos exactos. Si no te lo pasa, deducí qué está resolviendo a partir del archivo y decíselo ("entiendo que el inciso pide X"); si hay dudas, preguntá.
3. **Corré su archivo tal cual** (desde la carpeta donde está) para ver qué imprime y si da error. Si da error, explicá la causa en una línea y cómo arreglarlo.
4. **Revisá cada invocación**, en orden:
   - qué inciso resuelve;
   - si usó la **función correcta con los argumentos correctos** (ver tabla y errores típicos de abajo);
   - si el **valor** es correcto (recalculado como en la regla 2);
   - si lo que imprime o escribe como interpretación es correcto según `teoria_resumen.md`.
5. **Revisá qué falta.** Compará los incisos del enunciado con lo que hay en el archivo y listá lo que no está, con la función a usar.
6. **Si el archivo usa las variables `MENSAJE`, `N`, `ENTRADA`, `SALIDA`**, podés además correr `SegundoParcial/Revisar.py` (poniendo el nombre del archivo en `ARCHIVO`) como verificación extra; su veredicto es confiable para esos casilleros. No es obligatorio.

## Formato de la respuesta

**Siempre decile qué hacer para que quede bien.** Para cada ❌, cada ⚠️ y cada inciso que falta, dale la **línea de código exacta** para corregirlo o agregarlo, escrita con SUS nombres de variables y su estilo de import (si escribe `FuncionesParcial2.huffman(...)`, respetalo), lista para copiar en su archivo, y el **valor que le tiene que dar** al correrla. Antes de proponerla, comprobá en el script temporal que esa línea da ese valor. Si el problema es de interpretación (texto), dale la frase corregida.

Una línea por resultado, con el número de línea del archivo:

- `línea 12 · entropia = 1.7884` → **✅ Bien** (1a, entropía H(S)).
- `línea 15 · L_ext = 1.7945` → **❌ Mal**: es L_n/n; el inciso pide L_n por bloque = 5.3835. Arreglo: `resumen_codigo(pe, cod_ext)["L"]`.
- `línea 20 · cap = capacidad_binaria(m, 0.0001)` → **⚠️ Bien, pero**: ... (cuando el valor es correcto pero hay algo que aclarar en la respuesta escrita).

Después:
- **Falta**: incisos que no están, cada uno con la línea exacta para agregar y el valor que tiene que dar.
- **Archivo**: si corre, imports, si sirve para entregar tal cual.
- **Total**: cuántos bien y cuántos mal.

## Qué función corresponde a cada pedido

| Piden | Función correcta (argumentos) |
|---|---|
| probabilidades de un mensaje | `alfabeto_y_probabilidades(mensaje)` → (alfabeto, probs) |
| entropía | `CalcEntropia(probs)` (bits) |
| código óptimo | `huffman(probs)`; otro código con la misma L e instantáneo también es válido |
| Shannon-Fano | `shannon_fano(probs)` |
| L, η, R | `resumen_codigo(probs, codigos)` o `get_longitudMedia` + `rendimiento_redundancia` |
| extensión de orden n | `pe = extension_fuente(probs, n)`; óptimo: `huffman(pe)`; L, η, R: `resumen_codigo(pe, cod_ext)` (L por bloque) |
| Primer Teorema | `detalle_primer_teorema(probs_ORIGINALES, codigo_de_la_extensión, n)` |
| clasificar un código / Kraft | `clasifica(codigo)`, `es_instantaneo`, `es_univocamente_decodificable`, `calcular_kraft` |
| tasa de compresión | `tasa_compresion_codigo(mensaje, alfabeto, codigos)` (sin bytes extra) |
| decodificar | `decodificar_cadena(cadena, simbolos, codigos)` |
| RLC | `rlc_texto(m)`, `rlc_comprimir(m)`, tasa = `tasa_compresion(m, rlc_comprimir(m))` |
| Hamming de un código | `analizar_codigo_hamming(codigos)` → (d_min, detecta, corrige) |
| Levenshtein | `distancia_levenshtein(a, b)` |
| paridad | proteger: `generar_mensaje_con_paridad(texto)`; corregir: `analizar_matriz_paridad(filas_de_bits(bits))["mensaje"]` (fila 1 = LRC) |
| canal desde secuencias | `canal_desde_secuencias(entrada, salida)` → (A, probs, B, matriz) |
| canal dado por matriz | usar la matriz y las a priori del enunciado (si no las dan, preguntar o aclarar que se suponen equiprobables) |
| sin ruido / determinante | `es_sin_ruido(m)` (columnas), `es_determinante(m)` (filas) |
| P(b), P(a,b), P(a/b), H(A/b) | `probabilidades_salida`, `probabilidades_simultaneas`, `probabilidades_a_posteriori`, `entropias_a_posteriori` |
| H(A/B), H(B/A), H(A,B), I | `equivocacion`, `perdida`, `entropia_afin`, `informacion_mutua` (todas con `(probs, matriz)`) |
| reducciones suficientes | `reducir_canal(m)` |
| canales en serie | `canal_serie(m1, m2)`; comparar `informacion_mutua` antes y después |
| capacidad | 2 entradas: `capacidad_binaria(m_o_reducido, 0.0001)` → (C, P(a1)); fórmula directa: `capacidad_canal(m)` |
| probabilidad de error | `probabilidad_error(probs, matriz_ORIGINAL)` (guía); `a_posteriori=True` es la regla de la diapositiva |

## Errores típicos a revisar SIEMPRE

- L de la extensión por símbolo (L_n/n) cuando se pide L_n por bloque; L, η y R que no cierran (η = n·H/L_n).
- Primer Teorema con las probabilidades de la extensión (va con las ORIGINALES).
- Código de la extensión armado concatenando palabras en vez de `huffman(extension_fuente(...))`.
- Tasa de compresión con `tasa_compresion` + `codificar_mensaje` (cuenta un byte extra).
- Fila de una matriz que no suma 1.
- Capacidad informada con las a priori o con 0,5/0,5 (van las P que maximizan).
- P_E calculada con el canal reducido o con probabilidades equivocadas; P_E mayor que 1 - max P(a).
- Mensaje corregido dejado en bits (va el texto) o primera fila tomada como carácter (es la LRC).
- `detecta`/`corrige` de Hamming con fórmulas cambiadas (detecta d-1, corrige ⌊(d-1)/2⌋).
- Interpretaciones que contradicen a la cátedra (por ejemplo, llamar "pérdida" a H(A/B): H(A/B) es la equivocación o ruido; H(B/A) es la pérdida).
- El .py de entrega que importa un módulo propio no entregado.
