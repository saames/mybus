import tkinter as tk
import ttkbootstrap as ttk
from placeholder import PlaceHolder
from tkinter import messagebox

class CadastroUser:
    def __init__(self, master):
        # Ajustes na janela
        self.janela = master 
        self.janela.geometry('450x550')
        self.janela.title(" Formulário para Cadastro")
        self.janela.resizable(False, False)

        # Frame para centralizar os componentes no meio da janela
        self.frm_center = ttk.Frame(self.janela)
        self.frm_center.pack(expand=True, padx=10, pady=10)
        self.frm_center.columnconfigure(0, weight=1)

        # Titulo
        self.lbl_tile = ttk.Label(self.frm_center, text='Crie uma conta',  bootstyle='primary',font=('TkDefaultFont', 14, 'bold'))
        self.lbl_tile.grid(column=0,row=0, pady=(0,25),sticky='w')

        # Nome do usuário
        self.lbl_name = ttk.Label(self.frm_center, text='Nome:',font=('TkDefaultFont', 10, 'bold'))
        self.lbl_name.grid(column=0, row=1,sticky='w', pady=(0, 2))
        self.ent_name = ttk.Entry(self.frm_center)
        self.ent_name.grid(column=0, row=2, sticky='ew', pady=(0,10))

        # CPF do usuário    
        self.lbl_CPF = ttk.Label(self.frm_center, text='CPF:', font=('TkDefaultFont', 10, 'bold'))
        self.lbl_CPF.grid(column=0, row=3, sticky='w', pady=(0, 2))
        self.ent_CPF = ttk.Entry(self.frm_center)
        self.ent_CPF.grid(column=0, row=4, sticky='ew', pady=(0, 10))
        PlaceHolder.add_placeholder(self.ent_CPF,'00000000000')
    

        # Telefone do usuário 
        self.lbl_phone = ttk.Label(self.frm_center, text='Telefone:', font=('TkDefaultFont', 10, 'bold'))
        self.lbl_phone.grid(column=0, row=5, sticky='w', pady=(0, 2))
        self.ent_phone = ttk.Entry(self.frm_center)
        self.ent_phone.grid(column=0, row=6, sticky='ew', pady=(0, 10))
        PlaceHolder.add_placeholder(self.ent_phone, '(00)00000000')

        # Senha do usuário
        self.lbl_password = ttk.Label(self.frm_center, text='Senha (Tamanho maior ou igual a 8):', font=('TkDefaultFont', 10, 'bold'))
        self.lbl_password.grid(column=0, row=7, sticky='w', pady=(0, 2))
        self.ent_password = ttk.Entry(self.frm_center, show='*')
        self.ent_password.grid(column=0, row=8, sticky='ew', pady=(0, 10))


        # Confirmar senha
        self.lbl_checker_pass = ttk.Label(self.frm_center, text='Confirmar Senha:', font=('TkDefaultFont', 10, 'bold'))
        self.lbl_checker_pass.grid(column=0, row=9, sticky='w', pady=(0, 2))
        self.ent_checker_pass = ttk.Entry(self.frm_center, show='*')
        self.ent_checker_pass.grid(column=0, row=10, sticky='ew', pady=(0, 10))
        
        # frame dos botões
        self.frm_buttons = ttk.Frame(self.frm_center)
        self.frm_buttons.grid(column=0, row=11, pady=(25, 0), sticky='ew')
        self.frm_buttons.columnconfigure((0, 1), weight=1)

        # Botão Cancelar 
        self.btn_cancel = ttk.Button(self.frm_buttons, text='Cancelar', bootstyle='danger', command=self.cancelar)
        self.btn_cancel.grid(column=0, row=0, sticky='ew', padx=(0, 5))

        # Botão Salvar 
        self.btn_save = ttk.Button(self.frm_buttons, text='Salvar', bootstyle='success', state='disabled')
        self.btn_save.grid(column=1, row=0, sticky='ew', padx=(5, 0))
        self.btn_save.bind('<ButtonRelease-1>', self.validar_campos)


    def validar_campos(self, event):
        nome = self.ent_name.get()
        cpf = self.ent_CPF.get()
        senha = self.ent_password.get()
        confirmar_senha = self.ent_checker_pass.get()
        telefone = self.ent_phone.get()

        if len(telefone) >= 12 and nome != "" and len(cpf) == 11 and len(senha) >= 8 and confirmar_senha == senha:
            self.btn_save.config(state='enable')
        else:
            self.btn_save.config(state='disabled')
    
    def cancelar(self):
        can = messagebox.askquestion('Cancelar cadastro', 'Deseja cancelar o processo de cadastro no sistema?')
        if can == 'yes':
            self.janela.destroy()



app = ttk.Window(themename='mybus')
CadastroUser(app)
app.mainloop()