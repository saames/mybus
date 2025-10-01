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
        #self.janela.geometry('450x550')
        self.janela.title("Cadastrar ônibus - MyBus")
        self.janela.resizable(False, False)

        self.frm_center = ttk.Frame(self.janela)
        self.frm_center.pack(expand=True, padx=10, pady=10)

        #Pegando as linha do banco de dados
        self.utils = Utils()
        self.gereciar_linha = GerenciarLinhasControl()
        self.gereciar_onibus = GerenciarOnibusControl()

        #Pegando as informações de um onibus caso queira editar
        if args:
            print(args)
            self.onibus_editar = args[0]
        else:
            self.onibus_editar = None

        # Titulo
        self.lbl_title = ttk.Label(self.frm_center, text='Cadastrar ônibus', bootstyle='primary-inverse', padding=(120, 11))
        self.lbl_title.grid(column=0,row=0, columnspan=2, pady=(0,20))

        # Número do ônibus
        self.lbl_number = ttk.Label(self.frm_center, text='Número',bootstyle='inverse-secondary', 
                                                                                  borderwidth=7, 
                                                                                  padding=(36,0),
                                                                                  font=('TkDefaultFont', 10, 'bold'))
        self.lbl_number.grid(column=0, row=1, sticky='w', pady=(0,5))
        
        self.spb_number_value = ttk.IntVar(value=1)
        if self.onibus_editar:
            self.spb_number_value.set(self.onibus_editar[1])

        self.spb_number = ttk.Spinbox(self.frm_center, textvariable=self.spb_number_value, from_=1, to=999, format='%03.0f')
        #self.spb_number.set(f"{self.spb_number_value.get():03d}") # Solução para o número começar com 3 casas antes da vírgula.
        self.spb_number.grid(column=1, row=1, sticky='ew', pady=(0, 5))
        self.spb_number.bind('<KeyRelease>', self.validar_campos)
        self.spb_number.bind('<ButtonRelease>', self.validar_campos)
        
        # self.ent_number_value = ttk.StringVar()
        # if self.onibus_editar:
        #     self.ent_number_value.set(self.onibus_editar[1])
        # self.ent_number = ttk.Entry(self.frm_center, textvariable=self.ent_number_value)
        # self.ent_number.grid(column=1, row=1, sticky='ew', ipadx=60, pady=(0,5))
        # self.ent_number.bind('<KeyRelease>', self.validar_campos)

        # Placa do ônibus
        self.lbl_plate = ttk.Label(self.frm_center, text='Placa', bootstyle='inverse-secondary', 
                                                                  borderwidth=7, 
                                                                  padding=(45,0),
                                                                  font=('TkDefaultFont', 10, 'bold'))
        self.lbl_plate.grid(column=0, row=2, sticky='w', pady=(0,5))
        self.ent_plate_value = ttk.StringVar()
        if self.onibus_editar:
            self.ent_plate_value.set(self.onibus_editar[2])
        self.ent_plate = ttk.Entry(self.frm_center, textvariable=self.ent_plate_value)
        self.ent_plate.grid(column=1, row=2, sticky='ew', pady=(0, 5))
        self.ent_plate.bind('<KeyRelease>', self.validar_campos)
        Utils.add_placeholder(self.janela, self.ent_plate, 'XXX-XXXX')

        # Status do ônibus
        self.lbl_status = ttk.Label(self.frm_center, text='Status', bootstyle='inverse-secondary', 
                                                                    borderwidth=7, 
                                                                    padding=(42,0),
                                                                    font=('TkDefaultFont', 10, 'bold'))
        self.lbl_status.grid(column=0, row=3, sticky='w', pady=(0,5))

        # frame pros radios
        self.frm_radios = ttk.Frame(self.frm_center)
        self.frm_radios.grid(column=1, row=3, sticky='ew', pady=(0, 5))

        d = {0:'Inativo', 1:'Ativo'}
        self.var_rbt = ttk.IntVar(value=0) # O valor padrão dele vai ser inativo
        if self.onibus_editar:
            self.var_rbt.set(self.onibus_editar[3])
        cont = 0
        for chave, valor in d.items():
            rbt = ttk.Radiobutton(self.frm_radios, 
                                  text=valor, 
                                  value=chave, 
                                  variable=self.var_rbt,
                                  command=self.validar_campos)
            rbt.grid(row=0, column=cont, padx=5)
            #rbt.bind('<ButtonRelease-1>', ) # Vincular a cada radiobutton
            cont += 1

        # Linha Associada ao ônibus
        self.lbl_line = ttk.Label(self.frm_center, text='Linha Associada', bootstyle='inverse-secondary', 
                                                                           borderwidth=7, 
                                                                           padding=(5,0),
                                                                           font=('TkDefaultFont', 10, 'bold'))
        self.lbl_line.grid(column=0, row=4, sticky='w', pady=(0,5))

        self.linha = ttk.StringVar()
        self.linha_id = 0

        self.cbx_line = ttk.Combobox(self.frm_center, 
                                     textvariable=self.linha,
                                     state='readonly')
    
        self.cbx_line.grid(column=1, row=4, sticky='ew', pady=(0, 5))
        self.carrega_linhas()
        self.cbx_line.bind('<<ComboboxSelected>>', self.escolhendo_linha)

        # frame dos botões
        self.frm_buttons = ttk.Frame(self.frm_center)
        self.frm_buttons.grid(column=0, row=5, columnspan=2, pady=(25, 0))

        # Botão Cancelar 
        self.btn_cancel = ttk.Button(self.frm_buttons, text='CANCELAR', bootstyle='danger')
        self.btn_cancel.grid(column=0, row=0, sticky='ew', padx=(0, 5))
        self.btn_cancel.bind('<ButtonRelease-1>', self.cancelar)

        # Botão Salvar 
        self.btn_save = ttk.Button(self.frm_buttons, text='SALVAR', bootstyle='success', state='disabled')
        self.btn_save.grid(column=1, row=0, sticky='ew')
        self.btn_save.bind('<ButtonRelease-1>', self.cadastrar_onibus)

        self.utils.centraliza(self.janela)



    def carrega_linhas(self):
        result = self.gereciar_linha.listar_linhas()
        self.keys = [""]
        self.values = ["Selecione"]

        for i in result:
            self.keys.append(i[0])
            self.values.append(f"{i[2]} : {i[1]}")

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
        self.validar_campos()

    def validar_campos(self, *event):
        numero = self.spb_number.get()
        placa = self.ent_plate.get().replace("-","")
        status = self.var_rbt.get()
        linha_id = self.linha_id

        # Verifica se os campos estão corretamente inseridos.
        insercao_campos = (len(placa) == 7 
                           and numero 
                           and linha_id != "") # Evita que o usuário escolha "Selecione" no combobox
        
        # Verifica se os campos foram alterados em uma edição.
        if self.onibus_editar:
            print(f'numero: {numero} | self.onibus_editar[1]: {self.onibus_editar[1]}')
            print(f'placa: {placa} | self.onibus_editar[2]: {self.onibus_editar[2]}')
            print(f'status: {status} | self.onibus_editar[3]: {self.onibus_editar[3]}')
            print(f'linha_id: {linha_id} | self.onibus_editar[4]: {self.onibus_editar[4]}')
            sem_alteracoes_campos = (numero == self.onibus_editar[1] 
                                and placa == self.onibus_editar[2]
                                and status == self.onibus_editar[3] 
                                and linha_id == self.onibus_editar[4])
            if insercao_campos and sem_alteracoes_campos:
                self.btn_save.config(state='disabled')
                return False

        if insercao_campos:
            self.btn_save.config(state='normal')
            return True
        else:
            self.btn_save.config(state='disabled')
            return False
    
    def cancelar(self):
        can = messagebox.askquestion('Cancelar cadastro', 'Deseja cancelar o processo de cadastro no sistema?')
        if can == 'yes':
            self.janela.destroy()
 
    def cadastrar_onibus(self, event):
        number = self.spb_number_value.get()
        plate = self.ent_plate_value.get().replace("-","")
        status = self.var_rbt.get()
        linha_id = self.linha_id
        if not self.onibus_editar:
            if self.validar_campos():
                result = self.gereciar_onibus.inserir_onibus(number, plate, status, linha_id)
                if result:
                    messagebox.showinfo("Informação", "Cadastro realizado com sucesso!")
                    self.janela.destroy()
            else:
                messagebox.showerror('Erro', 'Insira os dados corretamente.')
        else:
            if self.validar_campos():
                result = self.gereciar_onibus.editar_onibus(self.onibus_editar[0], number, plate, status, linha_id)
                if result:
                    messagebox.showinfo("Informação", "Edição realizada com sucesso!")
                    self.janela.destroy()
            else:
                messagebox.showwarning('Aviso', 'É necessário alterar dados para salvar uma edição.')