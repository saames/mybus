import ttkbootstrap as ttk
from resources.utils import Utils
from tkinter import messagebox

class OnibusForm:
    def __init__(self, master):
        # Ajustes na janela
        # self.janela_origem = janela_origem
        self.janela = master 
        self.janela.geometry('450x550')
        self.janela.title(" Formulário para Cadastrar um novo Ônibus - MyBus")
        self.janela.resizable(False, False)

        # Frame para centralizar os componentes no meio da janela
        self.frm_center = ttk.Frame(self.janela)
        self.frm_center.pack(expand=True, padx=10, pady=10)
        self.frm_center.columnconfigure(0, weight=1)

        # Titulo
        self.lbl_tile = ttk.Label(self.frm_center, text='Adicione um novo ônibus',  bootstyle='primary',font=('TkDefaultFont', 14, 'bold'))
        self.lbl_tile.grid(column=0,row=0, pady=(0,25),sticky='w')

        # Número do ônibus
        self.lbl_number = ttk.Label(self.frm_center, text='Número (obrigatório):',font=('TkDefaultFont', 10, 'bold'))
        self.lbl_number.grid(column=0, row=1,sticky='w', pady=(0, 2))
        self.ent_number = ttk.Entry(self.frm_center)
        self.ent_number.grid(column=0, row=2, sticky='ew', pady=(0,10))
        self.ent_number.bind('<KeyRelease>', self.validar_campos)

        # Placa do ônibus    
        self.lbl_plate = ttk.Label(self.frm_center, text='Placa (obrigatório):', font=('TkDefaultFont', 10, 'bold'))
        self.lbl_plate.grid(column=0, row=3, sticky='w', pady=(0, 2))
        self.ent_plate = ttk.Entry(self.frm_center)
        self.ent_plate.grid(column=0, row=4, sticky='ew', pady=(0, 10))
        self.ent_plate.bind('<KeyRelease>', self.validar_campos)
        Utils.add_placeholder(self.ent_plate,'XXXXXXX')


        # Status do ônibus
        self.lbl_status = ttk.Label(self.frm_center, text='Status:', font=('TkDefaultFont', 10, 'bold'))
        self.lbl_status.grid(column=0, row=5, sticky='w', pady=(0, 2))

        # frame pros radios
        self.frm_radios = ttk.Frame(self.frm_center)
        self.frm_radios.grid(column=0, row=6, sticky='ew')

        d = {0:'Inativo', 1:'Ativo'}
        self.var_rbt = ttk.IntVar(value=0) # O valor padrão dele vai ser inativo
        for chave, valor in d.items():
            rbt = ttk.Radiobutton(self.frm_radios, 
                                  text=valor, 
                                  value=chave, 
                                  variable=self.var_rbt )
            rbt.pack(side='left',padx=5, pady=(0,10))

        # Linha Associada ao ônibus
        self.lbl_line = ttk.Label(self.frm_center, text='Linha Associada:', font=('TkDefaultFont', 10, 'bold'))
        self.lbl_line.grid(column=0, row=7, sticky='w', pady=(0, 2))

        self.linha = ttk.StringVar()

        self.cbx_line = ttk.Combobox(self.frm_center, 
                                     textvariable=self.linha,
                                     state='readonly')
    
        self.cbx_line.grid(column=0, row=8, sticky='ew', pady=(0, 10))
        self.carrega_linhas()

        # frame dos botões
        self.frm_buttons = ttk.Frame(self.frm_center)
        self.frm_buttons.grid(column=0, row=11, pady=(25, 0), sticky='ew')
        self.frm_buttons.columnconfigure((0, 1), weight=1)

        # Botão Cancelar 
        self.btn_cancel = ttk.Button(self.frm_buttons, text='CANCELAR', bootstyle='danger')
        self.btn_cancel.grid(column=0, row=0, sticky='ew', padx=(0, 5))
        self.btn_cancel.bind('<ButtonRelease-1>', self.cancelar)

        # Botão Salvar 
        self.btn_save = ttk.Button(self.frm_buttons, text='SALVAR', bootstyle='success', state='disabled')
        self.btn_save.grid(column=1, row=0, sticky='ew', padx=(5, 0))
        self.btn_save.bind('<ButtonRelease-1>')


    def carrega_linhas(self):
        
        linhas = ['Linha 101 - Avenina Ceara'] # colocar os dados do banco aqui, vou so fazer uma coisa estatica por enquanto
        placeholder = ['Selecionar']
        lista = placeholder + linhas

        self.cbx_line['values'] = lista
        self.cbx_line.current(0)
        
    def validar_campos(self, event):
        numero = self.ent_number.get()
        placa = self.ent_plate.get()

        if len(placa) == 7 and numero != "" and placa != 'XXXXXXX':
            self.btn_save.config(state='enable')
            return True
        else:
            self.btn_save.config(state='disabled')
            return False
    
    def cancelar(self, event):
        can = messagebox.askquestion('Cancelar cadastro', 'Deseja cancelar o processo de cadastro no sistema?')
        if can == 'yes':
            self.janela.destroy()
            if self.janela_origem:
                self.janela_origem.deiconify()