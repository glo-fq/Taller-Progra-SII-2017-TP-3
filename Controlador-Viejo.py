from Amontonador2 import AmontonadorKmedias
import matplotlib.pyplot as plt
from Graficador import Graficador
import numpy
from GeneradorDatos import GeneradorDatos
import time

class Controlador:
    def __init__(self,N, K,P,Xc1,Xd1,Xc2,Xd2,Yc1,Yd1,Yc2,Yd2):
        self.__K = K
        self.__N=N
        self.__P = P   #sea P el numero de iteraciones
        self.__centroide1X = Xc1 
        self.__centroide2X = Xc2
        self.__desviacion1X = Xd1
        self.__desviacion2X = Xd2
        self.__centroide1Y = Yc1
        self.__centroide2Y = Yc2
        self.__desviacion1Y = Yd1
        self.__desviacion2Y = Yd2
        self.__X = self.generarDatos()
        
        
    def iteradorKmedias(self):
        
        contador=1
        Y = AmontonadorKmedias(self.__K, self.__X)
        while contador <= self.__P:
            time.sleep(1)
            if contador==1:
                
                #Consigo los centroides
                centroides = AmontonadorKmedias.getCentroides(Y)
                #Grafico los centroides
                plt.plot(centroides[:, 0], centroides[:, 1], "y", marker = "o", ls="--", label = "Centroide original")
                #Realizo la fase de etiquetado
                Y.etiquetar()
        
                #Se grafican las líneas que unen los puntos con los centroides
                amontonadoCentroide1 = Y.amontonarK(0)
                #Muestro el gráfico
                plt.plot()
                tiempo =time.strftime("%S")
                plt.savefig("figura"+str(tiempo))
                contador+=1
                
            else:
                #Recalculo los centroides
                Y.recalcularKmedias()
                #Reasigno las etiquetas
                Y.etiquetar()
                centroides = AmontonadorKmedias.getCentroides(Y)
                plt.plot([centroides[0][0], centroides[1][0]], [centroides[0][1], centroides[1][1]], "red", marker="o", ls="--", label = "Centroide Nuevo")
                plt.legend(loc="upper left")
                #Grafica las líneas que unen los puntos con los centroides
                amontonadoCentroide1 = Y.amontonarK(0)
                plt.plot()
                tiempo =time.strftime("%S")
                plt.savefig("figura"+str(tiempo))
                contador+=1
            plt.close()
                
    def generarDatos(self):
        graficador = Graficador()
        generadorDatos = GeneradorDatos()
        matrizXc1 = generadorDatos.generarDatosGauss2D(self.__centroide1X,self.__desviacion1X, self.__centroide2X, self.__desviacion2X, self.__N)
        matrizXc2 = generadorDatos.generarDatosGauss2D(self.__centroide1Y,self.__desviacion1Y, self.__centroide2Y, self.__desviacion2Y, self.__N)
        X = numpy.concatenate((matrizXc1, matrizXc2), axis = 1 )
        return  X
              
def principal():
    K = 2 #cantidad de clases
    N = 50 #cantidad de datos
    
    control=Controlador(N,K,3,15,10,20,10,5,10,10,10)
    control.iteradorKmedias()
    
principal()               
 