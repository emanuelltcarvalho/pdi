#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 13:54:42 2017

@author: marcos
"""

#==============================================================================
# Importa modulos relacionados a GUI
#==============================================================================
import tkinter.constants as cte
from tkinter import Tk
from tkinter import Frame, Menu
from tkinter import LabelFrame, Label, Button, Scrollbar, Toplevel, Scale
from tkinter import Canvas, Radiobutton
from tkinter import filedialog as tkf
from PIL import ImageTk
from tkinter import messagebox as tkm
from tkinter import StringVar

#==============================================================================
# Outros modulos
#==============================================================================
import os
from classes.imagem import Imagem
import modulos.cores as cor

class Gui(Frame):
#==============================================================================
#     Metodos Basicos
#==============================================================================
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        # Atributos GUI
        self.parent = parent
        self.file_opt = self.flopt = {}
        w,h = self.parent.winfo_screenwidth(), self.parent.winfo_screenheight()
        self.largura = w - 20
        self.altura = h - 20

        # Atributos funcionais
        self.img = None
        self.imgOld = None
        self.arqImg = StringVar()
        self.arqImg.set('')

        self.formatos = {}
        self.formatos['gif'] = 'GIF'
        self.formatos['jpg'] = 'JPEG'
        self.formatos['jpeg'] = 'JPEG'
        self.formatos['png'] = 'PNG'
        self.formatos['bmp'] = 'BMP'
        self.formatos['tif'] = 'TIFF'
        self.formatos['tiff'] = 'TIFF'
        self.formatos['ppm'] = 'PPM'
        self.formatos['pbm'] = 'PPM'
        self.formatos['pgm'] = 'PPM'

        self.tipos = [('Imagens', ('*.jpg', '*.png', '*.gif', '*.bmp', '*.ppm', '*.pgm', '*.pbm')),('JPEG', '*.jpg'), ('PNG', '*.png'), ('GIF', '*.gif'), ('BMP', '*.bmp'), ('PPM', '*.ppm'), ('PGM', '*.pgm'), ('PBM', '*.pbm'), ('Todos arquivos', '*')]

        # Cria/atualiza GUI
        self.createWidgets()
        self.update_idletasks()

#==============================================================================
#     Metodos relacionados ao comportamento da GUI
#==============================================================================

    def createWidgets(self):
        self.canvas = Canvas(self.parent, width=1366, height=768)
        self.scroll = Scrollbar(self.parent, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.scroll.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Configura barra de menus
        self.menubar = Menu(self.parent)
        self.parent.config(menu=self.menubar)

        # Menu arquivo e suas opcoes
        self.menuArquivo = Menu(self.menubar)
        self.menuArquivo.add_command(label='Abrir', underline=0, command=self.abrir)
        self.menuArquivo.add_separator()
        self.menuArquivo.add_command(label='Salvar', underline=0, command=self.salvar)
        self.menuArquivo.add_command(label='Salvar Como...', underline=0, command=self.salvarComo)
        self.menuArquivo.add_separator()
        self.menuArquivo.add_command(label='Fechar imagem(ns)', underline=0, command=self.fecharArquivo)
        self.menuArquivo.add_command(label="Sair", underline=3, command=self.onExit)
        self.menubar.add_cascade(label="Arquivo", underline=0, menu=self.menuArquivo)

        # Menu editar e suas opcoes
        self.menuEditar = Menu(self.menubar)
        self.menuEditar.add_command(label='Desfazer', underline=0, command=self.desfazer)
        self.menubar.add_cascade(label="Editar", underline=0, menu=self.menuEditar)

        # Menu Imagem e suas opcoes
        self.menuImagem = Menu(self.menubar)

        self.submenuConverte = Menu(self.menuImagem)
        self.submenuConverte.add_command(label='Colorido RGB', underline=0, command=lambda:self.converte('RGB'))
        self.submenuConverte.add_command(label='Colorido RGBA', underline=0, command=lambda:self.converte('RGBA'))
        self.submenuConverte.add_command(label='Escala de cinza', underline=0, command=lambda:self.converte('L'))
        self.submenuConverte.add_command(label='Binario', underline=0, command=lambda:self.converte('1'))

        self.menuImagem.add_command(label='Informacoes gerais', underline=0, command=self.info)
        self.menuImagem.add_separator()
        self.menuImagem.add_cascade(label='Converter', underline=0, menu=self.submenuConverte)
        self.menubar.add_cascade(label="Imagem", underline=0, menu=self.menuImagem)

        # Menu de operacoes sobre cores e suas opcoes
        self.menuCores = Menu(self.menubar)

        self.submenuCinza = Menu(self.menuCores)
        self.submenuCinza.add_command(label='Decomposicao de Maximo', underline=18, command=self.emConstrucao)
        self.submenuCinza.add_command(label='Decomposicao de Minimo', underline=18, command=self.emConstrucao)
        self.submenuCinza.add_command(label='Average', underline=0, command=lambda:self.mudaCor('average'))
        self.submenuCinza.add_command(label='Lightness', underline=0, command=self.emConstrucao)
        self.submenuCinza.add_command(label='Luminosity', underline=0, command=self.emConstrucao)
        self.submenuCinza.add_command(label='Componente R', underline=11, command=lambda:self.mudaCor('r'))
        self.submenuCinza.add_command(label='Componente G', underline=11, command=self.emConstrucao)
        self.submenuCinza.add_command(label='Componente B', underline=11, command=self.emConstrucao)
        self.submenuCinza.add_command(label='Quantidade arbitraria de tons', underline=0, command=self.emConstrucao)

        self.submenuHalftone = Menu(self.menuCores)
        self.submenuHalftone.add_command(label='Bayer 2x2', underline=6, command=lambda:self.halftoning('bayer2'))
        self.submenuHalftone.add_command(label='Bayer 5x5', underline=6, command=self.emConstrucao)
        self.submenuHalftone.add_command(label='Atkinson', underline=0, command=self.emConstrucao)
        self.submenuHalftone.add_command(label='Sierra Lite', underline=0, command=self.emConstrucao)
        self.submenuHalftone.add_command(label='Jarvis, Judice, and Ninke', underline=0, command=self.emConstrucao)
        self.submenuHalftone.add_command(label='Floyd-Steinberg', underline=0, command=lambda:self.halftoning('floyd'))

        self.menuCores.add_cascade(label='Tons de cinza', underline=0, menu=self.submenuCinza)
        self.menuCores.add_command(label='Inverter', underline=0, command=lambda:self.mudaCor('inv'))
        self.menuCores.add_command(label='Sepia', underline=0, command=self.emConstrucao)
        self.menuCores.add_separator()
        self.menuCores.add_command(label='Pseudo Binaria', underline=0, command=self.binaria)
        self.menuCores.add_cascade(label='Halftoning', underline=0, menu=self.submenuHalftone)
        self.menuCores.add_separator()
        self.menuCores.add_command(label='Cisalhamento de Cor', underline=0, command=self.emConstrucao)
        self.menuCores.add_command(label='Balanco de cores', underline=0, command=self.balancoCor)
        self.menuCores.add_command(label='Quantizacao de cores', underline=0, command=self.emConstrucao)
        self.menubar.add_cascade(label="Cores", underline=0, menu=self.menuCores)

        # Menu de operacoes topologicas e suas opcoes
        self.menuTopologia = Menu(self.menubar)
        self.menuTopologia.add_command(label='Rotular Componentes', underline=0, command=self.emConstrucao)
        self.menuTopologia.add_command(label='Transformada da Distancia', underline=0, command=self.emConstrucao)
        self.menuTopologia.add_command(label='Esqueletizacao', underline=0, command=self.emConstrucao)
        self.menubar.add_cascade(label="Topologia", underline=0, menu=self.menuTopologia)

        # Grupo principal, onde serao atualizados os widgets
        self.grupoPrincipal = Frame(self.canvas, width=self.largura, height=self.altura, bd=1, padx=10, pady=10)
        self.grupoPrincipal.pack()
        #self.grupoPrincipal.grid_propagate(False) # Faz com que o Frame nao seja redimensionado com a mudanca dos widgets
        self.canvas.create_window((4,20), window=self.grupoPrincipal, anchor="nw", tags="self.grupoPrincipal")
        self.grupoPrincipal.bind("<Configure>", self.OnFrameConfigure)

    def OnFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def onExit(self):
        self.parent.destroy()

    def limpaTela(self):
        for widget in self.grupoPrincipal.winfo_children():
            widget.destroy()

    def emConstrucao(self):
        tkm.showinfo(title="Em construcao", message="Recurso em Construcao...")

    def load_file(self, titulo, varFile, tipos):
        if os.path.isfile(varFile.get()):
            path = os.path.dirname(varFile.get())
            self.flopt['initialdir'] = path
        else:
            self.flopt['initialdir'] = os.path.curdir
        self.flopt['filetypes'] = tipos
        arquivo = tkf.askopenfilename(title=titulo, **self.flopt)
        if arquivo:
            varFile.set(arquivo)

    def widgetFile(self, master, titulo, texto, varFile, tuplaFiletype):
        esteFrame = LabelFrame(master, text=titulo, padx=5, pady=5)

        j = 0
        varFile.set("Nenhum arquivo informado")
        labelRotulo = Label(esteFrame, text=texto)
        labelRotulo.grid(row=j,column=0,sticky=cte.E)

        botao = Button(esteFrame, text="Procurar", command=lambda:self.load_file(texto, varFile, tuplaFiletype), width=10)
        botao.grid(row=j, column=1, pady=5,sticky=cte.W)

        j += 1

        labelArq = Label(esteFrame, textvariable=varFile, bg='white')
        labelArq.grid(row=j, column=0, columnspan=2)

        return esteFrame

    def refreshImg(self):
        try:
            self.grupoPrincipal.photo = ImageTk.PhotoImage(self.img.img)
            if hasattr(self.grupoPrincipal, 'canvas'):
                self.grupoPrincipal.canvas.destroy()
            self.grupoPrincipal.canvas = Canvas(self.grupoPrincipal)
            self.grupoPrincipal.canvas.create_image(0,0,image=self.grupoPrincipal.photo, anchor=cte.NW)
            self.grupoPrincipal.canvas.config(bg='white', width=self.img.altura, height=self.img.largura)
            #self.grupoPrincipal.canvas.place(x=self.parent.winfo_screenwidth()/2, y=self.parent.winfo_screenheight()/2, anchor=cte.CENTER)
            self.grupoPrincipal.canvas.place(x=0, y=0, anchor=cte.NW)
            self.grupoPrincipal.update_idletasks()
        except Exception as e:
            tkm.showerror('Erro', 'O seguinte erro ocorreu: %s' % str(e.args))

#==============================================================================
#   Metodos relacionados ao meno Arquivo
#==============================================================================

    def abrir(self):
        try:
            self.limpaTela()
            self.load_file('Arquivos de Imagem', self.arqImg, self.tipos)
            self.img = Imagem(self.arqImg.get())
            self.refreshImg()
        except Exception as e:
            tkm.showerror('Erro', 'O seguinte erro ocorreu: %s' % str(e.args))

    def saveFile(self):
        try:
            nome,extensao = os.path.splitext(self.arqImg.get())
            extensao = extensao.replace('.','')
            self.img.salva(self.arqImg.get(), self.formatos[extensao.lower()])
            tkm.showinfo('Sucesso', 'Arquivo %s salvo com sucesso' % os.path.basename(self.arqImg.get()))
        except Exception as e:
            tkm.showerror('Erro', 'O seguinte erro ocorreu: %s' % str(e.args))

    def salvar(self):
        if self.arqImg.get() == '':
            tkm.showwarning('Aviso', 'Nao ha arquivo aberto para ser salvo')
        else:
            try:
                self.saveFile()
            except Exception as e:
                tkm.showerror('Erro', 'O seguinte erro ocorreu: %s' % str(e.args))

    def salvarComo(self):
        if self.arqImg.get() == '':
            tkm.showwarning('Aviso', 'Nao ha arquivo aberto para ser salvo')
        else:
            try:
                if os.path.isfile(self.arqImg.get()):
                    path = os.path.dirname(self.arqImg.get())
                    self.flopt['initialdir'] = path
                else:
                    self.flopt['initialdir'] = os.path.curdir
                self.flopt['filetypes'] = self.tipos
                nomeArq = tkf.asksaveasfilename(title='Salvar imagem como...', **self.flopt)
                if nomeArq:
                    self.arqImg.set(nomeArq)
                    self.saveFile()
            except Exception as e:
                tkm.showerror('Erro', 'O seguinte erro ocorreu: %s' % str(e.args))

    def fecharArquivo(self):
        if not hasattr(self.grupoPrincipal, 'canvas') or self.grupoPrincipal.canvas.find_all() == ():
            tkm.showwarning('Aviso', 'Nao ha imagens abertas')
        else:
            try:
                self.img = self.imgOld = None
                self.grupoPrincipal.canvas.delete('all')
                self.grupoPrincipal.update_idletasks()
            except Exception as e:
                tkm.showerror('Erro', 'O seguinte erro ocorreu: %s' % str(e.args))

#==============================================================================
#  Metodos relacionados ao menu Editar
#==============================================================================

    def desfazer(self):
        if self.arqImg.get() == '' or self.img is None:
            tkm.showwarning('Aviso', 'Nao ha arquivo aberto')
        elif self.imgOld is None:
            tkm.showwarning('Aviso', 'Impossivel Desfazer')
        else:
            try:
                temp = self.img
                self.img = self.imgOld
                self.imgOld = temp
                self.refreshImg()
            except Exception as e:
                tkm.showerror('Erro', 'O seguinte erro ocorreu: %s' % str(e.args))

#==============================================================================
#   Metodos relacionados ao menu Cores
#==============================================================================
    def mudaCor(self, metodo):
        if self.arqImg.get() == '' or self.img is None:
            tkm.showwarning('Aviso', 'Nao ha arquivo aberto')
        else:
            try:
                self.imgOld = self.img
                self.img = cor.mudaCor(self.imgOld, metodo)
                self.refreshImg()
            except Exception as e:
                tkm.showerror('Erro', 'O seguinte erro ocorreu: %s' % str(e.args))

    def binaria(self):
        if self.arqImg.get() == '' or self.img is None:
            tkm.showwarning('Aviso', 'Nao ha arquivo aberto')
        else:
            try:
                self.imgOld = self.img
                self.img = cor.binaria(self.imgOld)
                self.refreshImg()
            except Exception as e:
                tkm.showerror('Erro', 'O seguinte erro ocorreu: %s' % str(e.args))

    def getFatoresBalanco(self):
        self.fatores = [float(self.escalaFatorR.get())]
        self.fatores.append(float(self.escalaFatorG.get()))
        self.fatores.append(float(self.escalaFatorB.get()))

        self.w.destroy()

    def formBalanco(self):
        self.fator = None
        self.fatores = None

        self.w = Toplevel(self)
        self.w.wm_title("Informar os fatores de ajuste")

        self.w.geometry("+%d+%d" % (self.winfo_rootx()+50, self.winfo_rooty()+50))
        self.w.focus_set()

        i = 0

        self.labelFatorR = Label(self.w, text='Ajuste em R', width=25)
        self.labelFatorR.grid(row=i, column=0)
        self.escalaFatorR = Scale(self.w, from_=0, to=2, resolution=0.05, length=350, orient=cte.HORIZONTAL)
        self.escalaFatorR.set(0.5)
        self.escalaFatorR.grid(row=i, column=1)
        i+=1

        self.labelFatorG = Label(self.w, text='Ajuste em G', width=25)
        self.labelFatorG.grid(row=i, column=0)
        self.escalaFatorG = Scale(self.w, from_=0, to=2, resolution=0.05, length=350, orient=cte.HORIZONTAL)
        self.escalaFatorG.set(0.5)
        self.escalaFatorG.grid(row=i, column=1)
        i+=1

        self.labelFatorB = Label(self.w, text='Ajuste em B', width=25)
        self.labelFatorB.grid(row=i, column=0)
        self.escalaFatorB = Scale(self.w, from_=0, to=2, resolution=0.05, length=350, orient=cte.HORIZONTAL)
        self.escalaFatorB.set(0.5)
        self.escalaFatorB.grid(row=i, column=1)
        i+=1

        self.botaoFator = Button(self.w, text='Ok', command=self.getFatoresBalanco, width=10)
        self.botaoFator.grid(row=i, column=0, columnspan=2)

        self.w.grid()

    def balancoCor(self):
        if self.arqImg.get() == '' or self.img is None:
            tkm.showwarning('Aviso', 'Nao ha arquivo aberto')
        else:
            try:
                self.formBalanco()
                self.wait_window(self.w)
                if self.fatores is not None:
                    self.imgOld = self.img
                    self.img = cor.balanco(self.imgOld, self.fatores[0], self.fatores[1], self.fatores[2])
                    self.refreshImg()
            except Exception as e:
                tkm.showerror('Erro', 'O seguinte erro ocorreu: %s' % str(e.args))

    def halftoning(self, metodo='bayer2'):
        if self.arqImg.get() == '' or self.img is None:
            tkm.showwarning('Aviso', 'Nao ha arquivo aberto')
        else:
            try:
                self.imgOld = self.img
                if metodo == 'bayer2':
                    self.img = cor.bayer(self.imgOld)
                elif metodo == 'floyd':
                    self.img = cor.floyd(self.imgOld)
                else:
                    raise Exception('Metodo de halftoning desconhecido')
                self.refreshImg()
            except Exception as e:
                tkm.showerror('Erro', 'O seguinte erro ocorreu: %s' % str(e.args))

#==============================================================================
#   Metodos relacionados ao menu Imagem
#==============================================================================
    def converte(self, modo='RGB'):
        if self.arqImg.get() == '' or self.img is None:
            tkm.showwarning('Aviso', 'Nao ha arquivo aberto')
        else:
            try:
                self.imgOld = self.img.copia()
                self.img.converte(modo)
                self.refreshImg()
            except Exception as e:
                tkm.showerror('Erro', 'O seguinte erro ocorreu: %s' % str(e.args))

    def info(self):
        if self.arqImg.get() == '':
            tkm.showwarning('Aviso', 'Nao ha arquivo aberto')
        else:
            try:
                texto = 'Imagem %s, modo: %s (%d x %d pixels)' % (self.img.img.format, self.img.img.mode, self.img.img.size[0], self.img.img.size[1])
                tkm.showinfo('Aviso', texto)
            except Exception as e:
                tkm.showerror('Erro', 'O seguinte erro ocorreu: %s' % str(e.args))

# Cria janela principal
top = Tk()
top.title("PhotoPobre Beta v1.0")
# Maximiza
w,h = top.winfo_screenwidth(), top.winfo_screenheight()
top.geometry("%dx%d+0+0" % (w,h))

# Executa em loop ate janela ser fechada
mainw = Gui(parent=top)
mainw.mainloop()
