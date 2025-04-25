import os
import pandas as pd
import xlwt
import lxml
from lxml import etree
from datetime import datetime
from xlwt import *
import xlsxwriter
import math
from os import listdir
import numpy as np
import sys


def generaExcelStoma(carpeta, es, pixeles, unidad):
    # creamos el excel y la fila de las cabeceras
    wb = xlsxwriter.Workbook(carpeta+'/'+'stomata.xlsx')
    ws = wb.add_worksheet('Summary')#second page
    ws2 = wb.add_worksheet('Stomata')#primary page


    style0 = wb.add_format({'bold': True, 'font_color': 'white', 'fg_color': '0x10'})
    # style0.set_font_color('red')
    # -------------------------------------
    path = carpeta
    # Lista vacia para incluir los xmls
    lstFiles = []
    # Lista con todos los ficheros del directorio:
    lstDir = os.walk(path)  # os.walk()Lista directorios y ficheros
    # Crea una lista de los ficheros xml que existen en el directorio y los incluye a la lista.
    for root, dirs, files in lstDir:
        for fichero in files:
            (nombreFichero, extension) = os.path.splitext(fichero)
            if (extension == ".xml"):
                lstFiles.append(nombreFichero + extension)
            elif (extension != ".xml") and (extension != ".xlsx"):
                extImages = extension
    i = 1
    col = 0 # contador que me va a permitir ir quitando las columnas que me solicitan
    lstFiles.sort()
    # escribimos la cabecera para la primera hoja
    ws.write(0, 0, 'Image name', style0)
    ws.set_column(0, 0, 25)
    ws2.write(0, 0, 'Image name', style0)
    ws2.set_column(0, 0, 25)
    ws.write(0, 1, 'Number of stomata in total', style0)
    ws.set_column(0, 1, 20)
    ws.write(0, 2, 'Average height', style0)
    ws.set_column(0, 2, 20)
    ws.write(0, 3, 'Average width', style0)
    ws.set_column(0, 3, 20)
    ws.write(0, 4, 'Standard height deviation', style0)
    ws.set_column(0, 4, 20)
    ws.write(0, 5, 'Standard width deviation', style0)
    ws.set_column(0, 5, 20)
    escala = es/pixeles
    for fichero in lstFiles:
        # variables que vamos a necesitar
        numEstomas = 0
        numEstomasS = 0
        j = 0
        k = 0
        # alturaTotal = 0
        # anchuraTotal = 0
        listaAlturas = []
        listaAnchuras = []
        doc = etree.parse(carpeta+'/' + fichero)
        filename = doc.getroot()  # buscamos la raiz de nuestro xml
        nomImagen = filename.find("filename")
        # print(filename.text)  # primer elto del que obtenemos el título de nuestro video
        # ws.write(i, 0, nomImagen.text.split('\\')[len(nomImagen.text.split('/'))-1])
        nom =os.path.split(nomImagen.text)
        nom2 = fichero[0:fichero.rfind(".")]
        ws.write(i, 0, nom2+extImages)
        ws2.write(i, 0, nom2+extImages)
        # Calculamos el número de estomas por imagen
        objetos = filename.findall("object")
        j = 0
        while j < len(objetos):
            if objetos[j].find("name").text == "stoma":
                # stoma = objetos[j].find("name")
                numEstomas = numEstomas + 1
                ymax = float(objetos[j].find("bndbox").find("ymax").text)
                ymin = float(objetos[j].find("bndbox").find("ymin").text)
                xmax = float(objetos[j].find("bndbox").find("xmax").text)
                xmin = float(objetos[j].find("bndbox").find("xmin").text)
                alturaEstomaActual = (ymax - ymin) * escala
                #ws3.write(0, 2*k+1, 'Height' + str(k) + '(' + unidad + ')', style0)
                #ws3.write(i, 2*k+1, float('%.2f' % alturaEstomaActual))
                # almacenamos la altura del estoma en un vector
                listaAlturas.append(alturaEstomaActual)
                # Calculamos la media del ancho de los estomas
                anchuraEstomaActual = (xmax - xmin) * escala
                #ws3.write(0, 2*k + 2, 'Width' + str(k) + '('+unidad+')', style0)
                #ws3.write(i, 2*k + 2, float('%.2f' % anchuraEstomaActual))
                listaAnchuras.append(anchuraEstomaActual)

                k = k + 1

                alturaEstomaActual1 = (ymax - ymin) * escala
                # almacenamos la altura del estoma en un vector
                listaAlturas.append(alturaEstomaActual1)
                ws2.write(0, 2*j + 1, 'Height' + str(k) + '(' + unidad + ')', style0)
                ws2.write(i, 2*j + 1, float('%.2f' % alturaEstomaActual1))
                # Calculamos la media del ancho de los estomas
                anchuraEstomaActual1 = (xmax - xmin) * escala
                listaAnchuras.append(anchuraEstomaActual1)
                ws2.write(0, 2*j + 2, 'Width' + str(j), style0)
                ws2.write(i, 2*j + 2, float('%.2f' % anchuraEstomaActual1))
                ws.write(i, 2, float('%.2f' % (np.mean(listaAlturas))))
                ws.write(i, 3, float('%.2f' % (np.mean(listaAnchuras))))
                ws.write(i, 4, float('%.2f' % (np.std(listaAlturas))))
                ws.write(i, 5, float('%.2f' % (np.std(listaAnchuras))))
            j = j + 1

        ws.write(i, 1, numEstomas)

        #else:
            #col = col +1

        i = i + 1
    wb.close()
    # wb.save('UsueEstomas.xlsx')