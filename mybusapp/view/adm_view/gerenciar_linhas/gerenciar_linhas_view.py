import ttkbootstrap as ttk
import tkintermapview as tkmap
from tkinter import messagebox
from resources.utils import Utils
from control.gerenciar_linhas_control import GerenciarLinhasControl
from view.adm_view.criar_linhas.criar_linhas_view import CriarLinhaView
from view.user_view.linha.horarios_linha import HorariosLinhaView
from view.user_view.visualizar_rota.visualizar_rota_view import VisualizarRotaView

class GerenciarLinhasView:
    def __init__(self, master, janela_origem):
        self.janela = master
        self.janela_origem = janela_origem
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
        self.btn_voltar = ttk.Button(self.frm_center, text='⬅', style='large.TButton', command=self.voltar)
        self.btn_voltar.grid(column=0, row=0)
        self.btn_voltar.bind('<ButtonRelease-1>')

        # Título da janela
        self.lbl_titulo = ttk.Label(self.frm_center, text='Gerenciar Linhas', bootstyle='primary-inverse', padding=(159, 11))
        self.lbl_titulo.grid(column=1, row=0, columnspan=2)

        # Tabela (cabeçalho + corpo)
        colunas = ['id', 'nome', 'numero']
        self.tvw = ttk.Treeview(self.frm_center, height=8, columns=colunas, show='headings', selectmode='browse')
        self.tvw.heading('id', text='ID')
        self.tvw.heading('nome', text='NOME')
        self.tvw.heading('numero', text='NÚMERO')
        self.tvw.grid(column=0, row=1, columnspan=2, pady=6, sticky='we')
        # Alinha o campo com a coluna
        self.tvw.column('id', anchor='center', width=60, minwidth=60)
        self.tvw.column('nome', anchor='center', width=300, minwidth=300)
        self.tvw.column('numero', anchor='center', width=100, minwidth=100)

        # Configura cor para status
        self.tvw.tag_configure("geral", background="#002B5C")

        # Scrollbar da Tabela
        self.brl = ttk.Scrollbar(self.frm_center, command=self.tvw.yview)
        self.brl.grid(column=2, row=1, sticky='ns', pady=6)
        self.tvw.configure(yscrollcommand=self.brl.set)
        # Gerando tuplas
        self.atualizar_tabela()

        # Verifica se existe uma linha selecionada
        self.tvw.bind('<KeyRelease>', self.validar_botoes)
        self.tvw.bind('<ButtonRelease-1>', self.validar_botoes)

        self.frm_menu = ttk.Frame(self.frm_center)
        self.frm_menu.grid(column=0, row=2, columnspan=2)

        self.btn_cadastrar = ttk.Button(self.frm_menu, text='Cadastrar', bootstyle='success')
        self.btn_cadastrar.grid(column=0, row=0, padx=2)
        self.btn_cadastrar.bind('<ButtonRelease-1>', self.criar_linha)

        self.btn_editar = ttk.Button(self.frm_menu, text='Editar', bootstyle='warning', state='disabled')
        self.btn_editar.grid(column=1, row=0, padx=2)
        self.btn_editar.bind('<ButtonRelease-1>')

        self.btn_excluir = ttk.Button(self.frm_menu, text='Excluir', bootstyle='danger', state='disabled')
        self.btn_excluir.grid(column=3, row=0, padx=2)
        self.btn_excluir.bind('<ButtonRelease-1>', self.deletar_linha)

        #self.lbl_espacador = ttk.Label(self.frm_menu)
        #self.lbl_espacador.grid(column=4, row=0, padx=117)

        self.btn_horarios = ttk.Button(self.frm_menu, text='Horários', bootstyle='secondary', state='disabled')
        self.btn_horarios.grid(column=5, row=0, padx=2)
        self.btn_horarios.bind('<ButtonRelease-1>', self.visualizar_horario)

        self.btn_rotas = ttk.Button(self.frm_menu, text='Rotas', bootstyle='secondary', state='disabled')
        self.btn_rotas.grid(column=6, row=0, padx=2)
        self.btn_rotas.bind('<ButtonRelease-1>', self.visualizar_rota)

        # Comandos de navegação
        self.janela.bind('<Escape>', self.voltar)

        self.utils.centraliza(self.janela)

    def validar_botoes(self, *event):
        linha = item = self.tvw.selection()
        if linha: # Se uma linha for selecionada
            self.btn_editar.config(state='enable')
            self.btn_excluir.config(state='enable')
            self.btn_horarios.config(state='enable')
            self.btn_rotas.config(state='enable')
            return True
        else:
            self.btn_editar.config(state='disabled')
            self.btn_excluir.config(state='disabled')
            self.btn_horarios.config(state='disabled')
            self.btn_rotas.config(state='disabled')
            return False

    def atualizar_tabela(self):
        dados = self.tvw.get_children()
        for item in dados:
            self.tvw.delete(item)
        tuplas = self.gerenciar_linhas_control.listar_linhas()
        for i in range(len(tuplas)):
            linha = list(tuplas[i])
            linha[1] = linha[1].split("#")[0]
            tuplas[i] = linha
        for item in tuplas:
            tag_geral = tuple()
            tag_geral = ('geral',)
            self.tvw.insert('', 'end', values=item, tags=tag_geral)

    def criar_linha(self, event):
        self.tl = ttk.Toplevel(self.janela)
        CriarLinhaView(self.tl, self.janela_origem)
        self.utils.call_top_view(self.janela, self.tl)
        self.atualizar_tabela()

    def voltar(self, event=None):
            self.janela.destroy() 
            self.janela_origem.deiconify()

    def visualizar_rota(self, event):
        item = self.tvw.selection()
        if item:
            linha = self.tvw.item(item)['values']
            self.tl = ttk.Toplevel(self.janela)
            VisualizarRotaView(self.tl, linha)
            self.utils.call_top_view(self.janela, self.tl)
        else:
            messagebox.showerror("Erro", "É necessário selecionar uma linha.")

    def visualizar_horario(self,event):
        item = self.tvw.selection()
        if item:
            linha = list(self.tvw.item(item)['values'])
            self.tl = ttk.Toplevel(self.janela)
            HorariosLinhaView(self.tl,self.janela,linha)
            self.utils.call_top_view(self.janela,self.tl)
        else:
            messagebox.showerror("Erro", "É necessário selecionar uma linha.")

    def deletar_linha(self, event):
        item = self.tvw.selection()
        if item:
            linha = list(self.tvw.item(item)['values'])
            response = messagebox.askyesno("Mensagem", f"Voce deseja exluir a linha {linha[2]}.{linha[1]}?")
            if(response):
                self.gerenciar_linhas_control.delete_linha(linha[0])
                self.atualizar_tabela()
        else:
            messagebox.showerror("Erro", "É necessário selecionar uma linha.")
