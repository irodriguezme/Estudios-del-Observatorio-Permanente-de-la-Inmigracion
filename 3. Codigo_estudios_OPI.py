# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 20:51:28 2018

@author: irene
"""
# Se importan las librerias necesarias
import csv
import os
import requests
import csv
import re
from bs4 import BeautifulSoup

# Creamos el archivo csv con los cinco campos
csv_file = open('Opi_estudios_scrape.csv', 'w')

csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Numero','Titulo','Autor', 'Descripcion', 'Archivo_pdf'])

# Primeramente se realiza un bucle con las páginas que tienen una estructura 
# similar (desde el estudio número 10 al 31)

i=10
j=31

cadena='http://extranjeros.mitramiss.gob.es/es/ObservatorioPermanenteInmigracion/Publicaciones/fichas/publicacion_10.html'

while i<=j:
    
    source = requests.get(cadena).text
    soup = BeautifulSoup(source, 'lxml')
    texto = soup.find('div', class_='texto')
    # Selección del título
    titulo=texto.h2.text
    cuerpo= texto.find('div',class_='JustifyFull')
    autor = cuerpo.find('p').getText()
    autor=autor.split()
    autor=autor[1:]
    autor=' '.join(autor)
    descrip=cuerpo.find_all("p")
    descripcion=descrip[1:]
    parrafos = []
    for x in descripcion:
        parrafos.append(str(x))
    n=len(parrafos)
    for x in range(0,n):
        parrafos[x]=parrafos[x].replace('<p>',' ')
        parrafos[x]=parrafos[x].replace('</p>',' ')
    descripcion=' '.join(parrafos)
    print(descripcion)
    fichero= texto.find('ul')
    fichero=fichero.find('a')
    try:
        pdf=fichero.get('href')
        cad='http://extranjeros.mitramiss.gob.es/es/ObservatorioPermanenteInmigracion/Publicaciones/fichas/'
        pdf=cad + pdf
    except Exception as e:
        yt_link = None
    
    # Se elimina el teto que está entre <> y las comillasss
    descripcion=re.sub(r"\<[^]]*\>", "", descripcion)
    descripcion=descripcion.replace('"','')
    print(titulo)
    print(autor)
    print(descripcion)
    print(pdf)
    # Se sustituye el valor del número de estudio de la página Web
    m=i+1
    n=str(i)
    m=str(m)
    cadena=cadena.replace(n,m)
    i=i+1
    s=i-1
    print(cadena)
    print(i)
    csv_writer.writerow([s, titulo, autor, descripcion, pdf])
    
# A continuación se extrae la información necesaria del estudio 32 (última publicación
# cuya platilla es distinta a los números anteriores.

source = requests.get('http://extranjeros.mitramiss.gob.es/es/ObservatorioPermanenteInmigracion/Publicaciones/fichas/publicacion_32.html').text

soup = BeautifulSoup(source, 'lxml')


texto = soup.find('div',class_='texto')
print(texto)
titulo=texto.h2.text
cuerpo= texto.find('div',class_='JustifyFull')

cuerpo=cuerpo.text
cuerpo=cuerpo.splitlines(True)

cuerpo[0]=='\n'
autor=cuerpo[1]

autor=autor.split()

autor=autor[1:]
autor=' '.join(autor)
descripcion=cuerpo[2:]
n=len(descripcion)
for i in range(0,n):
    descripcion[i]=descripcion[i].replace('\n',' ')
descripcion=' '.join(descripcion)

print(titulo)
print(autor)
print(descripcion)

fichero= texto.find('ul')
fichero=fichero.find('a')
pdf=fichero.get('href')
cadena='http://extranjeros.mitramiss.gob.es/es/ObservatorioPermanenteInmigracion/Publicaciones/fichas/'
pdf=cadena + pdf

print(titulo)
print(autor)
print(descripcion)
print(pdf)    
s=32
csv_writer.writerow([s, titulo, autor, descripcion, pdf])

#Se cierra el fichero csv
csv_file.close()
