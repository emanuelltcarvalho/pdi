# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 17:54:51 2016

@author: marcos
"""

from PIL import Image
import numpy as np

#==============================================================================
# Classe Imagem: encapsula objeto Image, do modulo PIL
#   pode ser instanciada com um nome de arquivo ja existente ou com uma tupla
#       contendo 2 inteiros correspondendo as dimensoes (altura x largura) da imagem a ser criada
#==============================================================================

class Imagem(object):

#==============================================================================
#   Construtor e metodos internos essenciais
#==============================================================================
    def __init__(self, entrada):
        self.initVars()

        try:
            if type(entrada) is str:
                self.img = Image.open(entrada)
                self.altura, self.largura = self.img.size
            elif type(entrada) is tuple:
                self.img = Image.new('RGB', entrada)
                self.altura = int(entrada[0])
                self.largura = int(entrada[1])
            else:
                raise Exception('Voce deve especificar um arquivo ou um tamanho para a imagem.')
        except Exception as e:
            raise Exception(e.args)

    # Inicializacao de flags
    def initVars(self):
        self._y = 0
        self._getSet = False

#==============================================================================
# Metodos essenciais de uso externo
#==============================================================================

    # Salvamento de imagem em disco
    def salva(self, arquivo, formato='png'):
        try:
            self.img.save(arquivo, formato)
            self.img = Image.open(arquivo)
        except Exception as e:
            raise Exception(e.args)

    # Converte imagem para outro modo
    def converte(self, modo='RGB'):
        try:
            self.img = self.img.convert(modo)
        except Exception as e:
            raise Exception(e.args)

    # Exibe imagem em tela
    def exibe(self):
        try:
            self.img.show()
        except Exception as e:
            raise Exception(e.args)

    # Copia imagem
    def copia(self):
        try:
            img2 = Imagem((self.altura, self.largura))
            img2.img = self.img.copy()
            return img2
        except Exception as e:
            raise Exception(e.args)

    # Obtem array de dados apenas com numeros inteiros
    def arr(self):
        try:
            dados = np.empty((self.altura, self.largura, 3), dtype=int)
            for i in range(self.altura):
                for j in range(self.largura):
                    r,g,b = self.img.getpixel((i, j))
                    dados[i][j] = np.array([r,g,b])
            return dados
        except Exception as e:
            raise Exception(e.args)

    # Obtem array de dados linear (numeros inteiros apenas) com a lista de pixels
    def arrLin(self):
        try:
            dados = np.empty((self.altura * self.largura, 3), dtype=int)
            k = 0
            for i in range(self.altura):
                for j in range(self.largura):
                    r,g,b = self.img.getpixel((i, j))
                    dados[k] = np.array([r,g,b])
                    k += 1
            return dados
        except Exception as e:
            raise Exception(e.args)
            
    # Obtem array de dados linear (numeros inteiros apenas) com as coordenada agregadas
    def arrLinGeo(self):
        try:
            dados = np.empty((self.altura * self.largura, 3), dtype=int)
            k = 0
            for i in range(self.altura):
                for j in range(self.largura):
                    r,g,b = self.img.getpixel((i, j))
                    if r != g or r != b or g != b:
                        Y = int(0.299*r + 0.587*g + 0.114*b)
                    else:
                        Y = r
                    dados[k] = np.array([i,j,Y])
                    k += 1
            return dados
        except Exception as e:
            raise Exception(e.args)

#==============================================================================
#   Metodos para manipulacao da matriz
#==============================================================================

    # Obtencao de pixel da imagem (aceita notacao [i][j] ou [i,j])
    def __getitem__(self, indices):
        if type(indices) is tuple:
            i, j = indices
            if type(i) is not int or type(j) is not int:
                raise Exception('Os indices devem ser inteiros ou uma tupla de inteiros')
            return self.img.getpixel((i, j))
        elif type(indices) is int:
            if not self._getSet:
                self._getSet = True
                self._y = indices
                return self
            else:
                i = self._y
                self.initVars()
                return self.img.getpixel((i, indices))
        else:
            raise Exception('Os indices devem ser inteiros ou uma tupla de inteiros')

    # Altera ou define pixel da imagem (aceita notacao [i][j] ou [i,j]). Aceita passagem de uma tupla de inteiros rgb
    def __setitem__(self, indices, px):
        if type(px) is tuple:
            if len(px) != 3:
                raise Exception('A tupla deve ter dimensao 3')

            try:
                pix = tuple([min(255, max(int(x),0)) for x in px])
            except:
                raise Exception('Os elementos da tupla devem ser todos inteiros ou float. Problema em (%s,%s,%s)' % px)
        else:
            raise Exception('Os valores RGB devem ser passados em uma tupla')

        if type(indices) is tuple:
            i, j = indices
            if type(i) is not int or type(j) is not int:
                raise Exception('Os indices devem ser inteiros ou uma tupla de inteiros.')

            try:
                self.img.putpixel((i, j), pix)
            except Exception as e:
                raise Exception(e.args)

        elif type(indices) is int:
            if not self._getSet:
                self._getSet = True
                self._y = indices
                return self
            else:
                i = self._y
                self.initVars()
                try:
                    self.img.putpixel((i, indices), pix)
                except Exception as e:
                    raise Exception(e.args)
        else:
            raise Exception('Os indices devem ser inteiros ou uma tupla de inteiros.')

#==============================================================================
#   Metodos para operacoes com imagens e valores numericos
#==============================================================================

    # Soma: Imagem = Imagem + Imagem
    # Se: Imagem = Imagem + valor, chama o metodo addNum
    def __add__(self, outra):
        if not isinstance(outra, Imagem) and type(outra) is not int and type(outra) is not float:
            raise Exception('Uma imagem soh pode ser somada a outra imagem ou a um numero.')

        if type(outra) is float or type(outra) is int:
            # se outra for numerico, chama o metodo addNum
            return self.addNum(outra)
        elif self.altura != outra.altura or self.largura != outra.largura:
            raise Exception('Ambas imagens devem ter as mesmas dimensoes para serem somadas.')

        try:
            nova = Imagem((self.altura, self.largura))
            nova.img = self.img.copy()

            for i in range(self.altura):
                for j in range(self.largura):
                    nova[i][j] = tuple([min(255, max(0,i)) for i in np.array(self.img.getpixel((i, j))) + np.array(outra.img.getpixel((i, j)))])

            return nova
        except Exception as e:
            raise Exception(e.args)

    # Soma: Imagem = Imagem + numero
    def addNum(self, valor):
        try:
            nova = Imagem((self.altura, self.largura))
            nova.img = self.img.copy()

            for i in range(self.altura):
                for j in range(self.largura):
                    nova[i][j] = tuple([min(255, max(0,i)) for i in np.array(self.img.getpixel((i, j))) + valor])

            return nova
        except Exception as e:
            raise Exception(e.args)

    # Subtracao: Imagem = Imagem - Imagem
    # Se: Imagem = Imagem - valor, chama o metodo subNum
    def __sub__(self, outra):
        if not isinstance(outra, Imagem) and type(outra) is not int and type(outra) is not float:
            raise Exception('Uma imagem soh pode ser somada a outra imagem ou a um numero.')

        if type(outra) is float or type(outra) is int:
            # se outra for numerico, chama o metodo subNum
            return self.subNum(outra)
        elif self.altura != outra.altura or self.largura != outra.largura:
            raise Exception('Ambas imagens devem ter as mesmas dimensoes para serem somadas.')

        try:
            nova = Imagem((self.altura, self.largura))
            nova.img = self.img.copy()

            for i in range(self.altura):
                for j in range(self.largura):
                    nova[i][j] = tuple([min(255, max(0,i)) for i in np.array(self.img.getpixel((i, j))) - np.array(outra.img.getpixel((i, j)))])

            return nova
        except Exception as e:
            raise Exception(e.args)

    # Subtracao: Imagem = Imagem - numero
    def subNum(self, valor):
        try:
            nova = Imagem((self.altura, self.largura))
            nova.img = self.img.copy()

            for i in range(self.altura):
                for j in range(self.largura):
                    nova[i][j] = tuple([min(255, max(0,i)) for i in np.array(self.img.getpixel((i, j))) - valor])

            return nova
        except Exception as e:
            raise Exception(e.args)

    # Multiplicacao: Imagem = Imagem * numero
    def __mul__(self, valor):
        if type(valor) is not float and type(valor) is not int:
            raise Exception('A imagem deve ser multiplicada por um valor numerico')

        try:
            nova = Imagem((self.altura, self.largura))
            nova.img = self.img.copy()
            for i in range(self.altura):
                for j in range(self.largura):
                    nova[i][j] = tuple([min(255, max(0,i)) for i in np.array(self.img.getpixel((i, j))) * valor])

            return nova
        except Exception as e:
            raise Exception(e.args)

    # Divisao: Imagem = Imagem / numero
    def __truediv__(self, valor):
        if type(valor) is not float and type(valor) is not int:
            raise Exception('A imagem deve ser multiplicada por um valor numerico')

        try:
            nova = Imagem((self.altura, self.largura))
            nova.img = self.img.copy()
            for i in range(self.altura):
                for j in range(self.largura):
                    nova[i][j] = tuple([min(255, max(0,i)) for i in np.array(self.img.getpixel((i, j))) - valor])

            return nova
        except Exception as e:
            raise Exception(e.args)

#==============================================================================
#   Convolucao generica
#==============================================================================
    # Convolucao por gabarito truncado retorna um array de valores, nao uma imagem
    #  o resultado de uma convolucao pode ser combinado com o de outra (vide Sobel)
    #  sendo assim, os valores devem ser limitados no intervalo [0,255] somente ao termino
    #  da aplicacao dos operadores de convolucao. Para tal, utilizar o metodo getFromArray
    def convolucao(self, mascara):
        altMasc = mascara.shape[0]
        largMasc = mascara.shape[1]

        if altMasc != largMasc:
            raise Exception('A altura e a largura da mascara de convolucao devem ter a mesma dimensao')

        try:
            novosDados = np.empty((self.altura, self.largura, 3))

            if altMasc % 2 != 0: # Mascara de organizacao impar (resultado no centro)
                raio = altMasc // 2
                for y in range(self.altura):
                    for x in range(self.largura):
                        novosDados[y][x] = np.asarray([0,0,0])
                        a = 0
                        for i in range(max(0,y-raio), min(self.altura,y+raio+1)):
                            b = 0
                            for j in range(max(0,x-raio), min(self.largura,x+raio+1)):
                                novosDados[y][x] += np.array(self.img.getpixel((i, j))) * mascara[a][b]
                                b += 1
                            a += 1
            else: # Mascara de organizacao par (resultado no primeiro pixel)
                for y in range(self.altura):
                    for x in range(self.largura):
                        novosDados[y][x] = np.asarray([0,0,0])
                        a = 0
                        for i in range(y, min(self.altura,y+altMasc)):
                            b = 0
                            for j in range(x, min(self.largura, x+altMasc)):
                                novosDados[y][x] += np.array(self.img.getpixel((i, j))) * mascara[a][b]
                                b += 1
                            a += 1

            return novosDados
        except Exception as e:
            raise Exception(e.args)

    def getFromArray(self, arr):
        try:
            nova = Imagem((arr.shape[0], arr.shape[1]))
            for y in range(nova.altura):
                for x in range(nova.largura):
                    nova[y][x] = (arr[y][x][0], arr[y][x][1], arr[y][x][2])

            return nova
        except Exception as e:
            raise Exception(e.args)


#==============================================================================
#   Metodos estatisticos
#==============================================================================
    # Retorna o pixel (e posicao do mesmo) mais proximo do branco
    def maximo(self):
        branco = np.array([255, 255, 255])

        minDist = np.linalg.norm(branco)
        minPx = np.copy(branco)
        iMin = 0
        jMin = 0
        try:
            for i in range(self.altura):
                for j in range(self.largura):
                    d = np.linalg.norm(np.array(self.img.getpixel((i, j))) - branco)
                    if d <= minDist:
                        minDist = d
                        minPx = np.copy(np.array(self.img.getpixel((i, j))))
                        iMin = i
                        jMin = j
            return minPx, iMin, jMin
        except Exception as e:
            raise Exception(e.args)

    # Retorna o pixel (e posicao do mesmo) mais proximo do preto
    def minimo(self):
        preto = np.array([0, 0, 0])

        minDist = np.linalg.norm(preto)
        minPx = np.copy(preto)
        iMin = 0
        jMin = 0
        try:
            for i in range(self.altura):
                for j in range(self.largura):
                    d = np.linalg.norm(np.array(self.img.getpixel((i, j))) - preto)
                    if d <= minDist:
                        minDist = d
                        minPx = np.copy(np.array(self.img.getpixel((i, j))))
                        iMin = i
                        jMin = j
            return minPx, iMin, jMin
        except Exception as e:
            raise Exception(e.args)

    # Retorna os histogramas RGB da imagem
    def histogramas(self):
        hr = np.zeros(256, dtype=int)
        hg = np.zeros(256, dtype=int)
        hb = np.zeros(256, dtype=int)

        try:
            for i in range(self.altura):
                for j in range(self.largura):
                    r,g,b = self.img.getpixel((i, j))
                    hr[r] += 1
                    hg[g] += 1
                    hb[b] += 1
            return hr, hg, hb
        except Exception as e:
            raise Exception(e.args)

    # Retorna o histograma da versao cinza da imagem
    def histograma(self):
        h = np.zeros(256, dtype=int)

        try:
            for i in range(self.altura):
                for j in range(self.largura):
                    r,g,b = self.img.getpixel((i, j))
                    Y = int(0.299*r + 0.587*g + 0.114*b)
                    h[Y] += 1
            return h
        except Exception as e:
            raise Exception(e.args)
