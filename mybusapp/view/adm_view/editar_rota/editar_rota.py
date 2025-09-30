import ttkbootstrap as ttk
import tkintermapview as tkmap

class EditarRotaView:
    def __init__(self, master):
        self.janela = master
        self.janela.title('Editar Rota - MyBus')
        self.janela.resizable(False, False)
        self.frm_center = ttk.Frame(self.janela, padding=(20,20))
        self.frm_center.pack(fill='both', expand=True)

        # Título
        self.lbl_title = ttk.Label(self.frm_center, text='Editar Rota de ida',  bootstyle='primary', font=('TkDefaultFont', 14, 'bold'))
        self.lbl_title.grid(column=0, row=0, sticky='w', pady=(0, 15), columnspan=2)

        # Frame para os elementos a esquerda
        self.frm_esquerda = ttk.Frame(self.frm_center)
        self.frm_esquerda.grid( column=0, row=1, sticky='ns', padx=(0, 20))

        # Frame para a treeview
        self.frm_tree = ttk.Frame(self.frm_esquerda)
        self.frm_tree.pack(side='left', fill='both', expand=True)

        # Configurando a tree
        colunas = ['N°', 'Nome']
        self.tree = ttk.Treeview(self.frm_tree, columns=colunas, show='headings', height=12, selectmode='browse')
        self.tree.heading('N°', text='N°')
        self.tree.heading('Nome', text='NOME DO PONTO')
        self.tree.column('N°', anchor='center', width=40, minwidth=40)
        self.tree.column('Nome', anchor='center', width=250, minwidth=250)
        self.tree.tag_configure("geral", background="#002B5C", foreground="white")
        self.tree.pack(side='left', fill='both', expand=True)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.frm_tree, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side='right', fill='y')

        # Frame para os botões
        self.frm_botoes_lista = ttk.Frame(self.frm_esquerda)
        self.frm_botoes_lista.pack(side='left', fill='y', padx=(5, 0))

        # Botões
        self.btn_adicionar = ttk.Button(self.frm_botoes_lista, text="+", bootstyle='success')
        self.btn_adicionar.pack(side='top', pady=2)
        self.btn_editar = ttk.Button(self.frm_botoes_lista, text="..", bootstyle='warning')
        self.btn_editar.pack(side='top', pady=2)
        self.btn_remover = ttk.Button(self.frm_botoes_lista, text="X", bootstyle='danger')
        self.btn_remover.pack(side='top', pady=2)
        self.btn_subir = ttk.Button(self.frm_botoes_lista, text="▲", bootstyle='secondary')
        self.btn_subir.pack(side='top', pady=(20, 2)) 
        self.btn_descer = ttk.Button(self.frm_botoes_lista, text="▼",bootstyle='secondary' )
        self.btn_descer.pack(side='top', pady=2)

         # Frame para o mapa
        self.frm_mapa = ttk.Frame(self.frm_center)
        self.frm_mapa.grid(row=1, column=1, sticky='ns')

        # Mapa
        self.lbl_map_title = ttk.Label(self.frm_mapa, text="Pré-visualização da rota")
        self.lbl_map_title.pack(anchor='w', pady=(0, 5))

        self.mpv_rota = tkmap.TkinterMapView(self.frm_mapa, width=380, height=300)
        self.mpv_rota.set_position(-9.972802894375437, -67.82629104665347)
        self.mpv_rota.set_zoom(13)
        self.mpv_rota.pack()

        # traçar rota
        self.btn_tracar_rota = ttk.Button(self.frm_mapa, text="Traçar Rota")
        self.btn_tracar_rota.pack(fill='x', pady=(10, 0))

        # Rodape
        self.frm_rodape = ttk.Frame(self.frm_center)
        self.frm_rodape.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(20, 0))
        
        self.btn_voltar = ttk.Button(self.frm_rodape, text="Voltar", bootstyle='secondary')
        self.btn_voltar.pack(side='left')

        self.btn_continuar = ttk.Button(self.frm_rodape, text="Continuar", bootstyle='success')
        self.btn_continuar.pack(side='right')

        self.atualizar()
    def atualizar(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        exemplos = [
                (1, "UFAC"), (2, "BR-364"), (3, "Elisabeth Both Belem"),
                (4, "Avenida Ceará"), (5, "Terminal Urbano")
            ]
        for item in exemplos:
            self.tree.insert('', 'end', values=item, tags=('geral',))