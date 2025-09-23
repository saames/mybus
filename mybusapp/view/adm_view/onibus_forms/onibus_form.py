import ttkbootstrap as ttk
from tkinter import messagebox
from resources.utils import Utils
from control.gerenciar_linhas_control import GerenciarLinhasControl
from control.gerenciar_onibus_control import GerenciarOnibusControl
from tkinter import messagebox

class OnibusForm:
    def __init__(self, master, *args):
        # Ajustes na janela
        # self.janela_origem = janela_origem

        self.janela = master 
        self.janela.geometry('450x550')
        self.janela.title(" Formulário para Cadastrar um novo Ônibus - MyBus")
        self.janela.resizable(False, False)

        #Pegando as linha do banco de dados
        self.gereciar_linha = GerenciarLinhasControl()
        self.gereciar_onibus = GerenciarOnibusControl()

        #Pegando as informações de um onibus caso queira editar
        if args:
            self.onibus_editar = args[0]
        else:
            self.onibus_editar = None

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
        self.ent_number_value = ttk.StringVar()
        if self.onibus_editar:
            self.ent_number_value.set(self.onibus_editar[1])
        self.ent_number = ttk.Entry(self.frm_center, textvariable=self.ent_number_value)
        self.ent_number.grid(column=0, row=2, sticky='ew', pady=(0,10))
        self.ent_number.bind('<KeyRelease>', self.validar_campos)

        # Placa do ônibus    
        self.lbl_plate = ttk.Label(self.frm_center, text='Placa (obrigatório):', font=('TkDefaultFont', 10, 'bold'))
        self.lbl_plate.grid(column=0, row=3, sticky='w', pady=(0, 2))
        self.ent_plate_value = ttk.StringVar()
        if self.onibus_editar:
            self.ent_plate_value.set(self.onibus_editar[2])
        self.ent_plate = ttk.Entry(self.frm_center, textvariable=self.ent_plate_value)
        self.ent_plate.grid(column=0, row=4, sticky='ew', pady=(0, 10))
        self.ent_plate.bind('<KeyRelease>', self.validar_campos)
        Utils.add_placeholder(self.janela, self.ent_plate, 'XXXXXXX')


        # Status do ônibus
        self.lbl_status = ttk.Label(self.frm_center, text='Status:', font=('TkDefaultFont', 10, 'bold'))
        self.lbl_status.grid(column=0, row=5, sticky='w', pady=(0, 2))

        # frame pros radios
        self.frm_radios = ttk.Frame(self.frm_center)
        self.frm_radios.grid(column=0, row=6, sticky='ew')

        d = {0:'Inativo', 1:'Ativo'}
        self.var_rbt = ttk.IntVar(value=0) # O valor padrão dele vai ser inativo
        if self.onibus_editar:
            self.var_rbt.set(self.onibus_editar[3])
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
        self.linha_id = 0

        self.cbx_line = ttk.Combobox(self.frm_center, 
                                     textvariable=self.linha,
                                     state='readonly')
    
        self.cbx_line.grid(column=0, row=8, sticky='ew', pady=(0, 10))
        self.carrega_linhas()
        self.cbx_line.bind('<<ComboboxSelected>>', self.escolhendo_linha)

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
        self.btn_save.bind('<ButtonRelease-1>', self.cadastrar_onibus)


    def carrega_linhas(self):
        result = self.gereciar_linha.listar_linhas()
        self.keys = [""]
        self.values = ["Selecione"]

        for i in result:
            self.keys.append(i[0])
            self.values.append(f"{i[2]} : {i[1]}") # colocar os dados do banco aqui, vou so fazer uma coisa estatica por enquanto

        self.keys.append(None)
        self.values.append("Nenhuma linha associada.")

        self.cbx_line['values'] = self.values

        if self.onibus_editar:
            if(self.onibus_editar[4]):
                self.cbx_line.current(self.onibus_editar[4])
                self.linha_id = self.onibus_editar[4]
            else:
                self.cbx_line.current(len(self.keys) - 1)
                self.linha_id = len(self.keys) - 1
        else:
            self.cbx_line.current(0)


    def escolhendo_linha(self, event):
        linha = self.linha.get()
        self.linha_id = self.keys[self.values.index(linha)]

    def validar_campos(self, event):
        numero = self.ent_number.get()
        placa = self.ent_plate.get()

        if len(placa) == 8 and numero != "" and placa != 'XXXXXXX':
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

    def cadastrar_onibus(self, event):
        number = self.ent_number_value.get()
        plate = self.ent_plate_value.get()
        status = self.var_rbt.get()
        linha_id = self.linha_id
        if not self.onibus_editar:
            result = self.gereciar_onibus.inserir_onibus(number, plate, status, linha_id)
            if result:
                messagebox.showinfo("Informação", "Cadastro realizado com sucesso!")
                self.janela.destroy()
        else:
            result = self.gereciar_onibus.editar_onibus(self.onibus_editar[0], number, plate, status, linha_id)
            if result:
                messagebox.showinfo("Informação", "Edição realizada com sucesso!")
                self.janela.destroy()