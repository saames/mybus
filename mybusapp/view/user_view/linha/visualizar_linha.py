import ttkbootstrap as ttk
from tkinter import messagebox
from resources.photos import Base64
from resources.utils import Utils
from control.gerenciar_linhas_control import GerenciarLinhasControl
from view.user_view.visualizar_rota.visualizar_rota_view import VisualizarRotaView

class VisualizarLinhaView:
    def __init__(self,master, janela_origem):
        # Ajustes janela
        self.janela_origem = janela_origem
        self.janela = master
        #self.janela.geometry('700x550')
        self.janela.title('Visualizar Linha - MyBus')
        self.janela.resizable(False,False)
        self.frm_center = ttk.Frame(self.janela)
        self.frm_center.grid(column=0, row=0, padx=10, pady=10)

        # Criação de Instâncias
        self.utils = Utils()
        self.gerenciar_linha = GerenciarLinhasControl()

        # Botão Voltar
        self.style = ttk.Style()
        self.style.configure('large.TButton', font=('TkDefaultFont', 18, 'bold'))
        self.btn_voltar = ttk.Button(self.frm_center, text='⬅', style='large.TButton', command=self.voltar)
        self.btn_voltar.grid(column=0, row=0)
        self.btn_voltar.bind('<ButtonRelease-1>')

        # Título da janela
        self.lbl_titulo = ttk.Label(self.frm_center, text='Visualizar Linhas', bootstyle='primary-inverse', padding=(134, 11))
        self.lbl_titulo.grid(column=1, row=0, columnspan=2)

        # Logo MyBus no canto superior esquerdo
        # self.img_logo = ttk.PhotoImage(data=Base64.myBusLogo128())
        # self.lbl_logo = ttk.Label(self.janela, image=self.img_logo)
        # self.lbl_logo.image = self.img_logo
        # self.lbl_logo.grid(row=0, column=0, padx=10, pady=10, sticky='ne')

        # Tabela (cabeçalho + corpo)
        colunas = ['nome', 'numero']
        self.tvw = ttk.Treeview(self.frm_center, height=8, columns=colunas, show='headings', selectmode='browse')
        self.tvw.heading('nome', text='NOME')
        self.tvw.heading('numero', text='NÚMERO')
        self.tvw.grid(column=0, row=1, columnspan=2, pady=6, sticky='we')
        # Alinha o campo com a coluna
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

        self.frm_botoes = ttk.Frame(self.frm_center)
        self.frm_botoes.grid(column=0, row=2, columnspan=2)

        # Botão Rota
        self.btn_rota = ttk.Button(self.frm_botoes, text="Rotas", bootstyle='primary', state='disabled')
        self.btn_rota.grid(row=0, column=0, padx=2)
        self.btn_rota.bind('<Button-1>', self.visualizar_rota)

        # Botão Horário
        self.btn_horario= ttk.Button(self.frm_botoes, text="Horários", bootstyle='primary', state='disabled')
        self.btn_horario.grid(row=0, column=1, padx=2)
        self.btn_horario.bind('<Button-1>')

        # Registrar Viagem
        self.btn_registrar_viagem = ttk.Button(self.frm_botoes, text="Registrar Viagem", bootstyle='secondary', state='disabled')
        self.btn_registrar_viagem.grid(row=0, column=2, padx=2)
        self.btn_registrar_viagem.bind('<Button-1>', self.RegistrarViagem)

        # Favoritar Linha
        self.btn_favoritar_linha = ttk.Button(self.frm_botoes, text="Favoritar Linha", bootstyle='secondary', state='disabled')
        self.btn_favoritar_linha.grid(row=0, column=3, padx=2)
        self.btn_favoritar_linha.bind('<Button-1>')

        # self.frm_center.grid_rowconfigure(0, weight=1)
        # self.frm_center.grid_columnconfigure(0, weight=1)

        self.utils.centraliza(self.janela)

    def validar_botoes(self, *event):
        linha = self.tvw.selection()
        if linha: # Se uma linha for selecionada
            self.btn_rota.config(state='enable')
            self.btn_horario.config(state='enable')
            self.btn_registrar_viagem.config(state='enable')
            self.btn_favoritar_linha.config(state='enable')
            return True
        else:
            self.btn_rota.config(state='disabled')
            self.btn_horario.config(state='disabled')
            self.btn_registrar_viagem.config(state='disabled')
            self.btn_favoritar_linha.config(state='disabled')
            return False

    def RegistrarViagem(self,event):
        self.item_selecionado = self.tvw.selection()
        if len(self.item_selecionado) != 1:
            messagebox.showerror('Erro', 'Selecione uma linha para favoritar.')
        elif len(self.item_selecionado) == 1:
            messagebox.askyesno('Confirmação','Confirma Registro de Viagem ?')

    def atualizar_tabela(self):
        dados = self.tvw.get_children()
        for item in dados:
            self.tvw.delete(item)
        tuplas = self.gerenciar_linha.listar_linhas()
        for item in tuplas:
            tag_geral = tuple()
            tag_geral = ('geral',)
            self.tvw.insert('', 'end', values=item[1:], tags=tag_geral)

    def visualizar_rota(self, event):
        item = self.tvw.selection()
        if item:
            linha = self.tvw.item(item)['values']
            self.tl = ttk.Toplevel(self.janela)
            VisualizarRotaView(self.tl, linha)
            self.utils.call_top_view(self.janela, self.tl)
        else:
            messagebox.showerror("Erro", "É necessário selecionar uma linha.")

    def voltar(self):
            self.janela.destroy() 
            self.janela_origem.deiconify() 