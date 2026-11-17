# Teoría de la cátedra (TIC, FI-UNMdP) — unidades 4, 5 y 6

Resumen fiel a `teorias/teoria4.html`, `teoria5.html` y `teoria6.html` y a las guías TP4-TP6. Usá esta notación y estas definiciones al corregir.

## Fuentes y códigos (U4-U5)

- **Fuente de memoria nula**: cada símbolo es independiente del anterior. Las probabilidades de un mensaje se estiman con la **frecuencia relativa** (apariciones / largo).
- **Entropía**: H(S) = Σ P(si)·log2(1/P(si)) bits/símbolo. Máximo log2(q) con q símbolos equiprobables. Con un alfabeto código de r símbolos: H_r(S) = H(S)/log2(r).
- **Longitud media**: L = Σ P(si)·li (binits por símbolo). Para cualquier código unívoco, **L ≥ H_r(S)**.
- **Rendimiento** η = H_r(S)/L; **redundancia** R = 1 - η. η = 1 solo si cada P = r^(-li).
- **Clasificación de códigos**: bloque / no singular / unívocamente decodificable (Sardinas-Patterson) / instantáneo (ninguna palabra es prefijo de otra). Kraft: Σ r^(-li) ≤ 1 es condición para que exista un código instantáneo con esas longitudes.
- **Código compacto**: unívoco con la menor L posible para esa fuente. **Huffman** (unir siempre los dos menos probables) da un código compacto e instantáneo; con empates puede dar otras palabras/longitudes con la misma L. **Shannon-Fano** (ordenar y partir en dos grupos de probabilidad parecida) es instantáneo pero puede tener L mayor que Huffman.
- **Extensión de orden n**: q^n bloques de n símbolos; con memoria nula P(bloque) = producto y **H(S^n) = n·H(S)** (solo vale sin memoria). L_n = longitud media del código de la extensión, **por bloque**. η_n = n·H(S)/L_n. Concatenar las palabras del código original da L_n = n·L (no mejora); para mejorar hay que aplicar Huffman a la extensión.
- **Primer Teorema de Shannon**: con un código compacto de la extensión de orden n, **H_r(S) ≤ L_n/n < H_r(S) + 1/n**. Al crecer n, L_n/n → H. Huffman siempre lo cumple. L_n/n < H es imposible para un código unívoco.
- **Compresión**: tasa = tamaño original / tamaño comprimido, se lee N:1. En el parcial: original = 8 bits ASCII por carácter; comprimido = solo los bits de las palabras código (sin cabeceras ni bytes extra), en bytes enteros. Aproximadamente 8/L. **RLC**: cada ráfaga se guarda como (carácter, cantidad), 2 bytes; comprime solo si las ráfagas promedian más de 2 caracteres. Huffman, Shannon-Fano y RLC son sin pérdida.

## Control de errores (U4)

- **Distancia de Hamming** entre palabras de igual largo: posiciones distintas. **d_min** de un código = la menor entre todos los pares. **Detecta d_min - 1** errores y **corrige ⌊(d_min - 1)/2⌋**.
- **Paridad (par)**: VRC = bit de paridad de cada carácter (7 bits ASCII + paridad al final); LRC = paridad de cada columna; el último bit de la fila LRC es la **paridad cruzada**. Formato de la cátedra: la **primera fila es la LRC** y las siguientes son los caracteres. d_min = 4: detecta hasta 3 errores y corrige 1. Un error simple hace fallar exactamente una fila y una columna; se invierte el bit del cruce. Si fallan más filas/columnas, o solo filas, o solo columnas: hay 2 o más errores, se detectan pero no se corrigen. La respuesta del mensaje es el texto decodificado.
- **BCH** (n, k, t): n = 2^m - 1, d_min ≥ 2t + 1. **Reed-Solomon**: trabaja con símbolos (bytes); n - k = 2t; d_min = n - k + 1 (MDS); una ráfaga dentro de un byte cuenta como un solo error.
- **Levenshtein**: mínimo de inserciones, eliminaciones o sustituciones para pasar de una cadena a otra; sirve con longitudes distintas; con igual longitud es ≤ Hamming.

## Canales (U6, teoria6.html)

- Canal: alfabeto de entrada A = {ai}, de salida B = {bj} y matriz **P(bj/ai)**: **filas = entradas, columnas = salidas; cada fila suma 1**. Desde secuencias: P(b/a) = (veces que entró a y salió b) / (veces que entró a); a priori = frecuencia relativa en la entrada.
- **BSC**: [[1-p, p], [p, 1-p]]; C = 1 - H(p); con p = 0,5, C = 0.
- P(bj) = Σi P(ai)·P(bj/ai). **A posteriori** (Bayes): P(ai/bj) = P(bj/ai)·P(ai)/P(bj). Eventos simultáneos: P(a,b) = P(a)·P(b/a).
- **Entropía a priori** H(A); **a posteriori** H(A/bj) = Σ P(a/bj)·log2(1/P(a/bj)).
- **Equivocación (RUIDO)**: H(A/B) = Σ P(a,b)·log2(1/P(a/b)): información sobre A que queda después de observar B (lo que el canal no deja pasar). 0 ≤ H(A/B) ≤ H(A).
- **Pérdida**: H(B/A) = Σ P(a,b)·log2(1/P(b/a)).
- **Información mutua**: I(A,B) = H(A) - H(A/B) = H(B) - H(B/A) = Σ P(a,b)·log2(P(a,b)/(P(a)P(b))): información sobre A que atraviesa el canal. I ≥ 0 (= 0 si independientes), I(A,B) = I(B,A). **Entropía afín**: H(A,B) = H(A) + H(B) - I(A,B).
- **Canal sin ruido**: un único elemento ≠ 0 en cada **columna** → H(A/B) = 0, I = H(A), C = log2(nro de entradas).
- **Canal determinante**: un único elemento ≠ 0 en cada **fila** → H(B/A) = 0, I = H(B), C = log2(nro de salidas).
- **Reducción**: sumar dos columnas = poner en serie un canal determinante; I(A,B) ≥ I(A,C). **Reducción suficiente**: columnas proporcionales (P(b1/a) = cte·P(b2/a) ∀a) → la I no cambia para ninguna distribución a priori.
- **Canales en serie**: matriz producto; la información mutua no aumenta.
- **Capacidad**: C = max sobre P(ai) de I(A,B). En canales de 2 entradas se busca la P(a1) que maximiza (las funciones lo hacen con paso 0,0001). Las probabilidades que se informan son las que alcanzan el máximo. Siempre I(A,B) ≤ C. Canal uniforme: C = log2(nro de salidas) - H(fila).
- **Regla de decisión y P_E**: P_E = Σ P(E/b)·P(b) = 1 - Σ P(a*, b). La diapositiva llama "regla de máxima posibilidad condicional" a elegir la entrada con mayor P(a/b) (= mayor P(b/a)·P(a)); los resultados de la guía TP6 usan la variante que elige la mayor P(b/a) de la columna. Con entradas equiprobables coinciden. Si Lucas usó cualquiera de las dos y lo aclara, está bien.
- **Segundo Teorema de Shannon**: si una fuente tiene entropía H y el canal capacidad C, con H ≤ C la salida de la fuente se puede transmitir y recuperar con probabilidad de error tan pequeña como se quiera (usando codificación con bloques largos). Si H > C, no.
