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
        self.janela.geometry('700x550')
        self.janela.title('Visualizar Linha')
        self.janela.resizable(False,False)

        self.utils = Utils()

        self.style = ttk.Style()
        self.style.configure('large.TButton', font=('TkDefaultFont', 18, 'bold'))
        self.btn_voltar = ttk.Button(self.janela, text='⬅', style='large.TButton', command=self.voltar)
        self.btn_voltar.grid(column=0, row=0, sticky='wn',padx=20,pady=30)
        self.btn_voltar.bind('<ButtonRelease-1>')

        # Pegando as linha do banco de dados
        self.gerenciar_linha = GerenciarLinhasControl()

        # Logo MyBus no canto superior esquerdo
        self.img_logo = ttk.PhotoImage(data=Base64.myBusLogo128())
        self.lbl_logo = ttk.Label(self.janela, image=self.img_logo)
        self.lbl_logo.image = self.img_logo
        self.lbl_logo.grid(row=0, column=0, padx=10, pady=10, sticky='ne')


        # Frame centralizado com espaçamento
        self.frm_center = ttk.Frame(self.janela)
        self.frm_center.grid(row=2, column=0, padx=40, pady=50)

        colunas = ['id', 'nome', 'numero']
        self.tvw = ttk.Treeview(self.frm_center, height=5,
                                columns=colunas, show='headings')
        #Configurar o cabaçalho das colunas
        self.tvw.heading('id', text='ID')
        self.tvw.heading('numero', text='NÚMERO')
        self.tvw.heading('nome', text='NOME')
        self.tvw.grid(row=0, column=0,sticky='nsew')

        # Centralizar os valores das células
        self.tvw.column('id', anchor='center')
        self.tvw.column('numero', anchor='center')
        self.tvw.column('nome', anchor='center')

        self.tvw.grid(row=0, column=0, sticky='nsew')

        self.atualizar_tabela()

        self.brl = ttk.Scrollbar(self.frm_center, command=self.tvw.yview)
        self.brl.grid(row=0, column=1, sticky='ns')
        self.tvw.configure(yscrollcommand=self.brl.set)

        self.frm_botoes = ttk.Frame(self.janela)
        self.frm_botoes.grid(row=3, column=0,)

        self.btn_favoritar_linha = ttk.Button(self.frm_botoes, text="Favoritar Linha", bootstyle='primary',width=15)
        self.btn_favoritar_linha.grid(row=0,column=0,padx=10)
        self.btn_favoritar_linha.bind('<Button-1>', self)

        self.btn_horario= ttk.Button(self.frm_botoes, text="Horarios", bootstyle='primary',width=15)
        self.btn_horario.grid(row=0,column=1,padx=10)
        self.btn_horario.bind('<Button-1>', self)

        self.btn_registrar_viagem = ttk.Button(self.frm_botoes, text="Registrar Viagem", bootstyle='primary',width=15)
        self.btn_registrar_viagem.grid(row=0,column=2,padx=10)
        self.btn_registrar_viagem.bind('<Button-1>', self.RegistrarViagem)

        self.btn_rota = ttk.Button(self.frm_botoes, text="Rotas", bootstyle='primary',width=15)
        self.btn_rota.grid(row=0,column= 3,padx=10)
        self.btn_rota.bind('<Button-1>', self.visualizar_rota)

        self.frm_center.grid_rowconfigure(0, weight=1)
        self.frm_center.grid_columnconfigure(0, weight=1)

        self.utils.centraliza(self.janela)


    def RegistrarViagem(self,event):
        self.item_selecionado = self.tvw.selection()
        if len(self.item_selecionado) != 1:
            messagebox.showwarning('Aviso', 'Selecione um item')
        elif len(self.item_selecionado) == 1:
            messagebox.askyesno('Confirmação','Confirma Registro de Viagem ?')

    def atualizar_tabela(self):
        dados = self.tvw.get_children()
        for item in dados:
            self.tvw.delete(item)
        tuplas = self.gerenciar_linha.listar_linhas()
        for item in tuplas:
            self.tvw.insert('', 'end', values=item)

    def visualizar_rota(self, event):
        item = self.tvw.selection()
        if(item):
            linha = self.tvw.item(item)['values']
            self.tl = ttk.Toplevel(self.janela)
            VisualizarRotaView(self.tl, linha)
            self.utils.call_top_view(self.janela, self.tl)
        else:
            messagebox.showwarning("Error", "É necesserio selecionar uma linha.")

    def voltar(self):
            self.janela.destroy() 
            self.janela_origem.deiconify() 