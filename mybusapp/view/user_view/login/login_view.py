import ttkbootstrap as ttk
from mybusapp.control.login_control import LoginControl
from mybusapp.resources.photos import Base64
from mybusapp.resources.utils import Utils
from mybusapp.view.user_view.cadastro.cadastro_user import (CadastroUserView)

class LoginView:
    def __init__(self, master):
        self.janela = master
        self.janela.title('Login - MyBus')
        self.janela.geometry('440x380')
        self.frm_center = ttk.Frame(self.janela)
        self.frm_center.pack()

        #Login Control
        self.login_control = LoginControl()

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
        self.lbl_username.grid(column=0, row=1)
        self.ent_username_value = ttk.StringVar()
        self.ent_username = ttk.Entry(self.frm_center, textvariable=self.ent_username_value)
        self.ent_username.grid(column=1, row=1)
        self.ent_username.bind('<KeyRelease>', self.validar_campos)
        Utils.add_placeholder(self.ent_username,'XXX.XXX.XXX-XX')

        # Senha
        self.lbl_password = ttk.Label(self.frm_center, text='SENHA', bootstyle='inverse-secondary', 
                                                                     borderwidth=7, 
                                                                     padding=(2,0),
                                                                     font=('TkDefaultFont', 10, 'bold'))
        self.lbl_password.grid(column=0, row=2)
        self.ent_password_value = ttk.StringVar()
        self.ent_password = ttk.Entry(self.frm_center, show='*', textvariable=self.ent_password_value)
        self.ent_password.grid(column=1, row=2, pady=5)
        self.ent_password.bind('<KeyRelease>', self.validar_campos)

        # Botão Logar
        self.btn_acessar = ttk.Button(self.frm_center, text='ACESSAR', state='disabled')
        self.btn_acessar.grid(column=0, row=3, columnspan=2, sticky='we', pady=5)
        self.btn_acessar.bind('<ButtonRelease-1>', self.pedir_autenticacao)

        # Botão Cadastrar
        self.btn_cadastrar = ttk.Button(self.frm_center, text='Não possuo cadastro', bootstyle='LINK')
        self.btn_cadastrar.grid(column=0, row=4, columnspan=2, pady=10)
        self.btn_cadastrar.bind('<ButtonRelease-1>', self.abrir_cadastro_usuario)

        #Label Para mostrar que o login tá funcionando *Excluir depois*
        self.lbl_login = ttk.Label(self.frm_center)
        self.lbl_login.grid(column=0, row=5, columnspan=2, pady=10)

    # Restrições básicas para autenticação
    def validar_campos(self, event):
        cpf = self.ent_username.get().replace(".","").replace("-","")
        senha = self.ent_password.get()
        if len(cpf)==11 and len(senha) >= 8: # CPF tem tamanho 11 e senha maior ou igual 8.
            self.btn_acessar.config(state='enable')
        else:
            self.btn_acessar.config(state='disabled')

    # Abre a janela CadastroUsuarioView
    def abrir_cadastro_usuario(self, event):
        self.janela.withdraw() # Oculta janela, iconify() para apenas minimizar.
        self.janela_cadastro = ttk.Toplevel(self.janela)
        self.janela_cadastro.grab_set() # Impede interação com as demais janelas
        CadastroUserView(self.janela_cadastro, self.janela)

    def pedir_autenticacao(self, event):
        username = self.ent_username_value.get()
        password = self.ent_password_value.get()
        result = self.login_control.autenticar(f"'{username}'", f"'{password}'")
        if(result):
            lbl_login_value = (
                f"Usuario logado id: {result[0]}\n"
                f"Nome:{result[0]}\n"
                f"CPF:{result[1]}\n"
                f"Telefone:{result[2]}\n"
                f"Papel:{result[4]}\n"
                f"Status:{result[5]}"
            )
            self.lbl_login.config(text=lbl_login_value)
        else:
            lbl_login_value = (
                f"Login Invalido"
            )
            self.lbl_login.config(text=lbl_login_value)
