import tkinter as tk
import ttkbootstrap as ttk
from resources.photos import Base64
from resources.utils import Utils


class HomeLinhaView:
    def __init__(self,master,janela_origem=None):
        # Ajustes janela
        self.janela_origem = janela_origem
        self.janela = master
        self.janela.geometry('700x550')
        self.janela.title('Home Linha')
        self.janela.resizable(False,False)


        # Configura as colunas para expandir igualmente
        self.janela.grid_columnconfigure(0, weight=1)
        self.janela.grid_columnconfigure(1, weight=1)

        # Logo MyBus no canto superior esquerdo
        self.img_logo = ttk.PhotoImage(data=Base64.myBusLogo128())
        self.lbl_logo = ttk.Label(self.janela, image=self.img_logo)
        self.lbl_logo.image = self.img_logo
        self.lbl_logo.grid(row=0, column=0, padx=10, pady=10, sticky='nw')

        # Botão SAIR no canto superior direito
        self.btn_sair = ttk.Button(self.janela, text="SAIR", bootstyle='danger')
        self.btn_sair.grid(row=0, column=1, padx=30, pady=60, sticky='ne')
        self.btn_sair.bind('<ButtonRelease-1>', self.sair)

        # Frame para centralizar os componentes no meio da janela
        self.frm_center = ttk.Frame(self.janela)
        self.frm_center.grid(row=1,column=0, columnspan=2, padx=10, pady=(60,10), sticky='nsew')
        self.janela.grid_rowconfigure(1, weight=1)
        self.frm_center.columnconfigure(0, weight=1)

        

        # Botão Visualizar linhas 
        self.btn_visualizar = ttk.Button(self.frm_center,text="VISUALIZAR LINHAS",bootstyle='primary',width=20)
        self.btn_visualizar.grid(row=0, column=0, padx=10, pady=10, sticky='n')
        self.btn_visualizar.bind('<ButtonRelease-1>', self.sair)
        # Botão Gerenciar linhas 
        self.btn_gerenciar_linha = ttk.Button(self.frm_center,text="GERENCIAR LINHAS",bootstyle='primary',width=20)
        self.btn_gerenciar_linha.grid(row=1, column=0, padx=10, pady=10, sticky='n')
        self.btn_gerenciar_linha.bind('<ButtonRelease-1>', self.sair)

        # Botão Gerenciar Onibus
        self.btn_grerenciar_onibus = ttk.Button(self.frm_center,text="GERENCIAR ONIBUS",bootstyle='primary',width=20)
        self.btn_grerenciar_onibus.grid(row=2, column=0, padx=10, pady=10, sticky='n')
        self.btn_grerenciar_onibus.bind('<ButtonRelease-1>', self.sair)

        # Botão Gerenciar Usuario 
        self.btn_gerenciar_usuario = ttk.Button(self.frm_center,text="GERENCIAR USUARIO",bootstyle='primary',width=20)
        self.btn_gerenciar_usuario.grid(row=3, column=0, padx=10, pady=10, sticky='n')
        self.btn_gerenciar_usuario.bind('<ButtonRelease-1>', self.sair)


    
    def sair(self, event):
        self.janela.destroy()