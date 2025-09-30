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
        
        self.ponto = {}

        # Título
        self.lbl_title = ttk.Label(self.frm_center, text='Definir Parada',  bootstyle='primary', font=('TkDefaultFont', 14, 'bold'))
        self.lbl_title.grid(column=0, row=0, sticky='w', pady=(0, 15), columnspan=2)

        # Ponto
        self.lbl_ponto = ttk.Label(self.frm_center, text='Ponto', bootstyle='secondary-inverse')
        self.lbl_ponto.grid(column=0, row=3, columnspan=2, sticky='we', ipady=5)
        self.ent_ponto = ttk.Entry(self.frm_center, bootstyle='primary')
        self.ent_ponto.grid(column=0, row=4, columnspan=2, sticky='we', pady=(0,20))


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

        # Botão Salvar Ponto
        self.btn_continuar = ttk.Button(self.frm_center, text='Salvar Ponto', bootstyle='success', command=self.salvar_ponto)
        self.btn_continuar.grid(column=2, row=8, pady=(40,0), sticky='e')

        self.utils.centraliza(self.janela)

    def salvar_ponto(self):
            nome_ponto = self.ent_origem.get()
            lat_texto = self.ent_latitude.get()
            lon_texto = self.ent_longitude.get()
            if not nome_ponto or not lat_texto or not lon_texto:
                messagebox.showwarning("Campo Vazio", "Por favor, preencha a origem antes de continuar.")
                return
            
            self.ponto = {
                "nome": nome_ponto,
                "lat":float(lat_texto),
                "lon": float(lon_texto)
            }
            print(f"Ponto salvo: {self.ponto}")

            
    def buscar_e_marcar_no_mapa(self):
            """
            Busca as coordenadas e adiciona um marcador no mapa.
            Usa geopy.Nominatim com user_agent personalizado (isso evita um erro na requisição).
            """
            texto_referencia = self.ent_ponto.get().strip()
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
            self.janela.destroy() 
            self.janela_origem.deiconify()