import ttkbootstrap as ttk
from resources.utils import Utils

class HorariosLinhaView:
    def __init__(self,master,janela_origem=None,linha=None):
        # Ajustes janela
        self.janela = master
        self.janela_origem = janela_origem
        self.nome_linha = linha[0]
        self.numero_linha = linha[1]
        #self.janela.geometry('700x550')
        self.janela.title('Horários - MyBus')
        self.janela.resizable(False,False)
        self.frm_center = ttk.Frame(self.janela)
        self.frm_center.grid(column=0, row=0, padx=10, pady=10)

        #Criando Instancias
        self.utils = Utils()

        # Botão Voltar
        self.style = ttk.Style()
        self.style.configure('large.TButton', font=('TkDefaultFont', 18, 'bold'))
        self.btn_voltar = ttk.Button(self.frm_center, text='⬅', style='large.TButton', command=self)
        self.btn_voltar.grid(column=0, row=0)
        self.btn_voltar.bind('<ButtonRelease-1>',self.voltar)

        # Título da janela
        self.lbl_titulo = ttk.Label(self.frm_center, text=f'Linha-{self.numero_linha} {self.nome_linha}', bootstyle='primary-inverse', width=46,padding=(0,11),anchor='center')
        self.lbl_titulo.grid(column=1, row=0, columnspan=2,pady=4)

        #tiulo treeview dia util
        self.lbl_treeview_dia_util = ttk.Label(self.frm_center,text='Dias Uteis',bootstyle='primary-inverse', padding=(0, 11),width=51,anchor='center')
        self.lbl_treeview_dia_util.grid(column=0,row=1,columnspan=3)

        # Tabela (cabeçalho + corpo)
        colunas = ['turb', 'tufac']
        self.tvw_dias_uteis = ttk.Treeview(self.frm_center, height=8, columns=colunas, show='headings', selectmode='browse')
        self.tvw_dias_uteis.heading('turb', text='TURB/SAIDA')
        self.tvw_dias_uteis.heading('tufac', text='TUFAC/SAIDA')
        self.tvw_dias_uteis.insert('', 'end', values=('5:00', '5:30',))
        self.tvw_dias_uteis.grid(column=0, row=2, columnspan=2, pady=6, sticky='we')
        # Alinha o campo com a coluna
        self.tvw_dias_uteis.column('turb', anchor='center',)
        self.tvw_dias_uteis.column('tufac', anchor='center',)

        # Configura cor para status
        self.tvw_dias_uteis.tag_configure("geral", background="#002B5C")

        # Scrollbar da Tabela
        self.brl_dias_uteis = ttk.Scrollbar(self.frm_center, command=self.tvw_dias_uteis.yview)
        self.brl_dias_uteis.grid(column=2, row=2, sticky='ns', pady=6)
        self.tvw_dias_uteis.configure(yscrollcommand=self.brl_dias_uteis.set)

        #tiulo treeview dia não util
        self.lbl_treeview_dia_n_util = ttk.Label(self.frm_center,text='Dias Não Úteis',bootstyle='primary-inverse', padding=(0, 11),width=51,anchor='center')
        self.lbl_treeview_dia_n_util.grid(column=0,row=3,columnspan=3)
        # Tabela (cabeçalho + corpo)
        colunas = ['turb', 'tufac']
        self.tvw_dias_n_uteis = ttk.Treeview(self.frm_center, height=8, columns=colunas, show='headings', selectmode='browse')
        self.tvw_dias_n_uteis.heading('turb', text='TURB/SAIDA')
        self.tvw_dias_n_uteis.heading('tufac', text='TUFAC/SAIDA')
        self.tvw_dias_n_uteis.insert('', 'end', values=('5:00', '6:00',))
        self.tvw_dias_n_uteis.grid(column=0, row=4, columnspan=2, pady=6, sticky='we')
        # Alinha o campo com a coluna
        self.tvw_dias_n_uteis.column('turb', anchor='center', )
        self.tvw_dias_n_uteis.column('tufac', anchor='center',)

        # Configura cor para status
        self.tvw_dias_n_uteis.tag_configure("geral", background="#002B5C")

        # Scrollbar da Tabela
        self.brl_dias_n_uteis = ttk.Scrollbar(self.frm_center, command=self.tvw_dias_n_uteis.yview)
        self.brl_dias_n_uteis.grid(column=2, row=4, sticky='ns', pady=6)
        self.tvw_dias_n_uteis.configure(yscrollcommand=self.brl_dias_n_uteis.set)

        # Comandos para navegação
        self.janela.bind('<Escape>', self.voltar)

        self.utils.centraliza(self.janela)
        
    def voltar(self, *event):
        self.janela.destroy() 
        self.janela_origem.deiconify()
    
    
    
    


        

