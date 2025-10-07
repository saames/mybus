import ttkbootstrap as ttk
from resources.utils import Utils
from control.cronograma_control import CronogramaControl
from control.gerenciar_linhas_control import GerenciarLinhasControl

class HorariosLinhaView:
    def __init__(self,master,janela_origem=None,linha=None):
        # Ajustes janela
        self.janela = master
        self.janela_origem = janela_origem
        #self.janela.geometry('700x550')
        self.janela.title('Horários - MyBus')
        self.janela.resizable(False,False)
        self.frm_center = ttk.Frame(self.janela)
        self.frm_center.grid(column=0, row=0, padx=10, pady=10)



        #Criando Instancias
        self.utils = Utils()
        self.con_control = CronogramaControl()
        self.linha_control = GerenciarLinhasControl()

        #pegando as informações da linha
        self.linha_id = linha[0]
        linha_bd = self.linha_control.find_linha(self.linha_id)
        self.nome_completo_não_formatado = linha_bd[0][1].split("#")
        self.nome_origem_destino = self.nome_completo_não_formatado[1].split("-")
        self.nome_origem = self.nome_origem_destino[0].strip()
        self.nome_destino = self.nome_origem_destino[1].strip()
        self.numero_linha = linha[2]
        self.nome_linha = linha[1]

        #Pegando os horarios
        horarios = self.con_control.listar_cronograma(linha[0])
        self.horarios_dias_util = horarios[0]
        self.horarios_dias_n_util = horarios[1]

        # Botão Voltar
        self.style = ttk.Style()
        self.style.configure('large.TButton', font=('TkDefaultFont', 18, 'bold'))
        self.btn_voltar = ttk.Button(self.frm_center, text='⬅', style='large.TButton', command=self)
        self.btn_voltar.grid(column=0, row=0)
        self.btn_voltar.bind('<ButtonRelease-1>',self.voltar)

        # Título da janela
        self.lbl_titulo = ttk.Label(self.frm_center, text=f'Linha-{self.numero_linha} {self.nome_linha}', bootstyle='primary-inverse', width=65,padding=(0,11),anchor='center')
        self.lbl_titulo.grid(column=1, row=0, columnspan=3,pady=4)

        #tiulo treeview dia util
        self.lbl_treeview_dia_util = ttk.Label(self.frm_center,text='Dias Uteis',bootstyle='primary-inverse', padding=(2, 11),width=70,anchor='center')
        self.lbl_treeview_dia_util.grid(column=0,row=1,columnspan=4)

        # Tabela (cabeçalho + corpo)
        colunas = ['turb', 'tufac']
        self.tvw_dias_uteis = ttk.Treeview(self.frm_center, height=8, columns=colunas, show='headings', selectmode='browse')
        self.tvw_dias_uteis.heading('turb', text=f'{self.nome_origem}/SAIDA')
        self.tvw_dias_uteis.heading('tufac', text=f'{self.nome_destino}/SAIDA')
        for item in self.horarios_dias_util:
            self.tvw_dias_uteis.insert('', 'end', values=item)
        self.tvw_dias_uteis.grid(column=0, row=2, columnspan=3, pady=6, sticky='we')
        # Alinha o campo com a coluna
        self.tvw_dias_uteis.column('turb', anchor='center', width=276, minwidth=200)
        self.tvw_dias_uteis.column('tufac', anchor='center', width=276, minwidth=200)

        # Configura cor para status
        self.tvw_dias_uteis.tag_configure("geral", background="#002B5C")

        # Scrollbar da Tabela
        self.brl_dias_uteis = ttk.Scrollbar(self.frm_center, command=self.tvw_dias_uteis.yview)
        self.brl_dias_uteis.grid(column=3, row=2, sticky='ns', pady=6)
        self.tvw_dias_uteis.configure(yscrollcommand=self.brl_dias_uteis.set)

        #tiulo treeview dia não util
        self.lbl_treeview_dia_n_util = ttk.Label(self.frm_center,text='Dias Não Úteis',bootstyle='primary-inverse', padding=(2, 11),width=70,anchor='center')
        self.lbl_treeview_dia_n_util.grid(column=0,row=3,columnspan=4)
        # Tabela (cabeçalho + corpo)
        colunas = ['turb', 'tufac']
        self.tvw_dias_n_uteis = ttk.Treeview(self.frm_center, height=8, columns=colunas, show='headings', selectmode='browse')
        self.tvw_dias_n_uteis.heading('turb', text=f'{self.nome_origem}/SAIDA')
        self.tvw_dias_n_uteis.heading('tufac', text=f'{self.nome_destino}/SAIDA')
        for item in self.horarios_dias_n_util:
            self.tvw_dias_n_uteis.insert('', 'end', values=item)
        self.tvw_dias_n_uteis.grid(column=0, row=4, columnspan=3, pady=6, sticky='we')
        # Alinha o campo com a coluna
        self.tvw_dias_n_uteis.column('turb', anchor='center', width=276, minwidth=200)
        self.tvw_dias_n_uteis.column('tufac', anchor='center', width=276, minwidth=200)

        # Configura cor para status
        self.tvw_dias_n_uteis.tag_configure("geral", background="#002B5C")

        # Scrollbar da Tabela
        self.brl_dias_n_uteis = ttk.Scrollbar(self.frm_center, command=self.tvw_dias_n_uteis.yview)
        self.brl_dias_n_uteis.grid(column=3, row=4, sticky='ns', pady=6)
        self.tvw_dias_n_uteis.configure(yscrollcommand=self.brl_dias_n_uteis.set)

        # Comandos para navegação
        self.janela.bind('<Escape>', self.voltar)

        self.utils.centraliza(self.janela)
        
    def voltar(self, *event):
        self.janela.destroy() 
        self.janela_origem.deiconify()
    
    
    
    


        

