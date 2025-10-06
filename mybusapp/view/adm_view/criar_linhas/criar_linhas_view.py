from tkinter import messagebox
import ttkbootstrap as ttk
from control.cadastra_linha_control import CadastrarLinhaControl
from view.adm_view.definir_origem_destino.definir_origem_destino import DefinirOrigemDestinoView
from resources.utils import Utils

class CriarLinhaView:
    def __init__(self, master, janela_origem, linha=None):
        self.janela = master
        #Pegando a linha para o editar
        self.linha = linha

        self.janela_origem = janela_origem
        if(self.linha):
            self.janela.title('Editar Linha - MyBus')
        else:
            self.janela.title('Criar Linha - MyBus')
        #self.janela.geometry('400x300')
        self.janela.resizable(False, False)
        self.frm_center = ttk.Frame(self.janela)
        self.frm_center.pack(expand=True, padx=10, pady=10)


        # Criação de Instâncias
        self.utils = Utils()
        self.gerenciar_linha = CadastrarLinhaControl()

        # Titulo
        if(self.linha):
            title_text = "Editar Linha"
        else:
            title_text = "Criar Linha"
        self.lbl_title = ttk.Label(self.frm_center, text=title_text, bootstyle='primary-inverse', padding=(156, 11))
        self.lbl_title.grid(column=0,row=0, columnspan=2, pady=(0,20))

        # Nome da rota
        self.lbl_name = ttk.Label(self.frm_center, text='Nome',bootstyle='inverse-secondary',
                                                                         borderwidth=7, 
                                                                         padding=(14,0),
                                                                         font=('TkDefaultFont', 10, 'bold'))
        self.lbl_name.grid(column=0, row=1, sticky='w', pady=(0,5))

        self.ent_name_value = ttk.StringVar()
        if(self.linha):
            self.ent_name_value.set(linha["nome"].split("#")[0])
        self.ent_name = ttk.Entry(self.frm_center, textvariable=self.ent_name_value)
        self.ent_name.grid(column=1, row=1, sticky='ew', ipadx=60, pady=(0,5))
        self.ent_name.bind('<KeyRelease>', self.validar_campos)

        # Número da rota
        self.lbl_number = ttk.Label(self.frm_center, text='Número',bootstyle='inverse-secondary', 
                                                                    borderwidth=7, 
                                                                    padding=(6,0),
                                                                    font=('TkDefaultFont', 10, 'bold'))
        self.lbl_number.grid(column=0, row=2, sticky='w', pady=(0,5))
        self.spb_number_value = ttk.IntVar(value=1)
        if(self.linha):
            self.spb_number_value.set(int(self.linha["numero"]))
        self.spb_number = ttk.Spinbox(self.frm_center, textvariable=self.spb_number_value, from_=1, to=999, format='%03.0f')
        self.spb_number.set(f"{self.spb_number_value.get():03d}") # Solução para o número começar com 3 casas antes da vírgula.
        self.spb_number.grid(column=1, row=2, sticky='ew', pady=(0, 5))
        self.spb_number.bind('<KeyRelease>', self.validar_campos)
        self.spb_number.bind('<ButtonRelease>', self.validar_campos)
        
        # Frame para os botões
        self.frm_menu = ttk.Frame(self.frm_center)
        self.frm_menu.grid(column=0, row=3, columnspan=2, pady=(25, 0))
        
        # Botão Cancelar
        self.btn_cancel = ttk.Button(self.frm_menu, text='CANCELAR', bootstyle='danger', command=self.cancelar)
        self.btn_cancel.grid(column=0, row=0, sticky='ew', padx=(0,5))
        self.btn_cancel.bind('<ButtonRelease-1>')

        # Botão Continuar
        self.btn_continue = ttk.Button(self.frm_menu, text='CONTINUAR', bootstyle='success', state='disabled', command=self.continuar)
        self.btn_continue.grid(column=1, row=0, sticky='ew')
        self.btn_continue.bind('<ButtonRelease-1>')

        # Comandos para navegação
        self.janela.bind('<Escape>', self.cancelar)

        self.utils.centraliza(self.janela)

        if(linha):
            self.validar_campos("")

    
    def validar_campos(self, event):
        nome = self.ent_name.get()
        numero = self.spb_number.get()
        if numero.isdigit() and len(numero)==3 and len(nome)>=4: # O nome deve ter tamanho >= 4 e o número deve ter 3 casas antes da vírgula.
            self.btn_continue.config(state='enable')
        else:
            self.btn_continue.config(state='disabled')
    
    def continuar(self):
        numero = self.spb_number.get()
        testar_n = int(numero)
        nome = self.ent_name.get()
        if self.gerenciar_linha.verificar_numero_existente(testar_n) and self.linha == None:
            messagebox.showerror("Erro de Validação", "O número informado já está cadastrado no sistema.")
            return
        if self.gerenciar_linha.verificar_nome_existente(nome) and self.linha == None:
            messagebox.showerror("Erro de Validação", "O nome informado já está cadastrado no sistema.")
            return
        if(not self.linha):
            self.linha = {}
        self.linha["nome"]=self.ent_name_value.get()
        self.linha["numero"]=self.spb_number_value.get()
        self.tl = ttk.Toplevel(self.janela)
        DefinirOrigemDestinoView(self.tl, self, self.linha)
        self.utils.call_top_view(self.janela, self.tl)
    
    def cancelar(self, *event):
        can = messagebox.askquestion('Cancelar cadastro', 'Deseja cancelar o processo de cadastro de linha?')
        if can == 'yes':
            self.janela.destroy()

    def fechar_top_level(self):
        self.janela.destroy()