# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 10:32:28 2017

@author: Gloriana
"""

import numpy
import random
from Graficador import Graficador

class GeneradorDatos:
    """
    @param media1, media de la dimension 1 (temperatura)
    @param media2, media de la dimension 2 (humedad)
    @param desv1, desviacion estandar de la dimension 1
    @param desv2, desviacion estandar de la dimension 2
    @param 
    """
    
    def generarDatosGauss2D(self, media1, desv1, media2, desv2, cantidadDatos):
        muestrasDimension1 = numpy.random.normal(media1, desv1, cantidadDatos)
        muestrasDimension2 = numpy.random.normal(media2, desv2, cantidadDatos)
        #Crea matriz de ceros
        matrizX = numpy.zeros((2, cantidadDatos))
        for i in range(0, cantidadDatos):
            #Se concatena c/muestra en la matriz X
            matrizX[0, i] = muestrasDimension1[i]
            matrizX[1, i] = muestrasDimension2[i]
        return  matrizX
    
def principal():
    generadorDatos = GeneradorDatos()
    N = 5
    matrizXc1 = generadorDatos.generarDatosGauss2D(28, 3, 20, 10, N)
    print(matrizXc1)


principal()
        
    
    