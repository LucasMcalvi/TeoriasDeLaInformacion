# Segundo Parcial (unidades 4, 5 y 6)

## Mañana: `ResolverParcial.py`

Pegás `MENSAJE`, `N`, `ENTRADA` y `SALIDA` arriba (y, si el parcial da otra cosa, los datos opcionales: `PROBS`, `CODIGO`, `CADENA_A_DECODIFICAR`, `MATRIZ`, `PRIORI`, `MATRIZ2`, `CODIGO_HAMMING`, `LEVENSHTEIN`, `TEXTO_PARIDAD`, `BITS_PARIDAD`, `RLC`), corrés `python ResolverParcial.py` y te imprime (y guarda en `resultado_parcial.txt`): las respuestas para los casilleros, qué significa cada resultado, los textos para "explicar" y "concluir", y extras. Necesita `FuncionesParcial2.py` y `Explicaciones.py` en la misma carpeta. **No se entrega.**

## Para el parcial se usan dos archivos

- **`FuncionesParcial2.py`**: todas las fórmulas en un solo archivo (`from FuncionesParcial2 import *`).
- **`Explicaciones.py`**: interpretación de resultados (`explicar(funcion, args...)`). Necesita `FuncionesParcial2.py` en la misma carpeta. **No se entrega.**

Lo que se entrega es `Parcial_Ej1.py` / `Parcial_Ej2.py` (autocontenidos).

## Todos los archivos

| Archivo | Para qué es |
|---|---|
| `FuncionesParcial2.py` | Todas las funciones juntas: `Formulas.py` + `FormulasCodificacion.py` + `Func_clase4/5/6.py`. |
| `Parcial_Ej1.py` | Plantilla del ejercicio 1 (fuente, Huffman, tasa de compresión, extensión, Primer Teorema). **Autocontenida**: se entrega tal cual, solo cambiando `MENSAJE` y `N`. |
| `Parcial_Ej2.py` | Plantilla del ejercicio 2 (canal, entropías, reducciones, capacidad, P_E, paridad). **Autocontenida**: solo cambiar `ENTRADA` y `SALIDA`. |
| `Func_clase4.py`, `Func_clase5.py`, `Func_clase6.py` | Funciones de las guías TP4, TP5 y TP6 (usan `Formulas.py` y `FormulasCodificacion.py`). |
| `Explicaciones.py` | **No se entrega.** Importa todo de `FuncionesParcial2.py`. `explicar(funcion, args...)` corre la función e imprime qué significa el resultado, cómo se obtuvo, cómo leerlo según el valor y una frase para el parcial. También `explicacion_ej1/2` y `conclusiones_ej1/2`. |
| `Ejemplo_Explicaciones.py` | Recorre todo el parcial 2025 con `FuncionesParcial2.py` y `Explicaciones.py`. |
| `Guia_Interpretacion_Parcial2.pdf` | Guía de interpretación de resultados con respuestas modelo. |
| `Parcial2_2025_visual.pdf` | El segundo parcial 2025 con respuestas, correctas y comentarios del profe. |
| `Func_clase4/5/6.py`, `Formulas.py`, `FormulasCodificacion.py` | Versiones separadas (ya incluidas en `FuncionesParcial2.py`). |

Verificado: con los datos del parcial 2025 las plantillas dan los 33 valores de la clave; las funciones coinciden con los resultados de las guías TP4–TP6.
