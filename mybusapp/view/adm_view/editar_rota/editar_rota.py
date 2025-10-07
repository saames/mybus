from tkinter.messagebox import showerror
from tkinter.messagebox import askyesno

import ttkbootstrap as ttk
import tkintermapview as tkmap
from resources.utils import Utils
from resources.osrm.osrm import OSRM
from view.adm_view.criar_linhas.horario_nova_linha import HorarioNovaLinhaView
from view.adm_view.definir_rota.definir_rota import DefinirRotaView

class EditarRotaView:
    def __init__(self, master, janela_origem, linha=None, sentido="ida", pontos_ida=None):
        self.janela = master
        self.janela_origem = janela_origem
        self.janela.title('Editar Rota - MyBus')
        self.janela.resizable(False, False)
        self.frm_center = ttk.Frame(self.janela, padding=(20,20))
        self.frm_center.pack(fill='both', expand=True)

        #Pegando as informações ja inseridas da linha
        self.linha = linha
        self.pontos_ida = pontos_ida

        #Instacia que conecta com a api
        self.osrm = OSRM()

        # Título
        self.sentido = sentido
        self.lbl_title = ttk.Label(self.frm_center, text=f'Editar Rota de {self.sentido}',  bootstyle='primary', font=('TkDefaultFont', 14, 'bold'))
        self.lbl_title.grid(column=0, row=0, sticky='w', pady=(0, 15), columnspan=2)

        self.utils = Utils()

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
        self.tree.column('Nome', anchor='center', width=400, minwidth=400)
        self.tree.tag_configure("geral", background="#002B5C", foreground="white")
        self.tree.pack(side='left', fill='both', expand=True)
        self.tree.bind('<ButtonRelease-1>', self.validar_botoes)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.frm_tree, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side='right', fill='y')

        # Frame para os botões
        self.frm_botoes_lista = ttk.Frame(self.frm_esquerda)
        self.frm_botoes_lista.pack(side='left', fill='y', padx=(5, 0))

        # Estilização para os botões
        style = ttk.Style()
        style.configure('Add.success.TButton', font=('TkDefaultFont', 15, 'bold'))
        style.configure('Edit.warning.TButton', font=('TkDefaultFont', 12, 'bold'))
        style.configure('Remove.danger.TButton', font=('TkDefaultFont', 15, 'bold'))
        style.configure('Move.secondary.TButton', font=('TkDefaultFont', 15, 'bold'))

        # Botões
        self.btn_adicionar = ttk.Button(self.frm_botoes_lista, text="+", style='Add.success.TButton')
        self.btn_adicionar.pack(side='top', pady=2)
        self.btn_adicionar.bind('<ButtonRelease-1>', self.adicionar_novo_ponto)
        self.btn_editar = ttk.Button(self.frm_botoes_lista, text="...", style='Edit.warning.TButton', state='disabled')
        self.btn_editar.pack(side='top', pady=2, ipady=2)
        self.btn_editar.bind('<ButtonRelease-1>', self.editar_ponto)
        self.btn_remover = ttk.Button(self.frm_botoes_lista, text="×", style='Remove.danger.TButton', state='disabled')
        self.btn_remover.pack(side='top', pady=2)
        self.btn_remover.bind('<ButtonRelease-1>', self.excluir_ponto)
        self.btn_subir = ttk.Button(self.frm_botoes_lista, text="▲", style='Move.secondary.TButton', state='disabled')
        self.btn_subir.pack(side='top', pady=(20, 2))
        self.btn_subir.bind('<ButtonRelease-1>', self.subir_ordem)
        self.btn_descer = ttk.Button(self.frm_botoes_lista, text="▼",style='Move.secondary.TButton', state='disabled')
        self.btn_descer.pack(side='top', pady=2)
        self.btn_descer.bind('<ButtonRelease-1>', self.descer_ordem)

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
        self.btn_tracar_rota.bind('<ButtonRelease-1>', self.tracar_rota)

        # Rodape
        self.frm_rodape = ttk.Frame(self.frm_center)
        self.frm_rodape.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(20, 0))
        
        self.btn_voltar = ttk.Button(self.frm_rodape, text="Voltar", bootstyle='secondary')
        self.btn_voltar.pack(side='left')
        self.btn_voltar.bind('<ButtonRelease-1>', self.voltar)

        self.btn_continuar = ttk.Button(self.frm_rodape, text="Continuar", bootstyle='success', state='disabled')
        self.btn_continuar.pack(side='right')
        self.btn_continuar.bind('<ButtonRelease-1>', self.verificar_continuar)


        if ("id" not in self.linha.keys()):
            if (self.pontos_ida):
                self.atualizar(self.pontos_ida)
            else:
                self.atualizar()
        else:
            if(sentido == "ida"):
                pontos_editar = self.linha["marcacao-ida"]
                self.pontos = [(x + 1, pontos_editar[x][0], pontos_editar[x][1], pontos_editar[x][2]) for x in
                               range(len(pontos_editar))]
                self.atualizar(self.pontos)
            else:
                pontos_editar = self.linha["marcacao-volta"]
                self.pontos = [(x + 1, pontos_editar[x][0], pontos_editar[x][1], pontos_editar[x][2]) for x in
                               range(len(pontos_editar))]
                self.atualizar(self.pontos)

        
        self.utils.centraliza(self.janela)

    def validar_botoes(self, *event):
        linha = self.tree.selection()
        if linha:
            item = self.tree.item(linha[0])["values"]
            #print(item[0]) # Debug
            if item[0] in (1, len(self.pontos)):
                self.btn_editar.config(state='disabled')
                self.btn_remover.config(state='disabled')
                self.btn_subir.config(state='disabled')
                self.btn_descer.config(state='disabled')
            else:
                self.btn_editar.config(state='enable')
                self.btn_remover.config(state='enable')
                if item[0] != 2:
                    self.btn_subir.config(state='enable')
                else:
                    self.btn_subir.config(state='disabled')
                if item[0] != len(self.pontos)-1:
                    self.btn_descer.config(state='enable')
                else:
                    self.btn_descer.config(state='disabled')
                    


    def atualizar(self, pontos = None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.mpv_rota.delete_all_path()
        self.mpv_rota.delete_all_marker()

        if(pontos == None):
            pontos_iniciais = self.linha["pontos_iniciais"]
            self.pontos = [(x + 1, pontos_iniciais[x][0], pontos_iniciais[x][1], pontos_iniciais[x][2]) for x in range(len(pontos_iniciais))]
        else:
            self.pontos = pontos

        id_treeview = 0
        for item in range(len(self.pontos)):
            id_treeview += 1
            if(pontos):
                ponto_mod = list(self.pontos[item])
                ponto_mod[0] = id_treeview
                self.pontos[item] = ponto_mod
            self.tree.insert('', 'end', values=self.pontos[item], tags=('geral',), iid=id_treeview)

    def verificar_continuar(self, event):
        if str(self.btn_continuar['state']) == 'disabled':
            showerror("Ação necessária", "Trace uma rota antes de continuar.")
            return
        self.abrir_proxima_tela(event)


    def abrir_proxima_tela(self, event):
        if (self.sentido == "ida" and "rota-ida" not in self.linha) or (self.sentido == "volta" and "rota-volta" not in self.linha):
            showerror("Ação Necessária", "Trace uma rota antes de avançar.")
            return
        if(self.sentido == "ida"):
            if "rota-ida" not in (self.linha.keys()):
                self.tracar_rota("")
            if(len(self.pontos) > 2):
                if "id" not in self.linha.keys():
                    response = askyesno("Menssagem",
                                        "Você gostaria de definir a rota de retorno como o inverso da rota de ida?")
                    if (response):
                        self.tl = ttk.Toplevel(self.janela)
                        pontos_tela_volta = self.pontos[::-1]
                        EditarRotaView(self.tl, self, self.linha, sentido="volta", pontos_ida=pontos_tela_volta)
                        self.utils.call_top_view(self.janela, self.tl)
                    else:
                        self.tl = ttk.Toplevel(self.janela)
                        pontos_tela_volta = [self.pontos[len(self.pontos)-1], self.pontos[0]]
                        EditarRotaView(self.tl, self, self.linha, sentido="volta", pontos_ida=pontos_tela_volta)
                        self.utils.call_top_view(self.janela, self.tl)
                else:
                    self.tl = ttk.Toplevel(self.janela)
                    EditarRotaView(self.tl, self, self.linha, sentido="volta")
                    self.utils.call_top_view(self.janela, self.tl)
            else:
                self.tl = ttk.Toplevel(self.janela)
                pontos_tela_volta = [self.pontos[len(self.pontos) - 1], self.pontos[0]]
                EditarRotaView(self.tl, self, self.linha, sentido="volta", pontos_ida=pontos_tela_volta)
                self.utils.call_top_view(self.janela, self.tl)
        else:
            self.tl = ttk.Toplevel(self.janela)
            if "rota-volta" not in (self.linha.keys()):
                self.tracar_rota("")
            HorarioNovaLinhaView(self.tl, self, self.linha)
            self.utils.call_top_view(self.janela, self.tl)

    def fechar_top_level(self):
        self.janela.destroy()
        self.janela_origem.fechar_top_level()

    def tracar_rota(self, event):
        pontos_coordenadas = [(x[3], x[2]) for x in self.pontos]
        result = self.osrm.gerar_rota(pontos_coordenadas)
        for i in self.pontos:
            self.mpv_rota.set_marker(i[2], i[3], i[1])
        if(self.sentido == "ida"):
            self.linha["rota-ida"] = result
            self.linha["marcacao-ida"] = self.pontos
            self.mpv_rota.set_path(result, color="#0B67CD", width=5)
        else:
            self.linha["rota-volta"] = result
            self.linha["marcacao-volta"] = self.pontos
            self.mpv_rota.set_path(result, color="red", width=4)
        self.btn_continuar.config(state='normal')    

    def adicionar_novo_ponto(self, event):
        self.tl = ttk.Toplevel()
        DefinirRotaView(self.tl, self)
        self.utils.call_top_view(self.janela, self.tl)

    def editar_ponto(self, event):
        linha = self.tree.selection()

        if(len(linha)):
            item = self.tree.item(linha[0])["values"]
            if(item[0] not in (1, len(self.pontos))):
                self.tl = ttk.Toplevel()
                DefinirRotaView(self.tl, self, item)
                self.utils.call_top_view(self.janela, self.tl)
            else:
                showerror("Error", "A edição do ponto de origem/destino não é permitida. Para realizar essa ação, retorne à tela anterior.")
        else:
            showerror("Error",
                      "Escolha um ponto intermediário para editar.")

    def adicionar_ponto_na_lista(self, ponto):
        ultima_ponto = list(self.pontos[len(self.pontos) - 1])
        ultima_ponto[0] = ultima_ponto[0] + 1
        ultima_ponto = tuple(ultima_ponto)
        self.pontos[len(self.pontos) - 1] = ultima_ponto
        ponto = list(ponto)
        ponto.insert(0, ultima_ponto[0]-1)
        ponto = tuple(ponto)
        self.pontos.insert(ponto[0]-1, ponto)
        self.atualizar(self.pontos)
        self.btn_continuar.config(state='disabled')

    def adicionar_ponto_editado(self, ponto):
        self.pontos[ponto[0]-1] = ponto
        self.atualizar(self.pontos)
        self.btn_continuar.config(state='disabled')

    def excluir_ponto(self, event):
        linha = self.tree.selection()
        if (len(linha)):
            item = self.tree.item(linha[0])["values"]
            if (item[0] not in (1, len(self.pontos))):
                response = askyesno("Excluir", f"Deseja excluir o ponto: {item[0]}. {item[1]}")
                if(response):
                    self.pontos.pop(item[0]-1)
                    self.atualizar(self.pontos)
                    self.btn_continuar.config(state='disabled')
            else:
                showerror("Error",
                          "A exclusão do ponto de origem/destino não é permitida. Para realizar essa ação, retorne à tela anterior.")
        else:
            showerror("Error",
                      "Escolha um ponto intermediário para Excluir.")

    def subir_ordem(self, event):
        linha = self.tree.selection()
        if (len(linha)):
            item = self.tree.item(linha[0])["values"]
            if item[0] == 2:
                showerror("Error",
                          "A alteração de posição do ponto de origem/destino não é permitida. Para realizar essa ação, retorne à tela anterior.")
                return
            if (item[0]-1 > 1 and item[0] not in (1, len(self.pontos))):
                item_lista = list(self.pontos.pop(item[0]-1))
                self.pontos.insert(item_lista[0] - 2, item_lista)
                self.atualizar(self.pontos)
                self.tree.selection_set([f'{item_lista[0]-1}'])
                self.btn_continuar.config(state='disabled')
            else:
                if(item[0] in (1, len(self.pontos))):
                    showerror("Error",
                          "A alteração de posição do ponto de origem/destino não é permitida. Para realizar essa ação, retorne à tela anterior.")
        else:
            showerror("Error",
                      "Escolha um ponto intermediário para alterar sua posição.")
        self.validar_botoes()

    def descer_ordem(self, event):
        linha = self.tree.selection()
        if (len(linha)):
            item = self.tree.item(linha[0])["values"]
            if item[0] == len(self.pontos)-1:
                showerror("Error",
                          "A alteração de posição do ponto de origem/destino não é permitida. Para realizar essa ação, retorne à tela anterior.")
                return
            if (item[0]+1 < len(self.pontos) and item[0] not in (1, len(self.pontos))):
                item_lista = list(self.pontos.pop(item[0] - 1))
                self.pontos.insert(item_lista[0], item_lista)
                self.atualizar(self.pontos)
                self.tree.selection_set([f"{item_lista[0]+1}"])
                self.btn_continuar.config(state='disabled')
            else:
                if (item[0] in (1, len(self.pontos))):
                    showerror("Error",
                              "A alteração de posição do ponto de origem/destino não é permitida. Para realizar essa ação, retorne à tela anterior.")
        else:
            showerror("Error",
                      "Escolha um ponto intermediário para alterar sua posição (não é possível alterar a origem ou o destino).")
        self.validar_botoes()

    def voltar(self, *event):
        self.janela.destroy()
