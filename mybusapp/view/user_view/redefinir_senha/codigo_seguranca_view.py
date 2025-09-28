import ttkbootstrap as ttk
from resources.utils import Utils

class CodigoSegurancaView:
    def __init__(self, master):
        # Ajustes na janela
        self.janela = master
        self.janela.title("Código de Segurança - MyBus")
        self.janela.resizable(False, False)
        self.frm_center = ttk.Frame(self.janela)
        self.frm_center.pack(expand=True, padx=10, pady=10)

        # Criação de Instâncias
        self.utils = Utils()

        # Título
        self.lbl_title = ttk.Label(self.frm_center, text='Código de Segurança', bootstyle='primary-inverse', padding=(96, 11))
        self.lbl_title.grid(column=0,row=0, columnspan=2, pady=(0,30))

        self.email = "jean.g******@ufac.br" # Implementar algoritmo de censura. 
                                            # Sugestão:
                                            # Pegar o texto antes do @, divida por 2, censure a segunda metade.
                                            # É altamente recomendado que a parte censurada tenha um tamanho fixo (4-6 asterísticos).
        self.lbl_info = ttk.Label(self.frm_center, text=f"Um código de segurança foi enviado para o email:\n{self.email}",  justify='center')
        self.lbl_info.grid(column=0, row=1, columnspan=2, pady=(0,30))

        self.lbl_codigo = ttk.Label(self.frm_center, text='CÓDIGO', bootstyle='inverse-secondary', 
                                                              borderwidth=7, 
                                                              padding=(39,0),
                                                              font=('TkDefaultFont', 10, 'bold'))
        self.lbl_codigo.grid(column=0, row=2, sticky='w', pady=(0,5))
        self.ent_codigo = ttk.StringVar()
        self.ent_codigo = ttk.Entry(self.frm_center, textvariable=self.ent_codigo)
        self.ent_codigo.grid(column=1, row=2, sticky='ew', pady=(0, 5))
        self.ent_codigo.bind('<KeyRelease>', self.validar_campos)
        self.utils.add_placeholder(self.ent_codigo,'XXXXXX')

        self.tempo_restante = 59
        self.lbl_tempo_restante = ttk.Label(self.frm_center, text="")
        self.lbl_tempo_restante.grid(column=0, row=3, columnspan=2, pady=(30,0))

        # Frame dos botões
        self.frm_buttons = ttk.Frame(self.frm_center)
        self.frm_buttons.grid(column=0, row=4, columnspan=2, pady=(10, 0))

        # Botão Solicitar novo código
        self.btn_solicitar = ttk.Button(self.frm_buttons, text='SOLICITAR NOVO CÓDIGO', bootstyle='warning', state='disabled')
        self.btn_solicitar.grid(column=0, row=0, columnspan=2, sticky='ew', pady=(0,45))
        self.btn_solicitar.bind('<ButtonRelease-1>', self.enviar_codigo)

        # Botão Cancelar 
        self.btn_cancel = ttk.Button(self.frm_buttons, text='CANCELAR', bootstyle='danger')
        self.btn_cancel.grid(column=0, row=1, padx=(0,5))
        self.btn_cancel.bind('<ButtonRelease-1>', self.cancelar)

        # Botão Continuar
        self.btn_continuar = ttk.Button(self.frm_buttons, text='CONTINUAR', bootstyle='success', state='disabled')
        self.btn_continuar.grid(column=1, row=1)
        self.btn_continuar.bind('<ButtonRelease-1>', self.continuar)

        self.enviar_codigo()

        self.utils.centraliza(self.janela)


    def enviar_codigo(self, *event):
        self.btn_solicitar.config(state='disabled')
        self.tempo_restante = 59
        self.lbl_tempo_restante.grid() # Garante que o label esteja visível
        self.atualizar_contador()

    def atualizar_contador(self):
        if self.tempo_restante > 0:
            self.lbl_tempo_restante.config(text=f"Solicite novamente em {self.tempo_restante} segundos.")
            self.tempo_restante -= 1
            self.janela.after(1000, self.atualizar_contador)
        else:
            self.lbl_tempo_restante.grid_remove() # Esconde o label
            self.btn_solicitar.config(state='enabled')

    def validar_campos(self, event):
        cpf = self.ent_codigo.get()
        if len(cpf) == 6:
            self.btn_continuar.config(state='enable')
        else:
            self.btn_continuar.config(state='disabled')

    def cancelar(self, event):
        pass

    def continuar(self, event):
        pass