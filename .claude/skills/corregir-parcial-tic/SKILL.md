---
name: corregir-parcial-tic
description: Corrige lo que Lucas resolvió en el parcial de Teoría de la Información (U4-U6): dice si cada inciso está bien o mal, con el valor correcto, según la cátedra.
---

# Corregir el parcial de Teoría de la Información (unidades 4, 5 y 6)

Lucas resolvió un inciso (o un ejercicio entero) con su propio código y te pasa: el enunciado, su código y lo que respondió (números y/o texto). Tenés que decirle **con certeza** si está bien o mal, por qué y cuál es la respuesta correcta. Respondé en español rioplatense, corto y directo.

## Regla de oro: no corregir "a ojo"

Los números NO se juzgan razonando ni de memoria: **se recalculan** con las funciones verificadas de `SegundoParcial/FuncionesParcial2.py` (verificadas contra la clave oficial del parcial 2025 y los resultados de las guías TP4-TP6). La teoría y las convenciones de la cátedra están en `teoria_resumen.md` (en esta misma carpeta): leelo antes de opinar sobre cualquier texto. Si algo no se puede verificar con certeza, decilo así: "no lo puedo asegurar porque...". Nunca digas "probablemente está bien".

## Pasos

1. **Leé el enunciado y lo que hizo Lucas.** Identificá cada inciso, los datos exactos (copiados carácter por carácter) y qué respondió en cada uno.
2. **Corré su código tal cual**, si lo pasó: copialo a una carpeta temporal y ejecutalo. Fijate si corre, si imprime lo que dice y si importa solo `math` y `random` (más sus módulos). Si es el archivo de entrega, tiene que correr SOLO, sin importar módulos propios que no se entregan.
3. **Si Lucas te pasa SU SCRIPT (sus invocaciones)**: guardalo en `SegundoParcial/` (por ej. `mi_parcial.py`; tiene que definir `MENSAJE`, `N`, `ENTRADA`, `SALIDA`), poné ese nombre en `ARCHIVO` de `SegundoParcial/Revisar.py` y corré `python Revisar.py` desde `SegundoParcial/`. Revisar.py corre su código sin tocarlo, identifica qué inciso es cada variable, dice BIEN/MAL comparando con lo correcto, detecta los errores típicos y lista los incisos que faltan con la función a usar. Su veredicto es el que vale. Los `[ ?? ]` (True/False o valores que no coinciden con nada) los tenés que interpretar vos mirando su código.
   **Si te pasa los NÚMEROS que respondió**: verificalos con `SegundoParcial/Verificar.py`: completá `MENSAJE`, `N`, `ENTRADA`, `SALIDA` y `TUS_RESPUESTAS` con lo que respondió Lucas (lo que no aplique, `None` o vacío) y corré `python Verificar.py` desde `SegundoParcial/`. Su veredicto BIEN/MAL es el que vale para esos casilleros. Para lo que `Verificar.py` no cubre (código dado, matriz dada, Hamming, Levenshtein, RLC, canales en serie, etc.), escribí un script temporal con `from FuncionesParcial2 import *` que calcule el valor correcto y comparalo con tolerancia 0.00015.
4. **Corregí los textos** ("explicar cómo se obtuvieron", "analizar y concluir") contra `teoria_resumen.md`: cada afirmación tiene que ser correcta según la cátedra y coherente con los números verificados. Marcá lo que está mal, lo que falta y lo que sobra. Para comparar, podés correr `ResolverParcial.py` con los mismos datos (Parte 2 y Parte 3 tienen la interpretación de cada resultado y textos modelo).
5. **Respondé** con el formato de abajo.

## Formato de la respuesta

Por cada inciso:

- **✅ Bien** / **❌ Mal** / **⚠️ Bien, pero...** + el valor de Lucas y, si está mal, el correcto.
- **Por qué** (una línea): el error concreto (ej. "usaste las probabilidades de la extensión en el Primer Teorema; van las de la fuente original").

Al final:
- **Textos**: qué corregir o agregar en "explicar" y "concluir" (máximo 5 viñetas, concretas).
- **Archivo .py**: corre solo / no corre (y por qué) / imports.
- **Total**: cuántos incisos bien y cuántos mal.

## Errores típicos a revisar SIEMPRE (los que se marcaron en 2025)

- L de la extensión: es L_n POR BLOQUE (Huffman sobre la extensión). Tiene que cerrar con η = n·H/L_n y R = 1 - η.
- Primer Teorema de la extensión: con las probabilidades de la fuente ORIGINAL y el código de la extensión.
- Código óptimo = Huffman; otras palabras con la misma L también son válidas (verificar que sea instantáneo y con L mínima, no que las palabras sean idénticas).
- Tasa de compresión: (8 bits × caracteres) / (bits del código), sin bytes extra. Se escribe N:1.
- Cada fila de la matriz del canal (y del reducido) suma 1.
- Capacidad: las P que se informan son las que MAXIMIZAN I(A,B), no las a priori ni 0,5/0,5.
- P_E: con la matriz original y las a priori. Nunca mayor que 1 - max P(a) con la regla a posteriori.
- Mensaje corregido: el TEXTO decodificado (ej. SOL), no la tira de bits.
- "No explica": cada inciso necesita su línea de cómo se obtuvo (método + fórmula).
- Conclusión mínima: en fuentes hay que relacionar Shannon - longitud media - códigos compactos - extensiones; en canales, I vs H(A), qué salidas identifican la entrada, reducción, capacidad vs H(A) (Segundo Teorema), P_E y paridad.
- El .py entregado importaba un módulo propio que no se entregó y no corrió.
