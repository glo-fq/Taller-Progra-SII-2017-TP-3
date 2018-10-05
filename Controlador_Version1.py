import math as m
import numpy as np
from GeneradorDatos import GeneradorDatos

class Controlador():
    
    def __init__(self, matrizDatos, clases=2):
        self.__matrizDatos = matrizDatos
        self.__filas = len(matrizDatos)
        self.__columnas = len(matrizDatos[0])
        self.__matrizPesos = np.zeros((self.__filas * self.__columnas // 2, clases))
        

    def setValor(self, fila, columna, valor):
        self.__matrizPesos[fila][columna] = valor

    def getValorDatos(self, fila, columna):
        return self.__matrizDatos[fila][columna]
    
    def __str__(self):
        hilera =  str(self.__matrizPesos) 
        return hilera
    
    def inicializarValorCercanoMediaK1(self):
        datos = GeneradorDatos()
        valorMinimo = min(self.__matrizDatos[0])
        datoAleatorioK1 = datos.generarDatosGauss2D(valorMinimo, 10, valorMinimo, 10, 1)
        
        return (datoAleatorioK1)
    
    def inicializarValorCercanoMediaK2(self):
        datos = GeneradorDatos()
        valorMaximo = max(self.__matrizDatos[1])
        datoAleatorioK2 = datos.generarDatosGauss2D(valorMaximo, 10, valorMaximo, 10, 1)
        
        return (datoAleatorioK2)
    
    
        

    
    def distanciaEuclidiana(self, parVectorial, Kmedia):#sean par Vectorial y clase, un par ordenado ambos
        puntoX = parVectorial[0]
        puntoY = parVectorial[1]
        kMediaX = Kmedia[0][0]
        kMediaY = Kmedia[1][0]
        distancia = m.sqrt(((puntoX-kMediaX)**2) +((puntoY-kMediaY)**2))#formula de distancia euclidiana
        return distancia
        
    
    def faseDeEtiquetado(self):
        
        mediaK1 = self.inicializarValorCercanoMediaK1()#media aleatoria 1
        mediaK2 = self.inicializarValorCercanoMediaK2()#media aleatoria 2
        
        resultado = Controlador(self.__matrizPesos)
        
        columnas = self.__columnas
        
        contadorIndices = 0   #contador para colocar bien el resultado en la matriz pesos
        distancia1 = 0    #acumulador distancia 1
        distancia2 = 0    #acumulador distancia 2
        
        
        for i in range(0, self.__columnas):
            parOrdenado= [self.__matrizDatos[0][i], self.__matrizDatos[1][i]]
            distancia1 = self.distanciaEuclidiana(parOrdenado, mediaK1)#ambos parametros suponen un par ordenado
            distancia2 = self.distanciaEuclidiana(parOrdenado, mediaK2)
            if (distancia1 < distancia2):   #Ponemos 1 si es el elemento mas cercano a etiqueta 1
                valor = 1
                resultado.setValor(contadorIndices, 0, valor)
                contadorIndices += 1
            else:
                valor = 1 #sino ponemos 1 a etiqueta 2
                resultado.setValor(contadorIndices, 1, valor)
                contadorIndices += 1
                
            
            
        return resultado

                 
          
def main():
   x=[[30, 5, 23, 43, 29], [50, 55, 7, 12, 9]]
   controlador= Controlador(x)
   z = controlador.faseDeEtiquetado()
   print(z)
        
main()       
  
    
        
        
        
        
        
    
    