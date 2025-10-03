from tkinter import messagebox
import ttkbootstrap as ttk
from resources.utils import Utils

class DefinirNovaSenhaView:
    def __init__(self, master, janela_origem):
        # Ajustes na janela
        self.janela = master
        self.janela.title("Redefinir senha - MyBus")
        self.janela.resizable(False, False)
        self.frm_center = ttk.Frame(self.janela)
        self.frm_center.pack(expand=True, padx=10, pady=10)

        # Criação de Instâncias
        self.utils = Utils()

        # Título
        self.lbl_title = ttk.Label(self.frm_center, text='Redefinir Senha', bootstyle='primary-inverse', padding=(116, 11))
        self.lbl_title.grid(column=0,row=0, columnspan=2, pady=(0,40))

        # Senha do usuário
        self.lbl_password = ttk.Label(self.frm_center, text='Senha (8 dígitos)', bootstyle='inverse-secondary', 
                                                                     borderwidth=7, 
                                                                     padding=(6,0),
                                                                     font=('TkDefaultFont', 10, 'bold'))
        self.lbl_password.grid(column=0, row=1, sticky='w', pady=(0, 5))
        self.ent_password_value = ttk.StringVar()
        self.ent_password = ttk.Entry(self.frm_center, show='*', textvariable=self.ent_password_value)
        self.ent_password.grid(column=1, row=1, sticky='ew', pady=(0, 5))
        self.ent_password.bind('<KeyRelease>', self.validar_campos)

        # Confirmar senha
        self.lbl_checker_pass = ttk.Label(self.frm_center, text='Confirmar Senha', bootstyle='inverse-secondary', 
                                                                                   borderwidth=7, 
                                                                                   padding=(7,0),
                                                                                   font=('TkDefaultFont', 10, 'bold'))
        self.lbl_checker_pass.grid(column=0, row=2, sticky='w', pady=(0, 5))
        self.ent_checker_pass_value = ttk.StringVar()
        self.ent_checker_pass = ttk.Entry(self.frm_center, show='*', textvariable=self.ent_checker_pass_value)
        self.ent_checker_pass.grid(column=1, row=2, sticky='ew', pady=(0, 5))
        self.ent_checker_pass.bind('<KeyRelease>', self.validar_campos)

        # Frame dos botões
        self.frm_buttons = ttk.Frame(self.frm_center)
        self.frm_buttons.grid(column=0, row=3, columnspan=2, pady=(40, 0))

        # Botão Cancelar 
        self.btn_cancel = ttk.Button(self.frm_buttons, text='CANCELAR', bootstyle='danger')
        self.btn_cancel.grid(column=0, row=0, padx=(0,5))
        self.btn_cancel.bind('<ButtonRelease-1>', self.cancelar)

        # Botão Continuar
        self.btn_continuar = ttk.Button(self.frm_buttons, text='CONTINUAR', bootstyle='success', state='disabled')
        self.btn_continuar.grid(column=1, row=0)
        self.btn_continuar.bind('<ButtonRelease-1>', self.continuar)

        # Comandos de navegação
        self.janela.bind('<Return>')
        self.janela.bind('<Escape>')

        self.utils.centraliza(self.janela)
    
    def validar_campos(self, *event):
        senha = self.ent_password.get()
        confirmar_senha = self.ent_checker_pass.get()
        if len(senha) >= 8 and confirmar_senha == senha:
            self.btn_continuar.config(state='enable')
            return True
        else:
            self.btn_continuar.config(state='disabled')
            return False
        
    def cancelar(self, *event):
        self.janela.destroy()

    def continuar(self, *event):
        if self.validar_campos():
            nova_senha = self.ent_password_value.get()
            result = '' #implementar
            if result:
                messagebox.showinfo("Sucesso", "Senha alterada com sucesso!")
                self.janela.destroy()
            else:
                messagebox.showerror("Erro", "Ocorreu um erro ao tentar alterar a senha.")
