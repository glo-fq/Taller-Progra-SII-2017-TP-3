# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 11:02:27 2017

@author: Dereck
"""


import numpy
from GeneradorDatos import GeneradorDatos
import matplotlib.pyplot as plt
from Graficador import Graficador
from tkinter import *


class AmontonadorKmedias:
    def __init__(self, K, X):
        self.__generadorDatos = GeneradorDatos();
        self.__X = X;
        self.__N = len(X[0])
        self.__puntoMenor = self.__escogerPuntoMinimo();
        print("Punto menor: ", self.__puntoMenor)
        self.__puntoMax = self.__escogerPuntoMaximo();
        print("Punto max: ", self.__puntoMax)
        delta = numpy.linalg.norm(self.__puntoMax - self.__puntoMenor);
        print("Delta: ", delta)
        self.__matrizCentroides = numpy.zeros((2, K));
        self.__matrizPesos = numpy.zeros((self.__N, K))
        
        #Inicializa aleatoriamente los centroides
        for i in range(0, K):
            puntoAleatorio = self.__generadorDatos.generarPuntoAleatorio(self.__puntoMenor[0], self.__puntoMax[0] - delta, self.__puntoMenor[1] + delta, self.__puntoMax[1]);
            self.__matrizCentroides[0, i] = puntoAleatorio[0];
            self.__matrizCentroides[1, i] = puntoAleatorio[1]
        print("Centroides Iniciales:",self.__matrizCentroides)
                
    def getCentroides(self):
        return self.__matrizCentroides;
    
    def getMatrizPesos(self):
        return self.__matrizPesos
    
    def setValor(self, fila, columna, valor):
        self.__X[fila][columna] = valor
        
    def setCentroides(self, valor):
        self.__matrizCentroides = valor
    
    def setMatrizPesos(self, valor):
        self.__matrizPesos = valor

            
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
    

    def amontonarK(self, K):
        etiquetas = self.__matrizPesos
        for i in range (0, self.__N):
            if (etiquetas[i, K] == 1):
                #Adjunto el dato correspondiente al centroide en X y en Y
                datosx = [self.__matrizCentroides[0, 0]] + [self.__X[0, i]]
                datosy = [self.__matrizCentroides[0, 1]] + [self.__X[1, i]]
                
                #Añado las líneas con los puntos al plot
            else:
                datosx = [self.__matrizCentroides[1, 0]] + [self.__X[0, i]]
                datosy = [self.__matrizCentroides[1, 1]] + [self.__X[1, i]]
                
            plt.plot(datosx, datosy, marker="o")
    
    def etiquetar(self):
        resultado = self.__matrizPesos
        
        contadorIndices = 0   #contador para colocar bien el resultado en la matriz pesos
        distancia1 = 0    #acumulador distancia 1
        distancia2 = 0    #acumulador distancia 2
        
        for i in range(0, self.__N):
            parOrdenado= [self.__X[0][i], self.__X[1][i]]
            distancia1 = numpy.linalg.norm(parOrdenado - self.__matrizCentroides[0])#Ambos parametros suponen un par ordenado
            distancia2 = numpy.linalg.norm(parOrdenado - self.__matrizCentroides[1])#Cambie esto, es la distancia del par al centroide no al punto min o max
            #valor = 1
            if (distancia1 < distancia2):   #Ponemos 1 si es el elemento mas cercano a etiqueta 1
                resultado[contadorIndices, 0] = 1
                resultado[contadorIndices, 1] = 0
                contadorIndices += 1
            else:
                #Sino ponemos 1 a etiqueta 2
                resultado[contadorIndices, 1] = 1
                resultado[contadorIndices, 0] = 0
                contadorIndices += 1
                
        self.setMatrizPesos(resultado)
    
    
    def recalcularKmedias(self):
        
        acumuladorK1 = []
        acumuladorK2 = []
        filaPesos = len(self.__matrizPesos)
        contador2 = 0
        fila = 0
        for i in range(0, filaPesos): #verifica con la lista de pesos
            elemento = self.__matrizPesos[fila, 0]
            if elemento == 1:
                valor=[self.__X[0][contador2],self.__X[1][contador2]]
                acumuladorK1 += valor #Separa cada par, de acuerdo a su cercania a un centroide
                contador2 += 1
                fila += 1

            else:
                 valor = [self.__X[0][contador2], self.__X[1][contador2]]
                 acumuladorK2 += valor
                 contador2 += 1
                 fila += 1
                 
        mediaNuevaX = self.promediarListaParesOrdenados(acumuladorK1) #Falta agregar la excepcion cuando es 0/0
        mediaNuevaY = self.promediarListaParesOrdenados(acumuladorK2)#Actualizacion: parece que nunca un centroide se queda sin un dato relacionado
        
        print("Recalculo Centroides:",[mediaNuevaX ,mediaNuevaY])
        self.setCentroides(numpy.array([mediaNuevaX, mediaNuevaY]))
        
    def promediarListaParesOrdenados(self, lista): #Promedia las X con ellas mismas y las Y tambien
        acumuladorFilas = 0   #usa acumuladores para separar X con Y
        acumuladorColumnas = 0
        contador = 0
        largo = len(lista) // 2
        for i in lista: #recibe una lista plana y se separa por medio del contador
            if (contador % 2 == 0): #contador par, con X
                acumuladorFilas += i
                contador += 1
            else:
                acumuladorColumnas += i  #contador impar, con Y
                contador += 1
                
        promedioX = acumuladorFilas / largo  #promedia X y Y
        promedioY= acumuladorColumnas / largo
        return [promedioX, promedioY]
    
def principal():
    K = 2 #cantidad de clases
    graficador = Graficador();
    generadorDatos = GeneradorDatos();
    N = 50 #cantidad de datos
    #matrizXc1 = generadorDatos.generarDatosGauss2D(28, 3, 20, 10, N);
    #matrizXc2 = generadorDatos.generarDatosGauss2D(5, 3, 10, 10, N);
    matrizXc1 = generadorDatos.generarDatosGauss2D(15, 10, 20, 10, N);
    matrizXc2 = generadorDatos.generarDatosGauss2D(5, 10, 10, 10, N);
    X = numpy.concatenate((matrizXc1, matrizXc2), axis = 1 )
    
    """Iteración 1"""
    #Llamo a la clase
    Y = AmontonadorKmedias(K, X)
    #Consigo los centroides
    centroides = AmontonadorKmedias.getCentroides(Y)
    #Grafico los centroides
    
    #Realizo la fase de etiquetado
    Y.etiquetar()
    
    #Se grafican las líneas que unen los puntos con los centroides
    amontonadoCentroide1 = Y.amontonarK(0)
    
    plt.plot(centroides[:, 0], centroides[:, 1], "y", marker = "o", ls="--", label = "Centroide original")
    #Muestro el gráfico
    plt.show()
    
    """Iteración 2:"""
    #Recalculo los centroidesw
    Y.recalcularKmedias()
    #Reasigno las etiquetas
    Y.etiquetar()
    centroides = AmontonadorKmedias.getCentroides(Y)
    
    #Grafica las líneas que unen los puntos con los centroides
    amontonadoCentroide1 = Y.amontonarK(0)
    plt.plot([centroides[0][0], centroides[1][0]], [centroides[0][1], centroides[1][1]], "red", marker="o", ls="--", label = "Centroide Nuevo")
    plt.legend(loc="upper left")
    plt.show()
    
    """Iteración 3:"""
    #Recalculo los centroidesw
    Y.recalcularKmedias()
    #Reasigno las etiquetas
    Y.etiquetar()
    centroides = AmontonadorKmedias.getCentroides(Y)
    
    #Grafica las líneas que unen los puntos con los centroides
    amontonadoCentroide1 = Y.amontonarK(0)
    plt.plot([centroides[0][0], centroides[1][0]], [centroides[0][1], centroides[1][1]], "red", marker="o", ls="--", label = "Centroide Nuevo")
    plt.legend(loc="upper left")
    plt.show()
    
    """Iteración 4:"""
    #Recalculo los centroidesw
    Y.recalcularKmedias()
    #Reasigno las etiquetas
    Y.etiquetar()
    centroides = AmontonadorKmedias.getCentroides(Y)
    
    #Grafica las líneas que unen los puntos con los centroides
    amontonadoCentroide1 = Y.amontonarK(0)
    plt.plot([centroides[0][0], centroides[1][0]], [centroides[0][1], centroides[1][1]], "red", marker="o", ls="--", label = "Centroide Nuevo")
    plt.legend(loc="upper left")
    plt.show()
    
    """Iteración 5:"""
    #Recalculo los centroidesw
    Y.recalcularKmedias()
    #Reasigno las etiquetas
    Y.etiquetar()
    centroides = AmontonadorKmedias.getCentroides(Y)
    
    #Grafica las líneas que unen los puntos con los centroides
    amontonadoCentroide1 = Y.amontonarK(0)
    plt.plot([centroides[0][0], centroides[1][0]], [centroides[0][1], centroides[1][1]], "red", marker="o", ls="--", label = "Centroide Nuevo")
    plt.legend(loc="upper left")
    plt.show()
    
    
    """Iteración 6:"""
    #Recalculo los centroidesw
    Y.recalcularKmedias()
    #Reasigno las etiquetas
    Y.etiquetar()
    centroides = AmontonadorKmedias.getCentroides(Y)
    
    #Grafica las líneas que unen los puntos con los centroides
    amontonadoCentroide1 = Y.amontonarK(0)
    plt.plot([centroides[0][0], centroides[1][0]], [centroides[0][1], centroides[1][1]], "red", marker="o", ls="--", label = "Centroide Nuevo")
    plt.legend(loc="upper left")
    plt.show()
    
    
    
principal()
    
        

    
    
    
    