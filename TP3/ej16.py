import random

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