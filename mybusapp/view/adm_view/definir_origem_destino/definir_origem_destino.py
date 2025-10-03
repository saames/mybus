from tkinter import messagebox
import ttkbootstrap as ttk
import tkintermapview as tkmap
from view.adm_view.editar_rota.editar_rota import EditarRotaView
from resources.utils import Utils
from tkinter import TclError

class DefinirOrigemDestinoView:
    def __init__(self, master, janela_origem, linha):
        self.janela = master
        self.janela_origem = janela_origem
        self.janela.title('Definir Rota - MyBus')
        self.janela.resizable(False, False)
        self.frm_center = ttk.Frame(self.janela, padding=(20,20))
        self.frm_center.pack(fill='both', expand=True)

        self.utils = Utils()
        self.frm_center.columnconfigure(0, weight=1, minsize=250)

        #Pegando as informações ja inserida da linha
        self.linha = linha

        # Título
        self.lbl_title = ttk.Label(self.frm_center, text='Definir Origem e Destino',  bootstyle='primary', font=('TkDefaultFont', 14, 'bold'))
        self.lbl_title.grid(column=0, row=0, sticky='w', pady=(0, 15), columnspan=2)

        # Origem
        self.lbl_origem = ttk.Label( self.frm_center,
                                        text='Origem',
                                        bootstyle='inverse-secondary',
                                        borderwidth=7,  
                                        padding=(5,0),
                                        font=('TkDefaultFont', 10, 'bold')
        )
        self.lbl_origem.grid(column=0, row=2, columnspan=2, sticky='we') 

        self.origem = ttk.StringVar()
        self.origem_id = None
        self.cbx_origem = ttk.Combobox(
            self.frm_center,
            textvariable=self.origem,
            state='readonly',
            width=30
        )
        self.cbx_origem.grid(column=0, row=3, columnspan=2, sticky='we', pady=(0, 2))  
        self.cbx_origem.bind('<<ComboboxSelected>>')

        # Destino
        self.lbl_destino = ttk.Label( self.frm_center,
                                            text='Destino',
                                            bootstyle='inverse-secondary',
                                            borderwidth=7,  
                                            padding=(5,0),
                                            font=('TkDefaultFont', 10, 'bold')
        )
        self.lbl_destino.grid(column=0, row=4, columnspan=2, sticky='we', pady=(0,0)) 

        self.destino = ttk.StringVar()
        self.destino_id = None
        self.cbx_destino = ttk.Combobox(
            self.frm_center,
            textvariable=self.destino,
            state='readonly',
            width=30
        )
        self.cbx_destino.grid(column=0, row=5, columnspan=2, sticky='we', pady=(0, 2))  
        self.carregar_pontos()
        self.cbx_destino.bind('<<ComboboxSelected>>')

        # Botão Buscar Localização
        self.btn_buscar = ttk.Button(self.frm_center, text='Buscar Localização', bootstyle='secondary', command=self.buscar_e_marcar_no_mapa)
        self.btn_buscar.grid(column=0, row=7, columnspan=2, sticky='e', pady=(20, 0), ipadx=5)

        # Mapa
        self.lbl_map = ttk.Label(self.frm_center, text='Pré-Visualização da Rota')
        self.lbl_map.grid(column=2, row=0, pady=(0,15), padx=(20,0))
        self.mpv_rota = tkmap.TkinterMapView(self.frm_center, width=380, height=300)
        self.mpv_rota.set_position(-9.972802894375437, -67.82629104665347)
        self.mpv_rota.set_zoom(13)
        self.mpv_rota.grid(column=2, row=1, rowspan=7, padx=(20,0))

        # Botão Voltar
        self.btn_voltar = ttk.Button(self.frm_center, text='Voltar', bootstyle='secondary',command=self.voltar)
        self.btn_voltar.grid(column=0, row=8, pady=(40,0), sticky='w')

        # Botão Salvar Pontos
        self.btn_salvar = ttk.Button(self.frm_center, text='Salvar Pontos', bootstyle='success', command=self.salvar_pontos)
        self.btn_salvar.grid(column=2, row=8, pady=(40,0), sticky='e')

        self.utils.centraliza(self.janela)

    def salvar_pontos(self):
        origem_nome = self.origem.get()
        destino_nome = self.destino.get()
        self.rota = []

        if origem_nome == "Selecione" or destino_nome == "Selecione":
            messagebox.showwarning("Aviso", "Selecione uma origem e um destino antes de salvar.")
            return
        origem = list(self.pontos.get(origem_nome))
        destino = list(self.pontos.get(destino_nome))
        origem.insert(0, origem_nome)
        destino.insert(0, destino_nome)
        origem = tuple(origem)
        destino = tuple(destino)
        self.rota.append(origem)
        self.rota.append(destino)
        self.linha["pontos_iniciais"]=self.rota

        self.tl = ttk.Toplevel(self.janela)
        EditarRotaView(self.tl, self, self.linha)
        self.utils.call_top_view(self.janela, self.tl)

            
    def buscar_e_marcar_no_mapa(self):
        self.mpv_rota.delete_all_marker()

        marcadores = []

        # Marca origem, se válida
        if hasattr(self, "origem_lat") and self.origem_lat is not None:
            lat = float(self.origem_lat)
            lon = float(self.origem_lon)
            nome = self.origem.get()
            self.mpv_rota.set_marker(lat, lon, text=nome)
            marcadores.append((lat, lon))

        # Marca destino, se válido
        if hasattr(self, "destino_lat") and self.destino_lat is not None:
            lat = float(self.destino_lat)
            lon = float(self.destino_lon)
            nome = self.destino.get()
            self.mpv_rota.set_marker(lat, lon, text=nome)
            marcadores.append((lat, lon))

        # Centraliza o mapa
        if marcadores:
            if len(marcadores) == 1:
                # Se só um ponto, centraliza nele
                lat, lon = marcadores[0]
                self.mpv_rota.set_position(lat, lon)
                self.mpv_rota.set_zoom(14)
            else:
                # Se dois pontos, centraliza no meio
                lat_media = sum(m[0] for m in marcadores) / len(marcadores)
                lon_media = sum(m[1] for m in marcadores) / len(marcadores)
                self.mpv_rota.set_position(lat_media, lon_media)
                self.mpv_rota.set_zoom(13)
        else:
            messagebox.showwarning("Aviso", "Selecione ao menos Origem ou Destino para marcar no mapa.")


    def voltar(self):
            self.janela.destroy() 
            self.janela_origem.deiconify()

    """
        nome: Terminal Urbano, latitude -9.972261086504293, longitude -67.80508215454091
        nome: Terminal de integração da UFAC, latitude -9.951996973380488, longitude -67.86377218887112
        nome: Terminal de Integração Adalberto Sena, latitude -9.933183185350993, longitude -67.82624716099492
        nome: Terminal De Integração Da Baixada, latitude -10.006097506472686, longitude -67.84569171741323
        nome: Terminal de Integração Cidade do Povo, latitude -10.015813456823548, longitude -67.75233354029393
    """ 
    def carregar_pontos(self):
        self.pontos = {
            "Terminal Urbano": (-9.972261086504293, -67.80508215454091),
            "Terminal de Integração da UFAC": (-9.951996973380488, -67.86377218887112),
            "Terminal de Integração Adalberto Sena": (-9.933183185350993, -67.82624716099492),
            "Terminal De Integração Da Baixada": (-10.006097506472686, -67.84569171741323),
            "Terminal de Integração Cidade do Povo": (-10.015813456823548, -67.75233354029393),
        }

        nomes = ["Selecione"] + list(self.pontos.keys())
        self.cbx_origem["values"] = nomes
        self.cbx_destino["values"] = nomes

        self.cbx_origem.current(0)
        self.cbx_destino.current(0)

        # Adiciona a lógica de exclusão
        self.cbx_origem.bind("<<ComboboxSelected>>", self.origem_selecionado)
        self.cbx_destino.bind("<<ComboboxSelected>>", self.destino_selecionado)



    def origem_selecionado(self, event=None):
        """
            Função que remove o item selecionado no outro combobox
        """
        escolhido = self.origem.get()
        if escolhido == "Selecione":
            self.origem_lat = None
            self.origem_lon = None
        else:
            ponto = self.pontos.get(escolhido)
            if ponto:
                self.origem_lat, self.origem_lon = ponto

        # Atualizar opções do destino removendo a origem selecionada
        nomes = ["Selecione"] + [nome for nome in self.pontos.keys() if nome != escolhido]
        self.cbx_destino["values"] = nomes
        if self.destino.get() == escolhido:  # se destino era o mesmo, resetar
            self.cbx_destino.current(0)
            self.destino_lat = None
            self.destino_lon = None

    def destino_selecionado(self, event=None):
            escolhido = self.destino.get()
            if escolhido == "Selecione":
                self.destino_lat = None
                self.destino_lon = None
            else:
                # Busca direta no dicionário
                ponto = self.pontos.get(escolhido)
                if ponto:
                    self.destino_lat, self.destino_lon = ponto

            # Mesma lógica para o combobox de origem
            nomes = ["Selecione"] + [nome for nome in self.pontos.keys() if nome != escolhido]
            self.cbx_origem["values"] = nomes
            if self.origem.get() == escolhido:  
                self.cbx_origem.current(0)
                self.origem_lat = None
                self.origem_lon = None

    def fechar_top_level(self):
        self.janela.destroy()
        self.janela_origem.fechar_top_level()