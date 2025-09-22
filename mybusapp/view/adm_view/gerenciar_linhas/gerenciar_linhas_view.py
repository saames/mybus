import ttkbootstrap as ttk
import tkintermapview as tkmap
from resources.utils import Utils
from control.gerenciar_linhas_control import GerenciarLinhasControl

class GerenciarLinhasView:
    def __init__(self, master):
        self.janela = master
        self.janela.title('Gerenciar Linhas - MyBus')
        #self.janela.geometry('700x500')
        #self.janela.resizable(False, False)
        self.frm_center = ttk.Frame(self.janela)
        self.frm_center.grid(column=0, row=0, padx=10, pady=10)

        # Criação de Instâncias
        self.utils = Utils()
        self.gerenciar_linhas_control = GerenciarLinhasControl()


        #Pegando

        # Botão voltar
        self.style = ttk.Style()
        self.style.configure('large.TButton', font=('TkDefaultFont', 18, 'bold'))
        self.btn_voltar = ttk.Button(self.frm_center, text='⬅', style='large.TButton')
        self.btn_voltar.grid(column=0, row=0)
        self.btn_voltar.bind('<ButtonRelease-1>')

        # Título da janela
        self.lbl_titulo = ttk.Label(self.frm_center, text='Gerenciar Linhas', bootstyle='primary-inverse', padding=(229, 11))
        self.lbl_titulo.grid(column=1, row=0, columnspan=2)

        # Tabela (cabeçalho + corpo)
        colunas = ['id', 'numero', 'nome']
        self.tvw = ttk.Treeview(self.frm_center, height=8, columns=colunas, show='headings')
        self.tvw.heading('id', text='ID')
        self.tvw.heading('numero', text='NÚMERO')
        self.tvw.heading('nome', text='NOME')
        self.tvw.grid(column=0, row=1, columnspan=2, pady=6, sticky='we')
        # Alinha o campo com a coluna
        self.tvw.column('id', anchor='center', width=200, minwidth=100)
        self.tvw.column('numero', anchor='center', width=200, minwidth=100)
        self.tvw.column('nome', anchor='center', width=200, minwidth=200)
        # Scrollbar da Tabela
        self.brl = ttk.Scrollbar(self.frm_center, command=self.tvw.yview)
        self.brl.grid(column=2, row=1, sticky='ns', pady=6)
        self.tvw.configure(yscrollcommand=self.brl.set)
        # Gerando tuplas
        self.atualizar_tabela()

        self.frm_menu = ttk.Frame(self.frm_center)
        self.frm_menu.grid(column=0, row=2, columnspan=3)

        self.btn_cadastrar = ttk.Button(self.frm_menu, text='Cadastrar', bootstyle='success')
        self.btn_cadastrar.grid(column=0, row=0, padx=2)
        self.btn_cadastrar.bind('<ButtonRelease-1>')

        self.btn_editar = ttk.Button(self.frm_menu, text='Editar', bootstyle='warning')
        self.btn_editar.grid(column=1, row=0, padx=2)
        self.btn_editar.bind('<ButtonRelease-1>')

        self.btn_excluir = ttk.Button(self.frm_menu, text='Excluir', bootstyle='danger')
        self.btn_excluir.grid(column=3, row=0, padx=2)
        self.btn_excluir.bind('<ButtonRelease-1>')

        self.lbl_espacador = ttk.Label(self.frm_menu)
        self.lbl_espacador.grid(column=4, row=0, padx=117)

        self.btn_horarios = ttk.Button(self.frm_menu, text='Horários', bootstyle='secondary')
        self.btn_horarios.grid(column=5, row=0, padx=2)
        self.btn_horarios.bind('<ButtonRelease-1>')

        self.btn_rotas = ttk.Button(self.frm_menu, text='Rotas', bootstyle='secondary')
        self.btn_rotas.grid(column=6, row=0, padx=2)
        self.btn_rotas.bind('<ButtonRelease-1>')

        self.utils.centraliza(self.janela)

    def atualizar_tabela(self):
        dados = self.tvw.get_children()
        for item in dados:
            self.tvw.delete(item)
        tuplas = self.gerenciar_linhas_control.listar_linhas()
        for item in tuplas:
            self.tvw.insert('', 'end', values=item)