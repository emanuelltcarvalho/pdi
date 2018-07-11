# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 19:29:50 2017

@author: marcos
"""

from sklearn.cluster import KMeans
from sklearn.utils import shuffle

from classes.imagem import Imagem

import numpy as np

def mudaCor(img, metodo='average', nTons=256):
    nova = Imagem((img.altura, img.largura))
    for x in range(img.largura):
        for y in range(img.altura):
            r,g,b = img[y][x]
            if metodo == 'average':
                avg = (r + g + b) / 3.0
                nova[y][x] = (avg, avg, avg)
            elif metodo == 'r':
                nova[y][x] = (r,r,r)
            elif metodo == 'inv':
                nova[y][x] = (255-r, 255-g, 255-b)
            else:
                nova[y][x] = (r,g,b)

    return nova

def balanco(img, ar, ag, ab):
    nova = Imagem((img.altura, img.largura))

    for y in range(img.altura):
        for x in range(img.largura):
            r,g,b = img[y][x]
            R = int(ar*r)
            G = int(ar*g)
            B = int(ar*b)
            nova[y][x] = (R,G,B)

    return nova

def binaria(img):
    nova = img.copia()
    dados = img.arrLin()
    paleta = [[0,0,0], [255,255,255]]
    nClusters = 2
    amostraAleatoria = shuffle(dados, random_state=0)[:1000]
    km = KMeans(nClusters).fit(amostraAleatoria)
    labels = km.predict(dados)
    for x,label in enumerate(labels):
        i = x // img.largura
        j = x % img.largura
        r,g,b = paleta[label]
        nova[i][j] = (r,g,b)

    return nova

def propaga(tup, fator):
    r,g,b = tup
    return (r + fator, g + fator, b + fator)

# Floyd-Steinberg Dithering
def floyd(img):
    nova = mudaCor(img, 'average') # Mudar para luminosity, apos implementacao

    for y in range(img.altura):
        for x in range(img.largura):
            r,g,b = nova[y][x]
            if r >= 255//2:
                nova[y][x] = (255, 255, 255)
            else:
                nova[y][x] = (0, 0, 0)
            quantErro = r - nova[y][x][0]

            if x+1 < img.largura:
                nova[y][x+1] = propaga(nova[y][x+1], quantErro * 7/16)
            if y+1 < img.altura:
                if x-1 >= 0:
                    nova[y+1][x-1] = propaga(nova[y+1][x-1], quantErro * 3/16)
                nova[y+1][x] = propaga(nova[y+1][x], quantErro * 5/16)
                if x+1 < img.largura:
                    nova[y+1][x+1] = propaga(nova[y+1][x+1], quantErro * 1/16)

    return nova

# Ordered Dithering com matriz de Bayer
def bayer(img):
    matriz = np.array([[0,60], [45, 110]])
    dim = matriz.shape[0]

    nova = Imagem((img.altura, img.largura))

    for y in range(img.altura):
        for x in range(img.largura):
            r,g,b = img[y][x]
            Y = (r + g + b) / 3.0 # Mudar para luminancia (luminosity) apos implementado
            if Y > matriz[y % dim][x % dim]:
                nova[y][x] = (255, 255, 255)
            else:
                nova[y][x] = (0, 0, 0)

    return nova