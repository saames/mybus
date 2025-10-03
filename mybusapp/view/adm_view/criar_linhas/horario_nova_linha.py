import ttkbootstrap as ttk
from resources.utils import Utils
import datetime
from control.cadastra_linha_control import CadastrarLinhaControl


class HorarioNovaLinhaView:
    def __init__(self,master, janela_origem=None,linha=None):
        # Ajustes janela
        self.janela = master
        self.janela_origem = janela_origem
        #self.nome_linha = linha[0]
        #self.numero_linha = linha[1]
        #self.janela.geometry('700x550')

        self.linha = linha

        self.janela.title('Cronograma de Horarios - MyBus')
        self.janela.resizable(False,False)
        self.frm_center = ttk.Frame(self.janela)
        self.frm_center.grid(column=0, row=0, padx=10, pady=10)

        #Criando Instancias
        #self.utils = Utils()
        self.linha_control = CadastrarLinhaControl()

        # Botão Voltar
        #self.style = ttk.Style()
        #self.style.configure('large.TButton', font=('TkDefaultFont', 18, 'bold'))
        #self.btn_voltar = ttk.Button(self.frm_center, text='⬅', style='large.TButton',)
        #self.btn_voltar.grid(column=0, row=0)
        #self.btn_voltar.bind('<ButtonRelease-1>',self)


        # Título da janela
        self.lbl_titulo = ttk.Label(self.frm_center, 
                                    text=f'Definir Cronograma de horarios', 
                                    bootstyle='primary-inverse',
                                    padding=(100,11),
                                    anchor='center')
        self.lbl_titulo.grid(column=0, row=0, columnspan=2,pady=4,sticky='we')

        self.lbl_dia_util = ttk.Label(
                                    self.frm_center, 
                                    text='Intervalo Dias úteis', 
                                    bootstyle='inverse-secondary', 
                                    borderwidth=7, 
                                    padding=(5,0),
                                    width=20,
                                    anchor='center',
                                    font=('TkDefaultFont', 10, 'bold'))
        self.lbl_dia_util.grid(column=0, row=1, sticky='w', pady=(0,5))

        #combobox intervalo
        self.intervalo_d_util = ttk.StringVar()
        self.intervalo_d_n_util = ttk.StringVar()
        self.lista_intevalo = ['15','30','45']

        self.horarios_util = []
        self.cbx_intervalo_d_util = ttk.Combobox(self.frm_center,
                                     values=self.lista_intevalo, 
                                     textvariable=self.intervalo_d_util,
                                     state='readonly')
        self.cbx_intervalo_d_util.current(0)
        self.cbx_intervalo_d_util.grid(column=1,row=1)

        self.horarios_n_util = []
        self.lbl_dia_n_util = ttk.Label(
                                    self.frm_center, 
                                    text='Intervalo Dias Não úteis', 
                                    bootstyle='inverse-secondary', 
                                    borderwidth=7, 
                                    padding=(5,0),
                                    width=20,
                                    anchor='center',
                                    font=('TkDefaultFont', 10, 'bold'))
        self.lbl_dia_n_util.grid(column=0, row=2, sticky='w', pady=(0,5))

        self.cbx_intervalo_d_n_util = ttk.Combobox(self.frm_center,
                                     values=self.lista_intevalo, 
                                     textvariable=self.intervalo_d_n_util,
                                     state='readonly')
        self.cbx_intervalo_d_n_util.current(0)
        self.cbx_intervalo_d_n_util.grid(column=1,row=2)

        #botão gerar horarios
        self.btn_gerar = ttk.Button(self.frm_center,text='Gerar Horários',width=15)
        self.btn_gerar.grid(column=0,row=3,pady=4,sticky='w')
        self.btn_gerar.bind('<ButtonRelease-1>',self.gerar_horarios)


        # Tabela (cabeçalho + corpo)
        colunas = ['dutil', 'dnutil']
        self.tvw = ttk.Treeview(self.frm_center, height=8, columns=colunas, show='headings', selectmode='browse')
        self.tvw.heading('dutil', text='DIAS ÚTEIS')
        self.tvw.heading('dnutil', text='DIAS NÃO ÚTEIS')
        self.tvw.grid(column=0, row=4, columnspan=2, pady=6, sticky='w')
        # Alinha o campo com a coluna
        self.tvw.column('dutil', anchor='center',)
        self.tvw.column('dnutil', anchor='center',)

        # Configura cor para status
        self.tvw.tag_configure("geral", background="#002B5C")

        # Scrollbar da Tabela
        self.brl = ttk.Scrollbar(self.frm_center, command=self.tvw.yview)
        self.brl.grid(column=2, row=4, sticky='ns', pady=6)
        self.tvw.configure(yscrollcommand=self.brl.set)
        #botao voltar
        self.btn_cancelar = ttk.Button(self.frm_center,text='VOLTAR',bootstyle='secondary',width=15)
        self.btn_cancelar.grid(column=0,row=5)
        self.btn_cancelar.bind('<ButtonRelease-1>',self.voltar)

        #botao salvar linha
        self.btn_salvar = ttk.Button(self.frm_center,text='SALVAR LINHA',bootstyle='success',width=15)
        self.btn_salvar.grid(column=1,row=5)
        self.btn_salvar.bind('<ButtonRelease-1>',self.salvar_linha)

    def gerar_horarios(self, event):
        for item in self.tvw.get_children():
            self.tvw.delete(item)
        try:
            intervalo_util = int(self.cbx_intervalo_d_util.get())
        except ValueError:
            intervalo_util = 15

        try:
            intervalo_n_util = int(self.cbx_intervalo_d_n_util.get())
        except ValueError:
            intervalo_n_util = 15

        # Gera horários de 5:00 até 23:45 para cada coluna
        self.horarios_util = []
        hora_util = datetime.datetime.strptime("05:00", "%H:%M")
        fim = datetime.datetime.strptime("23:45", "%H:%M")
        while hora_util <= fim:
            self.horarios_util.append(hora_util.strftime("%H:%M"))
            hora_util += datetime.timedelta(minutes=intervalo_util)

        self.horarios_n_util = []
        hora_n_util = datetime.datetime.strptime("05:00", "%H:%M")
        while hora_n_util <= fim:
            self.horarios_n_util.append(hora_n_util.strftime("%H:%M"))
            hora_n_util += datetime.timedelta(minutes=intervalo_n_util)

        max_len = max(len(self.horarios_util), len(self.horarios_n_util))
        for i in range(max_len):
            h_util = self.horarios_util[i] if i < len(self.horarios_util) else ""
            h_n_util = self.horarios_n_util[i] if i < len(self.horarios_n_util) else ""
            self.tvw.insert('', 'end', values=(h_util, h_n_util))


    def salvar_linha(self, event):
        if(len(self.horarios_util) == 0 and len(self.horarios_n_util) == 0):
            self.gerar_horarios("")

        self.linha["horarios_util"] = self.horarios_util
        self.linha["horarios_n_util"] = self.horarios_n_util

        result = self.linha_control.inserir_linha(self.linha)

        if(result):
            self.janela.destroy()
            self.janela_origem.fechar_top_level()
    def voltar(self,event):
        self.janela.destroy() 