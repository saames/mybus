from tkinter import mainloop, messagebox

import ttkbootstrap as ttk
from control.login_control import LoginControl
from resources.utils import Utils
from resources.photos import Base64
from view.user_view.home.home_view import HomeLinhaView
from view.user_view.cadastro.cadastro_user import (CadastroUserView)
from control.login_control import LoginControl
from view.user_view.redefinir_senha.solicitar_redefinir_senha_view import SolicitarRedefinirSenhaView

class LoginView:
    def __init__(self, master):
        self.janela = master
        self.janela.title('Login - MyBus')
        self.janela.geometry('440x430')
        self.janela.resizable(False, False)
        self.frm_center = ttk.Frame(self.janela)
        self.frm_center.pack()

        # Criação de Instâncias
        self.login_control = LoginControl()
        self.utils = Utils()

        # Logo MyBus
        self.img_logo = ttk.PhotoImage(data=Base64.myBusLogo128())
        self.lbl_logo = ttk.Label(self.frm_center, image=self.img_logo)
        self.lbl_logo.image = self.img_logo
        self.lbl_logo.grid(column=0, row=0, columnspan=2, pady=20)

        # Nome de Usuário (CPF)
        self.lbl_username = ttk.Label(self.frm_center, text='CPF', bootstyle='inverse-secondary', 
                                                                   borderwidth=7, 
                                                                   padding=(13,0),
                                                                   font=('TkDefaultFont', 10, 'bold'))
        self.lbl_username.grid(column=0, row=2)
        self.ent_username_value = ttk.StringVar()
        self.ent_username = ttk.Entry(self.frm_center, textvariable=self.ent_username_value)
        self.ent_username.grid(column=1, row=2)
        self.ent_username.bind('<KeyRelease>', self.validar_campos)
        self.utils.add_placeholder(self.ent_username,'XXX.XXX.XXX-XX')

        # Senha
        self.lbl_password = ttk.Label(self.frm_center, text='SENHA', bootstyle='inverse-secondary', 
                                                                     borderwidth=7, 
                                                                     padding=(2,0),
                                                                     font=('TkDefaultFont', 10, 'bold'))
        self.lbl_password.grid(column=0, row=3)
        self.ent_password_value = ttk.StringVar()
        self.ent_password = ttk.Entry(self.frm_center, show='*', textvariable=self.ent_password_value)
        self.ent_password.grid(column=1, row=3, pady=5)
        self.ent_password.bind('<KeyRelease>', self.validar_campos)

        # Botão Logar
        self.btn_acessar = ttk.Button(self.frm_center, text='ACESSAR', state='disabled')
        self.btn_acessar.grid(column=0, row=4, columnspan=2, sticky='we', pady=5)
        self.btn_acessar.bind('<ButtonRelease-1>', self.pedir_autenticacao)

        # Botão Redefinir senha
        self.btn_redefinir = ttk.Button(self.frm_center, text='Esqueci minha senha', bootstyle='secondary-link')
        self.btn_redefinir.grid(column=0, row=5, columnspan=2, pady=(10,5))
        self.btn_redefinir.bind('<ButtonRelease-1>', self.abrir_redefinir_senha)

        # Linha Divisória
        self.spr_separator = ttk.Separator(self.frm_center, orient='horizontal')
        self.spr_separator.grid(column=0, row=6, columnspan=2, sticky='ew', pady=10)

        # Botão Cadastrar
        self.frm_cadastrar = ttk.Frame(self.frm_center)
        self.frm_cadastrar.grid(column=0, row=7, columnspan=2)

        self.lbl_cadastrar = ttk.Label(self.frm_cadastrar, text='Não possui\numa conta?')
        self.lbl_cadastrar.grid(column=0, row=0)

        self.btn_cadastrar = ttk.Button(self.frm_cadastrar, text='Cadastrar-se')
        self.btn_cadastrar.grid(column=1, row=0, padx=(15,0))
        self.btn_cadastrar.bind('<ButtonRelease-1>', self.abrir_cadastro_usuario)

        # Comandos de navegação
        self.janela.bind('<Return>', self.pedir_autenticacao)
        self.janela.bind('<Escape>', self.fechar_janela)

        self.janela.bind_class('TButton', '<Enter>', self.utils.on_enter)
        self.janela.bind_class('TButton', '<Leave>', self.utils.on_leave)

        self.utils.centraliza(self.janela)

    # Restrições básicas para autenticação
    def validar_campos(self, *event):
        cpf = self.ent_username.get().replace(".","").replace("-","")
        senha = self.ent_password.get()
        if len(cpf)==11 and len(senha) >= 8 and cpf != "XXX.XXX.XXX-XX": # CPF tem tamanho 11 e senha maior ou igual 8.
            self.btn_acessar.config(state='enable')
            return True
        else:
            self.btn_acessar.config(state='disabled')
            return False

    def abrir_redefinir_senha(self, event):
        self.reiniciar_tela()
        self.tl = ttk.Toplevel(self.janela)
        SolicitarRedefinirSenhaView(self.tl)
        self.utils.call_top_view(self.janela, self.tl)

    # Abre a janela CadastroUsuarioView
    def abrir_cadastro_usuario(self, event):
        self.reiniciar_tela()
        self.tl = ttk.Toplevel(self.janela)
        CadastroUserView(self.tl)
        self.utils.call_top_view(self.janela, self.tl)

    def pedir_autenticacao(self, event):
        username = self.ent_username_value.get().replace(".","").replace("-","")
        password = self.ent_password_value.get()
        result = self.login_control.autenticar(f"'{username}'", f"'{password}'")
        if(result):
            """lbl_login_value = (
                f"Usuario logado
                id: {result[0]}\n"
                f"Nome:{result[0]}\n"
                f"CPF:{result[1]}\n"
                f"Telefone:{result[2]}\n"
                f"Papel:{result[4]}\n"
                f"Status:{result[5]}"
            )"""
            if result[5] == 'A':
                self.reiniciar_tela()
                self.tl = ttk.Toplevel(self.janela)
                HomeLinhaView(self.tl, None, result[4], result[0])
                self.utils.call_top_view(self.janela, self.tl)
            else:
                messagebox.showwarning('Aviso', 'Login Indisponível.\nUsuário desativado.')

        else:
            messagebox.showerror('Erro', 'Login Inválido.\nTente novamente.')

    def reiniciar_tela(self):
        self.ent_username_value.set("")
        self.ent_password_value.set("")
        self.btn_acessar.config(state='disabled')

    def fechar_janela(self, event):
        self.janela.destroy()