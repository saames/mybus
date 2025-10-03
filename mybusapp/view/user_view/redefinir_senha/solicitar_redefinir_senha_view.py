from tkinter import messagebox
import ttkbootstrap as ttk
from resources.utils import Utils
from view.user_view.redefinir_senha.codigo_seguranca_view import CodigoSegurancaView
from control.redefinir_senha_control import RedefinirSenhaControl

class SolicitarRedefinirSenhaView:
    def __init__(self, master):
        # Ajustes na janela
        self.janela = master
        self.janela.title("Redefinir senha - MyBus")
        self.janela.resizable(False, False)
        self.frm_center = ttk.Frame(self.janela)
        self.frm_center.pack(expand=True, padx=10, pady=10)

        # Criação de Instâncias
        self.utils = Utils()
        self.rs_control = RedefinirSenhaControl()

        # Título
        self.lbl_title = ttk.Label(self.frm_center, text='Redefinir Senha', bootstyle='primary-inverse', padding=(71, 11))
        self.lbl_title.grid(column=0,row=0, columnspan=2, pady=(0,40))

        self.lbl_CPF = ttk.Label(self.frm_center, text='CPF', bootstyle='inverse-secondary', 
                                                              borderwidth=7, 
                                                              padding=(13,0),
                                                              font=('TkDefaultFont', 10, 'bold'))
        self.lbl_CPF.grid(column=0, row=1, sticky='w', pady=(0,5))
        self.ent_CPF_value = ttk.StringVar()
        self.ent_CPF = ttk.Entry(self.frm_center, textvariable=self.ent_CPF_value)
        self.ent_CPF.grid(column=1, row=1, sticky='ew', pady=(0, 5))
        self.ent_CPF.bind('<KeyRelease>', self.validar_campos)
        self.utils.add_placeholder(self.ent_CPF,'XXX.XXX.XXX-XX')

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
        self.janela.bind('<Return>', self.continuar)
        self.janela.bind('<Escape>', self.cancelar)

        self.utils.centraliza(self.janela)
    

    
    def validar_campos(self, *event):
        self.cpf = self.ent_CPF.get().replace(".","").replace("-","")
        if len(self.cpf) == 11 and self.cpf != "XXXXXXXXXXX":
            self.btn_continuar.config(state='enable')
            return True
        else:
            self.btn_continuar.config(state='disabled')
            return False

    def cancelar(self, *event):
        self.janela.destroy()

    def continuar(self, event):
        usuario = self.rs_control.buscar_usuario_cpf(self.cpf)
        if len(usuario) == 1:
            if self.validar_campos():
                self.tl = ttk.Toplevel(self.janela)
                # Implementar aqui um "Loading" visual em self.janela  
                CodigoSegurancaView(self.tl, self.janela, usuario[0])
                self.janela.withdraw()
                self.janela.wait_window(self.tl)
                self.janela.destroy()
            else:
                messagebox.showerror('Erro', 'Preencha o campo CPF corretamente.')
        else:
            messagebox.showerror('Erro', 'Não foi possível encontrar o usuário.')