from tkinter import messagebox
import ttkbootstrap as ttk
import tkintermapview as tkmap
from resources.utils import Utils
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError



class DefinirRotaView:
    def __init__(self, master, janela_origem):
        self.janela = master
        self.janela_origem = janela_origem
        self.janela.title('Definir Rota - MyBus')
        self.janela.resizable(False, False)
        self.frm_center = ttk.Frame(self.janela, padding=(20,20))
        self.frm_center.pack(fill='both', expand=True)

        self.utils = Utils()

        # Variáveis para armazenar os dados da rota
        self.ponto_origem = None
        self.ponto_destino = None

        # Título
        self.lbl_title = ttk.Label(self.frm_center, text='Definir Rota de ida',  bootstyle='primary', font=('TkDefaultFont', 14, 'bold'))
        self.lbl_title.grid(column=0, row=0, sticky='w', pady=(0, 15), columnspan=2)

        # Origem
        self.lbl_origem = ttk.Label(self.frm_center, text='Origem', bootstyle='secondary-inverse')
        self.lbl_origem.grid(column=0, row=3, columnspan=2, sticky='we', ipady=5)
        self.ent_origem = ttk.Entry(self.frm_center, bootstyle='primary')
        self.ent_origem.grid(column=0, row=4, columnspan=2, sticky='we', pady=(0,20))

        # Destino (escondido no início)
        self.lbl_destino = ttk.Label(self.frm_center, text='Destino', bootstyle='secondary-inverse')
        self.lbl_destino.grid(column=0, row=3, columnspan=2, sticky='we', ipady=5)
        self.ent_destino = ttk.Entry(self.frm_center, bootstyle='primary')
        self.ent_destino.grid(column=0, row=4, columnspan=2, sticky='we', pady=(0, 20))
        # Escondemos os widgets de destino
        self.lbl_destino.grid_remove()
        self.ent_destino.grid_remove()

        # Longitude
        self.lbl_longitude = ttk.Label(self.frm_center, text=' Longitude', bootstyle='secondary-inverse')
        self.lbl_longitude.grid(column=0, row=5, sticky='we', ipady=5)
        self.ent_longitude = ttk.Entry(self.frm_center, bootstyle='primary')
        self.ent_longitude.grid(column=0, row=6, sticky='we', padx=(0, 5))

        # Latitude
        self.lbl_latitude = ttk.Label(self.frm_center, text=' Latitude', bootstyle='secondary-inverse')
        self.lbl_latitude.grid(column=1, row=5, sticky='we', ipady=5)
        self.ent_latitude = ttk.Entry(self.frm_center, bootstyle='primary')
        self.ent_latitude.grid(column=1, row=6, sticky='we', padx=(5, 0))

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

        # Botão Salvar Origem/Salvar
        self.btn_continuar = ttk.Button(self.frm_center, text='Salvar Origem', bootstyle='success', command=self.proxima_etapa)
        self.btn_continuar.grid(column=2, row=8, pady=(40,0), sticky='e')

        self.utils.centraliza(self.janela)

    def proxima_etapa(self):
        """
        Define o estado atual da janela de acordo com qual botão está.
        Se estiver em "Salvar Origem", será definido a Origem, deixando oculto a entry do Destino.
        Se estiver em "Salvar Rota", será definido o Destino
        """
        # Se o botão ainda diz "Salvar Origem", estamos definindo a origem.
        if self.btn_continuar.cget('text') == 'Salvar Origem':
            origem_texto = self.ent_origem.get()
            if not origem_texto:
                messagebox.showwarning("Campo Vazio", "Por favor, preencha a origem antes de continuar.")
                return
            
            self.ponto_origem = origem_texto
            print(f"Origem salvo: {self.ponto_origem}")

            # Esconde os widgets de origem
            self.lbl_origem.grid_remove()
            self.ent_origem.grid_remove()

            # Mostra os widgets de destino
            self.lbl_destino.grid()
            self.ent_destino.grid()
            self.ent_destino.focus_set()

            self.ent_longitude.delete(0, 'end')
            self.ent_latitude.delete(0, 'end')
            self.mpv_rota.delete_all_marker()

            # Atualiza os textos da UI
            self.btn_continuar.config(text='Salvar Destino', bootstyle='primary')

        # Se o botão já foi alterado para "Salvar Destino", estamos definindo o destino.
        else:
            destino_texto = self.ent_destino.get()
            if not destino_texto:
                messagebox.showwarning("Campo Vazio", "Por favor, preencha o Destino antes de salvar.")
                return

            self.ponto_destino = destino_texto
            print(f"Destino salvo: {self.ponto_destino}")
        
            
    def buscar_e_marcar_no_mapa(self):
            """
            Busca as coordenadas e adiciona um marcador no mapa.
            Verifica qual campo está visível (Origem ou Destino).
            Usa geopy.Nominatim com user_agent personalizado (isso evita um erro na requisição).
            """
            # Verifica qual campo de texto está ativo para usar como referência
            if self.ent_origem.winfo_viewable():
                texto_referencia = self.ent_origem.get().strip()
            else:
                texto_referencia = self.ent_destino.get().strip()

            longitude_texto = self.ent_longitude.get().strip()
            latitude_texto = self.ent_latitude.get().strip()

            # Caso o usuário forneça lat/lon manualmente
            if latitude_texto and longitude_texto:
                try:
                    lat = float(latitude_texto)
                    lon = float(longitude_texto)
                    self.mpv_rota.delete_all_marker()
                    self.mpv_rota.set_marker(lat, lon, text=texto_referencia or "Coordenada")
                    self.mpv_rota.set_position(lat, lon)
                except ValueError:
                    messagebox.showerror("Erro de Valor", "Latitude e Longitude devem ser números válidos.")
                return

            # Caso o usuário forneça apenas um texto
            if texto_referencia:
                # Cria o geolocator com user_agent identificável
                geolocator = Nominatim(user_agent="MyBusApp/1.0")

                try:
                    location = geolocator.geocode(texto_referencia, addressdetails=True, exactly_one=True)
                    if location:
                        lat, lon = location.latitude, location.longitude
                        self.mpv_rota.delete_all_marker()
                        self.mpv_rota.set_marker(lat, lon, text=texto_referencia)
                        self.mpv_rota.set_position(lat, lon)

                        # Preenche os entrys
                        self.ent_latitude.delete(0,'end')
                        self.ent_latitude.insert(0, f"{lat:.7f}")

                        self.ent_longitude.delete(0,'end')
                        self.ent_longitude.insert(0, f"{lon:.7f}")

                    else:
                        messagebox.showerror("Endereço não encontrado", f"O endereço '{texto_referencia}' não pôde ser localizado.")
                except GeocoderServiceError as e:
                    messagebox.showerror("Erro no Serviço", f"Erro ao consultar o serviço de geocodificação: {e}")
                return

            # Se nenhum dado informado
            messagebox.showwarning("Faltam Dados", "Preencha o campo de endereço ou as coordenadas.")
    
    def voltar(self):
        # Verifica se estamos na tela de Destino
        if self.btn_continuar.cget('text') == 'Salvar Destino':
            self.lbl_destino.grid_remove()
            self.ent_destino.grid_remove()
            self.lbl_origem.grid()
            self.ent_origem.grid()

            self.ent_destino.delete(0, 'end')
            self.ent_longitude.delete(0, 'end')
            self.ent_latitude.delete(0, 'end')
            self.mpv_rota.delete_all_marker()
            
            # Restaura o valor do campo de origem e o foco
            self.ent_origem.delete(0, 'end')
            if self.ponto_origem:
                self.ent_origem.insert(0, self.ponto_origem)
            self.ent_origem.focus_set()
            
            self.btn_continuar.config(text='Salvar Origem', bootstyle='success')
        else:
            # Voltar para a janela anterior
            self.janela.destroy() 
            self.janela_origem.deiconify()