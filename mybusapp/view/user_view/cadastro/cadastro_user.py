import tkinter as tk
import ttkbootstrap as ttk
from resources.utils import Utils
from tkinter import messagebox
from control.cadastrar_control import Cadastra_control
from validate_docbr import CPF

class CadastroUserView:
    def __init__(self, master, usuario = None):
        # Ajustes na janela
        self.janela = master
        self.usuario = usuario
        #self.janela.geometry('450x550')
        if(self.usuario == None):
            self.janela.title(" Formulário para Cadastro - MyBus")
        else:
            self.janela.title(" Formulário para Edição - MyBus")
        self.janela.resizable(False, False)

        # Criação de Instâncias
        self.cadastrar_control = Cadastra_control()
        self.utils = Utils()
        self.cpf_verificar = CPF()

        # Frame para centralizar os componentes no meio da janela
        self.frm_center = ttk.Frame(self.janela)
        self.frm_center.pack(expand=True, padx=10, pady=10)

        # Titulo
        if(usuario == None):
            lbl_title_text = " Crie uma conta "
        else:
            lbl_title_text = "Edite um usuario"
        self.lbl_title = ttk.Label(self.frm_center, text=lbl_title_text, bootstyle='primary-inverse', padding=(162, 11))
        self.lbl_title.grid(column=0,row=0, columnspan=2, pady=(0,20))

        # Nome Completo
        self.lbl_name = ttk.Label(self.frm_center, text='Nome Completo', bootstyle='inverse-secondary', 
                                                                         borderwidth=7, 
                                                                         padding=(11,0),
                                                                         font=('TkDefaultFont', 10, 'bold'))
        self.lbl_name.grid(column=0, row=1, sticky='w', pady=(0,5))
        self.ent_name_value = ttk.StringVar()
        if(self.usuario != None):
            self.ent_name_value.set(self.usuario[1])
        self.ent_name = ttk.Entry(self.frm_center, textvariable=self.ent_name_value)
        self.ent_name.grid(column=1, row=1, sticky='ew', ipadx=50, pady=(0,5))
        self.ent_name.bind('<KeyRelease>', self.validar_campos)

        if(self.usuario == None):
            # CPF
            self.lbl_CPF = ttk.Label(self.frm_center, text='CPF', bootstyle='inverse-secondary', 
                                                                borderwidth=7, 
                                                                padding=(56,0),
                                                                font=('TkDefaultFont', 10, 'bold'))
            self.lbl_CPF.grid(column=0, row=2, sticky='w', pady=(0,5))
            self.ent_CPF_value = ttk.StringVar()
            if(self.usuario != None):
                self.ent_CPF_value.set(self.usuario[2])
            self.ent_CPF = ttk.Entry(self.frm_center, textvariable=self.ent_CPF_value)
            self.ent_CPF.grid(column=1, row=2, sticky='ew', pady=(0, 5))
            self.ent_CPF.bind('<KeyRelease>', self.validar_campos)
            self.utils.add_placeholder(self.ent_CPF,'XXX.XXX.XXX-XX')

        # Email do usuário 
        self.lbl_email = ttk.Label(self.frm_center, text='Email', bootstyle='inverse-secondary', 
                                                                  borderwidth=7, 
                                                                  padding=(50,0),
                                                                  font=('TkDefaultFont', 10, 'bold'))
        self.lbl_email.grid(column=0, row=3, sticky='w', pady=(0, 5))
        self.ent_email_value = ttk.StringVar()
        if(self.usuario != None):
            self.ent_email_value.set(self.usuario[7])
        self.ent_email = ttk.Entry(self.frm_center, textvariable=self.ent_email_value)
        self.ent_email.grid(column=1, row=3, sticky='ew', pady=(0, 5))
        self.ent_email.bind('<KeyRelease>', self.validar_campos)
        
        # Telefone do usuário 
        self.lbl_phone = ttk.Label(self.frm_center, text='Telefone', bootstyle='inverse-secondary', 
                                                                     borderwidth=7, 
                                                                     padding=(38,0),
                                                                     font=('TkDefaultFont', 10, 'bold'))
        self.lbl_phone.grid(column=0, row=4, sticky='w', pady=(0, 5))
        self.ent_phone_value = ttk.StringVar()
        if(self.usuario != None):
            self.ent_phone_value.set(self.usuario[3])
        self.ent_phone = ttk.Entry(self.frm_center, textvariable=self.ent_phone_value)
        self.ent_phone.grid(column=1, row=4, sticky='ew', pady=(0, 5))
        self.ent_phone.bind('<KeyRelease>', self.validar_campos)
        self.utils.add_placeholder(self.ent_phone, '(XX)XXXXXXXXX')

        if(self.usuario == None):
            # Senha do usuário
            self.lbl_password = ttk.Label(self.frm_center, text='Senha (8 dígitos)', bootstyle='inverse-secondary', 
                                                                        borderwidth=7, 
                                                                        padding=(6,0),
                                                                        font=('TkDefaultFont', 10, 'bold'))
            self.lbl_password.grid(column=0, row=5, sticky='w', pady=(0, 5))
            self.ent_password_value = ttk.StringVar()
            if(self.usuario != None):
                self.ent_password_value.set(self.usuario[6])
            self.ent_password = ttk.Entry(self.frm_center, show='*', textvariable=self.ent_password_value)
            self.ent_password.grid(column=1, row=5, sticky='ew', pady=(0, 5))
            self.ent_password.bind('<KeyRelease>', self.validar_campos)

            # Confirmar senha
            self.lbl_checker_pass = ttk.Label(self.frm_center, text='Confirmar Senha', bootstyle='inverse-secondary', 
                                                                                    borderwidth=7, 
                                                                                    padding=(7,0),
                                                                                    font=('TkDefaultFont', 10, 'bold'))
            self.lbl_checker_pass.grid(column=0, row=6, sticky='w', pady=(0, 5))
            self.ent_checker_pass_value = ttk.StringVar()
            if(self.usuario != None):
                self.ent_checker_pass_value.set(self.usuario[6])
            self.ent_checker_pass = ttk.Entry(self.frm_center, show='*', textvariable=self.ent_checker_pass_value)
            self.ent_checker_pass.grid(column=1, row=6, sticky='ew', pady=(0, 5))
            self.ent_checker_pass.bind('<KeyRelease>', self.validar_campos)
        
        # Frame dos botões
        self.frm_buttons = ttk.Frame(self.frm_center)
        self.frm_buttons.grid(column=0, row=7, columnspan=2, pady=(25, 0))

        # Botão Cancelar 
        self.btn_cancel = ttk.Button(self.frm_buttons, text='CANCELAR', bootstyle='danger')
        self.btn_cancel.grid(column=0, row=0, padx=(0,5))
        self.btn_cancel.bind('<ButtonRelease-1>', self.cancelar)

        # Botão Salvar 
        self.btn_save = ttk.Button(self.frm_buttons, text='SALVAR', bootstyle='success', state='disabled')
        self.btn_save.grid(column=1, row=0)
        self.btn_save.bind('<ButtonRelease-1>', self.cadastrar)

        # Comandos de navegação
        self.janela.bind('<Escape>', self.cancelar)
        self.janela.bind('<Return>', self.cadastrar)

        self.utils.centraliza(self.janela)

    def validar_campos(self, *event):
        nome = self.ent_name.get()
        email = self.ent_email.get()
        if(self.usuario == None):
            senha = self.ent_password.get()
            confirmar_senha = self.ent_checker_pass.get()
            cpf = self.ent_CPF.get().replace(".","").replace("-","")
        telefone = self.ent_phone.get().replace("(","").replace(")","").replace("-","")
        
        # Verifica se os campos estão corretamente inseridos.
        if(self.usuario == None):
            insercao_campos = (telefone.isdigit() and len(telefone)==11
                            and nome != ""
                            and len(cpf) == 11
                            and len(senha) >= 8
                            and confirmar_senha == senha
                            and "@" in email
                            and self.cpf_verificar.validate(f"{cpf[0:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}")
                            )
        else:
            insercao_campos = (telefone.isdigit() and len(telefone)==11
                            and nome != ""
                            and "@" in email
                            )

        # Verifica se os campos foram alterados em uma edição.
        if self.usuario:
            sem_alteracoes_campos = (nome == self.usuario[1]
                                     and telefone == self.usuario[3]
                                     and email == self.usuario[7]
                                     )
            if insercao_campos and sem_alteracoes_campos:
                self.btn_save.config(state='disabled')
                return False

        if insercao_campos:
            self.btn_save.config(state='normal')
            return True
        else:
            self.btn_save.config(state='disabled')
            return False
    
    def cancelar(self, event):
        if(self.usuario == None):
            can = messagebox.askquestion('Cancelar cadastro', 'Deseja cancelar a operação de cadastro de usuário?')
        else:
            can = messagebox.askquestion('Cancelar cadastro', 'Deseja cancelar a operação de edição de usuário?')
        if can == 'yes':
            self.janela.destroy()

    def cadastrar(self, event):
        if self.validar_campos():
            name = self.ent_name_value.get()
            email = self.ent_email.get()
            phone = self.ent_phone_value.get().replace("(", "").replace(")", "")
            if(self.usuario == None):
                cpf = self.ent_CPF_value.get().replace(".","").replace("-","")

                # Validando se já existe um cpf, email, ou telefone cadastrado no sistema
                if self.cadastrar_control.verificar_cpf_existente(cpf):
                    messagebox.showerror("Erro de Validação", "O CPF informado já está cadastrado no sistema.")
                    return 

                if self.cadastrar_control.verificar_email_existente(email):
                    messagebox.showerror("Erro de Validação", "O e-mail informado já está cadastrado no sistema.")
                    return
                
                if self.cadastrar_control.verificar_telefone_existente(phone):
                    messagebox.showerror("Erro de Validação", "O telefone informado já está cadastrado no sistema.")
                    return

                password = self.ent_password_value.get()
                result = self.cadastrar_control.Cadastrar_usuario(name, cpf, phone, password, "user", "A", email)
                if(result):
                    messagebox.showinfo("Informação", "Cadastro realizado com sucesso!")
                    self.janela.destroy()
            else:
                user_id = self.usuario[0]
                original_email = self.usuario[7] if len(self.usuario) > 7 else None
                original_phone = self.usuario[3]

                if email != original_email and self.cadastrar_control.verificar_email_existente(email, user_id):
                    messagebox.showerror("Erro de Validação", "O e-mail informado já está sendo utilizado por outro usuário.")
                    return

                if phone != original_phone and self.cadastrar_control.verificar_telefone_existente(phone, user_id):
                    messagebox.showerror("Erro de Validação", "O telefone informado já está sendo utilizado por outro usuário.")
                    return
            
                result = self.cadastrar_control.editar_usuario(self.usuario[0], name, self.usuario[2], self.usuario[6], phone, self.usuario[4], "A", email)
                if(result):
                    messagebox.showinfo("Informação", "Edição realizada com sucesso!")
                    self.janela.destroy()
        else:
            messagebox.showerror('Erro', 'Preencha todos os campos corretamente.')

