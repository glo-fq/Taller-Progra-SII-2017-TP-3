# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 08:16:19 2017

@author: Gloriana
"""

import os
from datetime import datetime
import tkinter as tk
from PIL import Image, ImageTk
import time
#from images2gif import writeGif


path = "C:/Users/Gloriana/Documents/TEC/Semestre II/Progra/TP3/Resultados"

instante = datetime.now()
nombreCarpeta = "%s_%s_%s_%s_%s_%s" % (instante.day, instante.month, instante.year, instante.hour, instante.minute, instante.second)

#Nombre final del directorio
nuevoPath = os.path.join(path, nombreCarpeta)

if not os.path.exists(nuevoPath):
    os.makedirs(nuevoPath)
    
    
#Verificar que el nombre de la carpeta no cambie conforme pasa el tiempo
"""for i in range (0, 200):
    print(nuevoPath)"""
    
#Crear un slideshow con tkinter
    
pathPrueba = "C:/Users/Gloriana/Documents/TEC/Semestre II/Progra/TP3/18_11_2017_8_58_19"

os.chdir(pathPrueba)

archivos = [f for f in os.listdir(pathPrueba) if os.path.isfile(os.path.join(pathPrueba, f))]
print(archivos)

"""imagenes = [Image.open(archivo) for archivo in archivos]

size = (150, 150)
for imagen in imagenes:
    im.thumbnail(size, Image.ANTIALIAS)
    
nombreFinal = os.path.join(pathPrueba, "resultado.gif")
writeGif(nombreFinal, imagenes, duration=0.2)"""


"""resultado = []

for filename in archivos:
    resultado.append(imageio.imread(filename))
nombreFinal = os.path.join(pathPrueba, "resultado.gif")
imageio.imsave(nombreFinal, pathPrueba)"""


def pasarAImagenPrevia():
    archivoActual = ""
    try:
        archivoActual = archivos[archivos.index(archivoActual) - 1]
    except:
        archivoActual = archivos[len(archivos) - 1]
        
    imagen.config(image = archivoActual) 
    imagen.image(archivoActual)

def pasarAImagenSig():
    archivoActual = ""
    try:
        archivoActual = archivos[archivos.index(archivoActual) + 1]
    except:
        archivoActual = archivos[0]
    imagen.config(image = archivoActual)
    imagen.image(archivoActual)


root = tk.Tk()

imagen = os.path.join(pathPrueba, "resultado20.jpg")
imagen = str(imagen)

foto = Image.open(imagen) #archivos[0]
imagen = ImageTk.PhotoImage(foto)
time.sleep(1)
label = tk.Label(root, image=imagen)
label.image(imagen)
label.place(relx = .5, rely = .5, anchor = "center")

botonPrevio = tk.Button(root, text="<", command = pasarAImagenPrevia)

botonProximo = tk.Button(root, text=">", command = pasarAImagenSig)


botonPrevio.pack(anchor = "w", side = "LEFT")
botonProximo.pack(anchor = "e", side = "RIGHT")



root.mainloop()






