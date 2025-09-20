import ttkbootstrap as ttk
import tkintermapview as tkmap
from resources.utils import Utils

class DefinirRotaView:
    def __init__(self, master):
        self.janela = master
        self.janela.title('Definir Rota - MyBus')
        #self.janela.geometry('860x500')
        self.janela.resizable(False, False)
        self.frm_center = ttk.Frame(self.janela)
        self.frm_center.pack(padx=20, pady=20)

        # Criação de Instâncias
        self.utils = Utils()

        #Título
        self.lbl_title = ttk.Label(self.frm_center, text='Definir rota de ida',  bootstyle='primary',font=('TkDefaultFont', 14, 'bold'))
        self.lbl_title.grid(column=0,row=0, sticky='w', pady=(15,15), columnspan=2)

        # Origem
        self.lbl_origem = ttk.Label(self.frm_center, text=' Origem', bootstyle='secondary-inverse', width=50)
        self.lbl_origem.grid(column=0, row=3, columnspan=2, sticky='we', ipady=5)
        self.ent_origem = ttk.Entry(self.frm_center, bootstyle='primary')
        self.ent_origem.grid(column=0, row=4, columnspan=2, sticky='we', pady=(0,20))

        # Longitude
        self.lbl_longitude = ttk.Label(self.frm_center, text=' Longitude', bootstyle='secondary-inverse')
        self.lbl_longitude.grid(column=0, row=5, sticky='we', ipady=5)
        self.ent_longitude = ttk.Entry(self.frm_center, bootstyle='primary')
        self.ent_longitude.grid(column=0, row=6, sticky='we')

        # Latitude
        self.lbl_latitude = ttk.Label(self.frm_center, text=' Latitude', bootstyle='secondary-inverse')
        self.lbl_latitude.grid(column=1, row=5, sticky='we', ipady=5)
        self.ent_latitude = ttk.Entry(self.frm_center, bootstyle='primary')
        self.ent_latitude.grid(column=1, row=6, sticky='we')

        # Botão Buscar Coordenadas
        self.btn_buscar = ttk.Button(self.frm_center, text='Buscar Coordenadas', bootstyle='secondary')
        self.btn_buscar.grid(column=1, row=7, sticky='e', pady=(20,64), ipadx=5)
        self.btn_buscar.bind('<ButtonRelease-1>')

        # Mapa
        self.lbl_map = ttk.Label(self.frm_center, text='Pré-Visualização da Rota')
        self.lbl_map.grid(column=2, row=2, columnspan=2)

        self.mpv_rota = tkmap.TkinterMapView(self.frm_center, width=380, height=260) # Cria mapa
        self.mpv_rota.set_position(-9.972802894375437, -67.82629104665347) # Define a posição em Rio Branco
        self.mpv_rota.set_zoom(13) # Ajusta o zoom
        self.mpv_rota.grid(column=2, row=3, columnspan=2, rowspan=5, padx=(20,0))

        # Botão Voltar
        self.btn_voltar = ttk.Button(self.frm_center, text='Voltar', bootstyle='secondary')
        self.btn_voltar.grid(column=0, row=8, pady=(80,0), sticky='w')
        self.btn_voltar.bind('<ButtonRelease-1>')

        # Botão Continuar
        self.btn_continuar = ttk.Button(self.frm_center, text='Continuar', bootstyle='success')
        self.btn_continuar.grid(column=3, row=8, pady=(80,0), sticky='e')
        self.btn_continuar.bind('<ButtonRelease-1>')







        self.utils.centraliza(self.janela)