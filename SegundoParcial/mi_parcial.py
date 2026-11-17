import FuncionesParcial2
import Explicaciones

MENSAJE = "GIIHGGGHGIHHIHIIGFHH"

alf, prob = FuncionesParcial2.alfabeto_y_probabilidades(MENSAJE)
entropia = FuncionesParcial2.CalcEntropia(prob)
huff = FuncionesParcial2.huffman(prob)
compresion = FuncionesParcial2.tasa_compresion_codigo(MENSAJE, alf, huff)
