# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 11:02:27 2017

@author: Dereck & Gloriana
"""


import numpy
from GeneradorDatos import GeneradorDatos
import matplotlib.pyplot as plt
from Graficador import Graficador


class AmontonadorKmedias:
    """
    Constructor del amontonador de K medias
    @param K, la cantidad de clases
    @param X, la matriz de datos
    """
    def __init__(self, K, X):
        #Llama a generador de datos
        self.__generadorDatos = GeneradorDatos();
        self.__X = X;
        self.__N = len(X[0])
        
        #Escoge un punto menor para crear un centroide inicial
        self.__puntoMenor = self.__escogerPuntoMinimo()
        print("Punto menor: ", self.__puntoMenor)
        
        #Escoge un punto mayor para crear el otro centroide inicial
        self.__puntoMax = self.__escogerPuntoMaximo()
        print("Punto max: ", self.__puntoMax)
        
        #Encuentra el delta entre los puntos creados
        delta = numpy.linalg.norm(self.__puntoMax - self.__puntoMenor)
        print("Delta: ", delta)
        
        #Inicializa una matriz de ceros para guardar los nuevos centroides
        self.__matrizCentroides = numpy.zeros((2, K))
        
        #Inicializa una matriz de ceros para etiquetar cada punto
        self.__matrizPesos = numpy.zeros((self.__N, K))
        
        #Inicializa aleatoriamente los centroides
        for i in range(0, K):
            puntoAleatorio = self.__generadorDatos.generarPuntoAleatorio(self.__puntoMenor[0], self.__puntoMax[0] - delta, self.__puntoMenor[1] + delta, self.__puntoMax[1]);
            self.__matrizCentroides[0, i] = puntoAleatorio[0];
            self.__matrizCentroides[1, i] = puntoAleatorio[1]
        print("Centroides Iniciales:",self.__matrizCentroides)
                
    
    """
    Consigue los centroides
    """
    def getCentroides(self):
        return self.__matrizCentroides;
    
    """
    Consigue la matriz de pesos
    """
    def getMatrizPesos(self):
        return self.__matrizPesos
    
    """
    Hace un set de algún valor
    """
    def setValor(self, fila, columna, valor):
        self.__X[fila][columna] = valor
    
    """    
    Hace un set de los centroides
    """
    def setCentroides(self, valor):
        self.__matrizCentroides = valor
    
    """
    Hace un set de la matriz de pesos
    """
    def setMatrizPesos(self, valor):
        self.__matrizPesos = valor

            
    """
    Retorna el punto minimo en X
    """    
    def __escogerPuntoMinimo(self):
        dimensiones = self.__X.shape
        #Itera por cada columna, o cada dato del K actual
        puntoMenor = self.__X[:, 0]
        magnitudMenor = numpy.linalg.norm(puntoMenor)
        for i in range(1, dimensiones[1]):
            puntoActual = self.__X[:, i]
            magnitud = numpy.linalg.norm(puntoActual)
            if(magnitud < magnitudMenor):
                magnitudMenor = magnitud
                puntoMenor = puntoActual
        puntoMenor = numpy.transpose(puntoMenor)
        
        return puntoMenor
                
    """
    Retorna el punto máximo en X
    """
    def __escogerPuntoMaximo(self):
        dimensiones = self.__X.shape
        #Itera por cada columna, o cada dato del K actual
        puntoMax = self.__X[:, 0]
        magnitudMax = numpy.linalg.norm(puntoMax)
        for i in range(1, dimensiones[1]):
            puntoActual = self.__X[:, i]
            magnitud = numpy.linalg.norm(puntoActual)
            if(magnitud > magnitudMax):
                magnitudMax = magnitud;
                puntoMax = puntoActual;
        puntoMax = numpy.transpose(puntoMax)
        
        return puntoMax
    
    """
    Va creando una asociación del punto basado en su etiqueta con su centroide correspondiente
    @K, la K en la que se va a amontonar
    """
    def amontonarK(self, K):
        #Consigo las etiquetas
        etiquetas = self.__matrizPesos
        #Itero en todos los datos
        for i in range (0, self.__N):
            #Si tiene un 1 en esa clase, une con rojo, y sino une con azul
            if (etiquetas[i, K] == 1):
                #Adjunto el dato correspondiente al centroide en X y en Y
                datosx = [self.__matrizCentroides[0, 0]] + [self.__X[0, i]]
                datosy = [self.__matrizCentroides[0, 1]] + [self.__X[1, i]]
                #Añado las líneas con los puntos al plot
                plt.plot(datosx, datosy, color = "red", marker = "o")
                
            else:
                #Adjunto el dato correspondiente al centroide en X y en Y
                datosx = [self.__matrizCentroides[1, 0]] + [self.__X[0, i]]
                datosy = [self.__matrizCentroides[1, 1]] + [self.__X[1, i]]
                #Añado las líneas con los puntos al plot
                plt.plot(datosx, datosy, color = "blue", marker = "o")
                
    """
    Realiza el etiquetado
    """
    def etiquetar(self):
        #Consigue la matriz de pesos
        resultado = self.__matrizPesos
        
        #Contador para colocar bien el resultado en la matriz pesos
        contadorIndices = 0   
        #Acumulador distancia 1
        distancia1 = 0
        #Acumulador distancia 2
        distancia2 = 0
        
        for i in range(0, self.__N):
            parOrdenado= [self.__X[0][i], self.__X[1][i]]
            #Ambos parámetros suponen un par ordenado
            distancia1 = numpy.linalg.norm(parOrdenado - self.__matrizCentroides[0])
            distancia2 = numpy.linalg.norm(parOrdenado - self.__matrizCentroides[1])
            
            #Se escribe un 1 si el elemento es más cercano a la primera clase
            if (distancia1 < distancia2):
                resultado[contadorIndices, 0] = 1
                #Se escribe un 0 del otro lado
                resultado[contadorIndices, 1] = 0
                #Incrementa el contador
                contadorIndices += 1
            else:
                #Sino se le asigna un 1 a la etiqueta 2
                resultado[contadorIndices, 1] = 1
                #Y se escribe un 0 del otro lado
                resultado[contadorIndices, 0] = 0
                #Se incrementa el contador
                contadorIndices += 1
                
        #Le asigna la matriz de resultado a la matriz de pesos
        self.setMatrizPesos(resultado)
    
    """
    Se hace un recálculo de las K medias
    """
    def recalcularKmedias(self):
        #Inicializo acumuladores como listas vacías
        acumuladorK1 = []
        acumuladorK2 = []
        #Busco la cantidad de filas de la matriz de pesos
        filaPesos = len(self.__matrizPesos)
        contador2 = 0
        fila = 0
        #Se realiza una verificación con la matriz de pesos
        #Separa cada par, de acuerdo a su cercania a un centroide
        for i in range(0, filaPesos):
            elemento = self.__matrizPesos[fila, 0]
            if elemento == 1:
                valor = [self.__X[0][contador2], self.__X[1][contador2]]
                #Incrementa el valor en acumulador de K1
                acumuladorK1 += valor 
                #Incrementa contador
                contador2 += 1
                #Incrementa fila
                fila += 1

            else:
                 valor = [self.__X[0][contador2], self.__X[1][contador2]]
                 #Incrementa el valor en acumulador de K2
                 acumuladorK2 += valor
                 #Incrementa contador
                 contador2 += 1
                 #Incrementa fila
                 fila += 1
                 
        #Promedia los datos acumulados para X y Y, y los asigna a la nueva media
        mediaNuevaX = self.promediarListaParesOrdenados(acumuladorK1)
        mediaNuevaY = self.promediarListaParesOrdenados(acumuladorK2)
        print("Recalculo Centroides:",[mediaNuevaX ,mediaNuevaY])
        
        #Asgina los nuevos centroides con la nueva media en X y en Y
        self.setCentroides(numpy.array([mediaNuevaX, mediaNuevaY]))
        
    """    
    Realiza un promediado de las X con ellas mismas, así como las Y entre sí mismas
    @param lista, la lista que se recibe para realizar el promediado
    """
    def promediarListaParesOrdenados(self, lista):
        #Usa acumuladores para separar X con Y
        acumuladorFilas = 0   
        acumuladorColumnas = 0
        #Inicializa un contador
        contador = 0
        largo = len(lista) // 2
        
        #Recibe una lista plana y las separa por medio del siguiente contador
        for i in lista:
            #Si es par, acumula en filas
            if (contador % 2 == 0):
                acumuladorFilas += i
                contador += 1
            #Sino, acumula en columnas
            else:
                acumuladorColumnas += i
                contador += 1
                
        #Realiza el promediado de X y de Y
        promedioX = acumuladorFilas / largo
        promedioY= acumuladorColumnas / largo
        
        #Retorna una lista con los promediados
        return [promedioX, promedioY]

    
    
    