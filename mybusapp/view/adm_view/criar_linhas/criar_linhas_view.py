import ttkbootstrap as ttk
from resources.utils import Utils

class CriarLinhaView:
    def __init__(self, master):
        self.janela = master
        self.janela.title('Criar Linha - MyBus')
        self.janela.geometry('400x300')
        self.janela.resizable(False, False)
        self.frm_center = ttk.Frame(self.janela)
        self.frm_center.pack(padx=10, pady=10)

        # Criação de Instâncias
        self.utils = Utils()

        # Titulo
        self.lbl_title = ttk.Label(self.frm_center, text='Criar Linha',  bootstyle='primary',font=('TkDefaultFont', 14, 'bold'))
        self.lbl_title.grid(column=0,row=0, sticky='we', columnspan=2, pady=(15,15))

        # Nome da rota
        self.lbl_name = ttk.Label(self.frm_center, text='Nome:',font=('TkDefaultFont', 10, 'bold'))
        self.lbl_name.grid(column=0, row=1,sticky='w', pady=(0, 2))
        self.ent_name_value = ttk.StringVar()
        self.ent_name = ttk.Entry(self.frm_center, textvariable=self.ent_name_value)
        self.ent_name.grid(column=0, row=2, sticky='ew', pady=(0,10))
        self.ent_name.bind('<KeyRelease>', self.validar_campos)

        # Número da rota
        self.lbl_numero = ttk.Label(self.frm_center, text='Número:',font=('TkDefaultFont', 10, 'bold'))
        self.lbl_numero.grid(column=0, row=3,sticky='w', pady=(0, 2))
        self.spb_numero_value = ttk.IntVar(value=1)
        self.spb_numero = ttk.Spinbox(self.frm_center, textvariable=self.spb_numero_value, from_=1, to=999, format='%03.0f')
        self.spb_numero.set(f"{self.spb_numero_value.get():03d}") # Solução para o número começar com 3 casas antes da vírgula.
        self.spb_numero.grid(column=0, row=4, sticky='ew', pady=(0,15))
        self.spb_numero.bind('<KeyRelease>', self.validar_campos)
        self.spb_numero.bind('<ButtonRelease>', self.validar_campos)
        
        # Frame para os botões
        self.frm_menu = ttk.Frame(self.frm_center)
        self.frm_menu.grid(column=0, row=5)
        # Botão Cancelar
        self.btn_cancel = ttk.Button(self.frm_menu, text='CANCELAR', bootstyle='danger')
        self.btn_cancel.grid(column=0, row=0, sticky='ew', padx=(0,30))
        self.btn_cancel.bind('<ButtonRelease-1>')

        # Botão Continuar
        self.btn_continuar = ttk.Button(self.frm_menu, text='CONTINUAR', bootstyle='success', state='disabled')
        self.btn_continuar.grid(column=1, row=0, sticky='ew')
        self.btn_continuar.bind('<ButtonRelease-1>')



        self.utils.centraliza(self.janela)

    
    def validar_campos(self, event):
        nome = self.ent_name.get()
        numero = self.spb_numero.get()
        if numero.isdigit() and len(numero)==3 and len(nome)>=4: # O nome deve ter tamanho >= 4 e o número deve ter 3 casas antes da vírgula.
            self.btn_continuar.config(state='enable')
        else:
            self.btn_continuar.config(state='disabled')