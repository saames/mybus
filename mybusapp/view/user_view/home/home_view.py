import tkinter as tk
import ttkbootstrap as ttk
from resources.photos import Base64
from resources.utils import Utils
from view.user_view.linha.visualizar_linha import VisualizarLinhaView
from view.adm_view.gerenciar_linhas.gerenciar_linhas_view import GerenciarLinhasView
from view.adm_view.gerenciar_onibus.gerenciar_onibus_view import GerenciarOnibusView
from view.adm_view.gerenciar_usuarios.gerenciar_usuarios_view import GerenciarUsuariosView

class HomeLinhaView:
    def __init__(self,master, janela_origem=None, papel="usuario", id = None):
        # Ajustes janela
        self.janela_origem = janela_origem
        self.janela = master
        self.janela.geometry('400x450')
        self.janela.title('Home - MyBus')
        self.janela.resizable(False,False)
        self.frm_center = ttk.Frame(self.janela)
        self.frm_center.pack(padx=20, pady=20)

        self.user_id = id

        #Criando Instancias
        self.utils = Utils()

        # Logo MyBus
        self.img_logo = ttk.PhotoImage(data=Base64.myBusLogo128())
        self.lbl_logo = ttk.Label(self.frm_center, image=self.img_logo)
        self.lbl_logo.image = self.img_logo
        self.lbl_logo.grid(row=0, column=0, pady=20)

        # Botão Visualizar linhas
        self.btn_visualizar = ttk.Button(self.frm_center,text="VISUALIZAR LINHAS")
        self.btn_visualizar.grid(row=2, column=0, sticky='ew', pady=(0,10))
        self.btn_visualizar.bind('<ButtonRelease-1>', self.visualizar_Linha)

        if (papel == "adm" or papel == 'super'):
            # Botão Gerenciar linhas
            self.btn_gerenciar_linha = ttk.Button(self.frm_center,text="GERENCIAR LINHAS", bootstyle='secondary')
            self.btn_gerenciar_linha.grid(row=3, column=0, sticky='ew', pady=(0,10))
            self.btn_gerenciar_linha.bind('<ButtonRelease-1>', self.gerenciar_linha)

            # Botão Gerenciar Onibus
            self.btn_grerenciar_onibus = ttk.Button(self.frm_center,text="GERENCIAR ÔNIBUS", bootstyle='secondary')
            self.btn_grerenciar_onibus.grid(row=4, column=0, sticky='ew', pady=(0,10))
            self.btn_grerenciar_onibus.bind('<ButtonRelease-1>', self.gereciar_onibus)

            # Botão Gerenciar Usuario
            self.btn_gerenciar_usuario = ttk.Button(self.frm_center,text="GERENCIAR USUÁRIO", bootstyle='secondary')
            self.btn_gerenciar_usuario.grid(row=5, column=0, sticky='ew', pady=(0,10))
            self.btn_gerenciar_usuario.bind('<ButtonRelease-1>', self.gereciar_usuarios)

        # Botão SAIR
        self.btn_sair = ttk.Button(self.frm_center, text="SAIR", bootstyle='danger')
        self.btn_sair.grid(row=6, column=0, sticky='ew', pady=(0,10))
        self.btn_sair.bind('<ButtonRelease-1>', self.sair)

        # Comandos de navegação
        self.janela.bind('<Escape>', self.sair)

        self.utils.centraliza(self.janela)

    def visualizar_Linha(self, event):
        self.janela.withdraw() 
        self.tl = ttk.Toplevel(self.janela)
        VisualizarLinhaView(self.tl,self.janela,self.user_id)
        self.utils.call_top_view(self.janela, self.tl)

    def gerenciar_linha(self, event):
        self.janela.withdraw() 
        self.tl = ttk.Toplevel(self.janela)
        GerenciarLinhasView(self.tl, self.janela) 
        self.utils.call_top_view(self.janela, self.tl)

    def gereciar_onibus(self, event):
        self.janela.withdraw() 
        self.tl = ttk.Toplevel(self.janela)
        GerenciarOnibusView(self.tl, self.janela)
        self.utils.call_top_view(self.janela, self.tl)

    def gereciar_usuarios(self, event):
        self.janela.withdraw() 
        self.tl = ttk.Toplevel(self.janela)
        GerenciarUsuariosView(self.tl, self.janela, self.user_id)
        self.utils.call_top_view(self.janela, self.tl)

    def sair(self, event):
        self.janela.destroy()