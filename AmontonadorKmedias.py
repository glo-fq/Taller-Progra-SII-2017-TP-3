# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 11:02:27 2017

@author: saul1917
"""


import numpy
from GeneradorDatos import GeneradorDatos
import matplotlib.pyplot as plt
from Graficador import Graficador


class AmontonadorKmedias:
    def __init__(self, K, X):
        self.__generadorDatos = GeneradorDatos();
        self.__X = X;
        self.__N = len(X[0])
        self.puntoMenor = self.__escogerPuntoMinimo();
        print("Punto menor: ", self.puntoMenor)
        self.puntoMax = self.__escogerPuntoMaximo();
        print("Punto max: ", self.puntoMax)
        delta = numpy.linalg.norm(self.puntoMax - self.puntoMenor);
        print("Delta: ", delta)
        self.__matrizCentroides = numpy.zeros((2, K));
        self.__matrizPesos = numpy.zeros((self.__N, K))
        #Inicializa aleatoriamente los centroides
        for i in range(0, K):
            puntoAleatorio = self.__generadorDatos.generarPuntoAleatorio(self.puntoMenor[0], self.puntoMax[0] + delta, self.puntoMenor[1] - delta, self.puntoMax[1]);
            self.__matrizCentroides[0, i] = puntoAleatorio[0];
            self.__matrizCentroides[1, i] = puntoAleatorio[1]
        #self.__matrizPesos[0, 0] = self.puntoMenor[0]
        #self.__matrizPesos[1, 0] = self.puntoMenor[1]
        #self.__matrizPesos[0, 1] = self.puntoMax[0]
        #self.__matrizPesos[1, 1] = self.puntoMax[1]
        print(self.__matrizCentroides)
                
    def getCentroides(self):
        return self.__matrizCentroides;
    
    def setValor(self, fila, columna, valor):
        self.__X[fila][columna] = valor

            
    """
    Retorna el punto minimo en X
    """    
    def __escogerPuntoMinimo(self):
        dimensiones = self.__X.shape;
        #Itera por cada columna, o cada dato del K actual
        puntoMenor = self.__X[:, 0];
        magnitudMenor = numpy.linalg.norm(puntoMenor);
        for i in range(1, dimensiones[1]):
            puntoActual = self.__X[:, i];
            magnitud = numpy.linalg.norm(puntoActual);
            if(magnitud < magnitudMenor):
                magnitudMenor = magnitud;
                puntoMenor = puntoActual;
        puntoMenor = numpy.transpose(puntoMenor)
        return puntoMenor;
                
    def __escogerPuntoMaximo(self):
        dimensiones = self.__X.shape;
        #Itera por cada columna, o cada dato del K actual
        puntoMax = self.__X[:, 0];
        magnitudMax = numpy.linalg.norm(puntoMax);
        for i in range(1, dimensiones[1]):
            puntoActual = self.__X[:, i];
            magnitud = numpy.linalg.norm(puntoActual);
            if(magnitud > magnitudMax):
                magnitudMax = magnitud;
                puntoMax = puntoActual;
        puntoMax = numpy.transpose(puntoMax)
        return puntoMax;
    
    def etiquetar(self):
        resultado = self.__matrizPesos
        
        contadorIndices = 0   #contador para colocar bien el resultado en la matriz pesos
        distancia1 = 0    #acumulador distancia 1
        distancia2 = 0    #acumulador distancia 2
        
        for i in range(0, self.__N):
            parOrdenado= [self.__X[0, i], self.__X[1, i]]
            distancia1 = numpy.linalg.norm(parOrdenado - self.puntoMenor)#Ambos parametros suponen un par ordenado
            distancia2 = numpy.linalg.norm(parOrdenado - self.puntoMax)
            valor = 1
            if (distancia1 < distancia2):   #Ponemos 1 si es el elemento mas cercano a etiqueta 1
                resultado[contadorIndices, 0] = valor
                contadorIndices += 1
            else:
                #Sino ponemos 1 a etiqueta 2
                resultado[contadorIndices, 1] = valor
                contadorIndices += 1
                
            
            
        return resultado
    
    def amontonarK(self, K):
        etiquetas = self.__matrizPesos
        for i in range (0, self.__N):
            if (etiquetas[i, K] == 0):
                #Adjunto el dato correspondiente al centroide en X y en Y
                datosx = [self.__matrizCentroides[0, 0]] + [self.__X[0, i]]
                datosy = [self.__matrizCentroides[0, 1]] + [self.__X[1, i]]
                #Añado las líneas con los puntos al plot
            else:
                datosx = [self.__matrizCentroides[1, 0]] + [self.__X[0, i]]
                datosy = [self.__matrizCentroides[1, 1]] + [self.__X[1, i]]
            plt.plot(datosx, datosy, marker="o")
                
    
    
def principal():
    K = 2;
    graficador = Graficador();
    generadorDatos = GeneradorDatos();
    N = 50; #cantidad de datos
    matrizXc1 = generadorDatos.generarDatosGauss2D(28, 3, 20, 10, N);
    matrizXc2 = generadorDatos.generarDatosGauss2D(5, 3, 10, 10, N);
    X = numpy.concatenate((matrizXc1, matrizXc2), axis = 1 )
    graficador.graficarPuntos(X)
    Y = AmontonadorKmedias(K, X)
    centroides = AmontonadorKmedias.getCentroides(Y)
    plt.plot(centroides[:, 0], centroides[:, 1], "r")
    etiquetas = Y.etiquetar()
    amontonadoCentroide1 = Y.amontonarK(0)
    #amontonadoCentroide2 = Y.amontonarK(1)
    plt.show()
    print("Etiquetas: ", etiquetas)
    
    
principal()
        
                
                        
            
                
               