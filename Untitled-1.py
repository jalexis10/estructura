import heapq
import os
import tkinter as tk
from tkinter import filedialog

# Crear una instancia de Tkinter
root = tk.Tk()

# Ocultar la ventana principal de Tkinter
root.withdraw()

class NodoHuffman:
    def __init__(self, caracter, frecuencia):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

    def __lt__(self, other):
        return self.frecuencia < other.frecuencia


class CodificadorHuffman:
    def __init__(self):
        self.codificacion = {}
        self.arbol_huffman = None

    def construir_arbol(self, texto):
        frecuencias = self.calcular_frecuencias(texto)
        cola_prioridad = []
        for caracter, frecuencia in frecuencias.items():
            nodo = NodoHuffman(caracter, frecuencia)
            heapq.heappush(cola_prioridad, nodo)

        while len(cola_prioridad) > 1:
            nodo_izq = heapq.heappop(cola_prioridad)
            nodo_der = heapq.heappop(cola_prioridad)
            nodo_padre = NodoHuffman(None, nodo_izq.frecuencia + nodo_der.frecuencia)
            nodo_padre.izquierda = nodo_izq
            nodo_padre.derecha = nodo_der
            heapq.heappush(cola_prioridad, nodo_padre)

        self.arbol_huffman = heapq.heappop(cola_prioridad)

    def calcular_frecuencias(self, texto):
        frecuencias = {}
        for caracter in texto:
            frecuencias[caracter] = frecuencias.get(caracter, 0) + 1
        return frecuencias

    def generar_codificacion(self, nodo_actual, codigo_actual):
        if nodo_actual.caracter is not None:
            self.codificacion[nodo_actual.caracter] = codigo_actual
            return

        self.generar_codificacion(nodo_actual.izquierda, codigo_actual + "0")
        self.generar_codificacion(nodo_actual.derecha, codigo_actual + "1")

    def codificar_texto(self, texto):
        codigo = ""
        for caracter in texto:
            codigo += self.codificacion[caracter]
        return codigo

    def decodificar_texto(self, codigo):
        texto = ""
        nodo_actual = self.arbol_huffman
        for bit in codigo:
            if bit == "0":
                nodo_actual = nodo_actual.izquierda
            else:
                nodo_actual = nodo_actual.derecha

            if nodo_actual.caracter is not None:
                texto += nodo_actual.caracter
                nodo_actual = self.arbol_huffman

        return texto

    def comprimir_archivo(self, nombre_archivo):
        nombre_archivo_comprimido = nombre_archivo.split(".")[0] + "_comprimido.txt"
        with open(nombre_archivo, "r") as archivo, open(nombre_archivo_comprimido, "wb") as archivo_comprimido:
            texto = archivo.read().rstrip()

            self.construir_arbol(texto)
            self.generar_codificacion(self.arbol_huffman, "")

            codigo = self.codificar_texto(texto)
            padding = 8 - (len(codigo) % 8)
            codigo = "{0:08b}".format(padding) + codigo + "0" * padding

            datos_bytes = bytearray()
            for i in range(0, len(codigo), 8):
                byte = codigo[i:i+8]
                datos_bytes.append(int(byte, 2))

            archivo_comprimido.write(bytes(datos_bytes))

        print("El texto se ha codificado y el archivo se ha comprimido correctamente.")

        tasa_compresion = (len(datos_bytes) * 100) / os.path.getsize(nombre_archivo)
        print("La tasa de compresión es del {:.2f}%.".format(tasa_compresion))

    def descomprimir_archivo(self, nombre_archivo):
        nombre_archivo_descomprimido = nombre_archivo.split("_")[0] + "_descomprimido.txt"
        with open(nombre_archivo, "rb") as archivo_comprimido, open(nombre_archivo_descomprimido, "w") as archivo_descomprimido:
            datos_bytes = archivo_comprimido.read()

            bits = ""
            for byte in datos_bytes:
                bits += "{0:08b}".format(byte)

            padding = int(bits[:8], 2)
            bits = bits[8:-padding]

            texto = self.decodificar_texto(bits)
            archivo_descomprimido.write(texto)

        print("El archivo se ha descomprimido correctamente.")


codificador = CodificadorHuffman()

#nombre_archivo = input("Ingrese el nombre del archivo de texto a comprimir (incluyendo la extensión .txt): ")
#codificador.comprimir_archivo(nombre_archivo)

#nombre_archivo_comprimido = input("Ingrese el nombre del archivo comprimido a descomprimir (incluyendo la extensión): ")
#codificador.descomprimir_archivo(nombre_archivo_comprimido)
#nombre_archivo = input("Ingrese el nombre del archivo de texto a comprimir (incluyendo la extensión .txt): ")
# Abrir el cuadro de diálogo de búsqueda de archivos
nombre_archivo = filedialog.askopenfilename(title="Seleccionar archivo", filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")))
codificador.comprimir_archivo(nombre_archivo)

#nombre_archivo_comprimido = input("Ingrese el nombre del archivo comprimido a descomprimir (incluyendo la extensión): ")
nombre_archivo_comprimido = filedialog.askopenfilename(title="Seleccionar archivo", filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")))
codificador.descomprimir_archivo(nombre_archivo_comprimido)