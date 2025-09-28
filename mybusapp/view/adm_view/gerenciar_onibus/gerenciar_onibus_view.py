import ttkbootstrap as ttk
import tkintermapview as tkmap
from tkinter import messagebox
from control.gerenciar_onibus_control import GerenciarOnibusControl
from view.adm_view.onibus_forms.onibus_form import OnibusForm
from resources.utils import Utils


class GerenciarOnibusView:
    def __init__(self,master, janela_origem):
        self.janela = master
        self.janela_origem = janela_origem
        self.janela.title('Gerenciar Ônibus - MyBus')
        #self.janela.geometry('700x500')
        #self.janela.resizable(False, False)
        self.frm_center = ttk.Frame(self.janela)
        self.frm_center.grid(column=0, row=0, padx=10, pady=10)

        # Criação de Instâncias
        self.utils = Utils()
        self.ge_onibus = GerenciarOnibusControl()

        # Botão voltar
        self.style = ttk.Style()
        self.style.configure('large.TButton', font=('TkDefaultFont', 18, 'bold'))
        self.btn_voltar = ttk.Button(self.frm_center, text='⬅', style='large.TButton', command=self.voltar)
        self.btn_voltar.grid(column=0, row=0)
        self.btn_voltar.bind('<ButtonRelease-1>')

        # Título da janela
        self.lbl_titulo = ttk.Label(self.frm_center, text='Gerenciar Ônibus', bootstyle='primary-inverse', padding=(258, 11))
        self.lbl_titulo.grid(column=1, row=0, columnspan=2)

        # Tabela (cabeçalho + corpo)
        colunas = ['id', 'numero', 'placa', 'status', 'linha associada']
        self.tvw = ttk.Treeview(self.frm_center, height=8, columns=colunas, show='headings', selectmode='browse')
        self.tvw.heading('id', text='ID')
        self.tvw.heading('numero', text='NÚMERO')
        self.tvw.heading('placa', text='PLACA')
        self.tvw.heading('status', text='STATUS')
        self.tvw.heading('linha associada', text='LINHA ASSOCIADA')
        self.tvw.grid(column=0, row=1, columnspan=2, pady=6, sticky='we')

        # Alinha o campo com a coluna
        self.tvw.column('id', anchor='center', width=60, minwidth=60)
        self.tvw.column('numero', anchor='center', width=100, minwidth=100)
        self.tvw.column('placa', anchor='center', width=100, minwidth=100)
        self.tvw.column('status', anchor='center', width=100, minwidth=100)
        self.tvw.column('linha associada', anchor='center', width=300, minwidth=300)

        # Configura cor para status
        self.tvw.tag_configure("ativo", background="#002B5C")
        self.tvw.tag_configure("inativo", background="#001F44")

        # Scrollbar da Tabela
        self.brl = ttk.Scrollbar(self.frm_center, command=self.tvw.yview)
        self.brl.grid(column=2, row=1, sticky='ns', pady=6)
        self.tvw.configure(yscrollcommand=self.brl.set)

        # Gerando tuplas
        self.atualizar_tabela()

        # Verifica se existe uma linha selecionada
        self.tvw.bind('<KeyRelease>', self.validar_botoes)
        self.tvw.bind('<ButtonRelease-1>', self.validar_botoes)

        # Botões
        self.frm_menu = ttk.Frame(self.frm_center)
        self.frm_menu.grid(column=0, row=2, columnspan=3) 

        self.entr_busca_value = ttk.StringVar()
        self.entr_busca = ttk.Entry(self.frm_menu, textvariable=self.entr_busca_value)
        self.entr_busca.grid(column=0, row=0, columnspan=2, sticky='ew')
        self.btn_buscar = ttk.Button(self.frm_menu, text='Buscar')
        self.btn_buscar.bind('<ButtonRelease-1>', self.pesquisar_onibus)
        self.btn_buscar.grid(column=2, row=0, padx=(5, 0)) 

        self.btn_cadastrar = ttk.Button(self.frm_menu, text='Cadastrar', bootstyle='success')
        self.btn_cadastrar.grid(column=0, row=1, padx=2, pady=(10, 0), sticky='ew')
        self.btn_cadastrar.bind('<ButtonRelease-1>', self.abrir_cadastro_onibus)

        self.btn_editar = ttk.Button(self.frm_menu, text='Editar', bootstyle='warning', state='disabled')
        self.btn_editar.grid(column=1, row=1, padx=2, pady=(10, 0), sticky='ew')
        self.btn_editar.bind('<ButtonRelease-1>', self.abrir_editar_onibus)

        self.btn_excluir = ttk.Button(self.frm_menu, text='Excluir', bootstyle='danger', state='disabled')
        self.btn_excluir.grid(column=2, row=1, padx=2, pady=(10, 0), sticky='ew')
        self.btn_excluir.bind('<ButtonRelease-1>', self.excluir_onibus)

        self.utils.centraliza(self.janela)

    def validar_botoes(self, *event):
        linha = item = self.tvw.selection()
        if linha: # Se uma linha for selecionada
            self.btn_editar.config(state='enable')
            self.btn_excluir.config(state='enable')
            return True
        else:
            self.btn_editar.config(state='disabled')
            self.btn_excluir.config(state='disabled')
            return False

    def atualizar_tabela(self, tuplas=None):
        dados = self.tvw.get_children()
        for item in dados:
            self.tvw.delete(item)

        if(tuplas == None):
            tuplas = self.ge_onibus.listar_onibus()

        for item in tuplas:
            valores = list(item)  # Converte para lista
            tag_inativo = tuple()
            tag_ativo = tuple()

            if valores[3] == 1:  # Verificando os status, se for 1 é ativo, se for 0 é inativo
                valores[3] = 'Ativo'
                tag_ativo = ('ativo',)
            elif valores[3] == 0:
                valores[3] = 'Inativo'
                tag_inativo = ('inativo',)

            if valores[4] == None:  # Verificando se veio alguma linha
                valores[4] = 'Nenhuma linha associada'
            
            self.tvw.insert('', 'end', values=valores, tags=[tag_inativo, tag_ativo])

     # Abre a janela OnibusForm
    def abrir_cadastro_onibus(self, event):
        self.tl = ttk.Toplevel(self.janela)
        OnibusForm(self.tl)
        self.utils.call_top_view(self.janela, self.tl)
        self.atualizar_tabela()

    def abrir_editar_onibus(self, event):
        selection = self.tvw.selection()
        id = self.tvw.item(selection)['values'][0]
        result = self.ge_onibus.buscar_onibus(id)[0]
        self.tl = ttk.Toplevel(self.janela)
        OnibusForm(self.tl, result)
        self.utils.call_top_view(self.janela, self.tl)
        self.atualizar_tabela()

    def pesquisar_onibus(self, event):
        texto = self.entr_busca_value.get()
        result = self.ge_onibus.pesquisar_onibus(texto)
        self.atualizar_tabela(result)

    def excluir_onibus(self, event):
        selection = self.tvw.selection()
        onibus = self.tvw.item(selection)['values']
        id = onibus[0]
        confirmar = messagebox.askquestion(f"Excluir onibus {onibus[1]} - {onibus[4]}", f"Voce Deseja excluir o onibus {onibus[1]} - {onibus[4]}")
        if confirmar == "yes":
            result = self.ge_onibus.excluir_onibus(id)
            if(result):
                messagebox.showinfo("Informação", "Processo realizado com sucesso")
                self.atualizar_tabela()
                
    def voltar(self):
            self.janela.destroy() 
            self.janela_origem.deiconify() 
