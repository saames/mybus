import ttkbootstrap as ttk
import tkintermapview as tkmap
from tkinter import messagebox
from resources.utils import Utils
from resources.osrm.osrm import OSRM
from control.rota_control import RotaControl

class VisualizarRotaView:
    def __init__(self, master, linha):
        self.janela = master
        self.janela.title('Visualizar Rota - MyBus')
        self.janela.geometry('575x500')
        self.janela.resizable(False, False)
        self.frm_center = ttk.Frame(self.janela)
        self.frm_center.grid(column=0, row=0, padx=10, pady=10)

        print(linha)
        self.nome_completo = linha[1]
        self.linha_id = linha[0]

        # Criação de Instâncias
        self.utils = Utils()
        self.rota_control = RotaControl()

        # Botão voltar
        self.style = ttk.Style()
        self.style.configure('large.TButton', font=('TkDefaultFont', 18, 'bold'))
        self.btn_voltar = ttk.Button(self.frm_center, text='⬅', style='large.TButton')
        self.btn_voltar.grid(column=0, row=0)
        self.btn_voltar.bind('<ButtonRelease-1>')

        # Nome da rota
        self.nome_rota = f'Rota: {linha[0]} {self.nome_completo}'
        self.lbl_nome_rota = ttk.Label(self.frm_center, text=self.nome_rota, bootstyle='primary-inverse', padding=(150, 11))
        self.lbl_nome_rota.grid(column=1, row=0)

        self.traçar_rota()

        self.utils.centraliza(self.janela)

    def traçar_rota(self):
        result = self.rota_control.buscar_rotas_da_linha(self.linha_id)
        if(len(result) > 1):
            # Mapa
            self.mpv_rota = tkmap.TkinterMapView(self.frm_center, width=554, height=350) # Cria mapa
            self.mpv_rota.set_position(-9.972802894375437, -67.82629104665347) # Define a posição em Rio Branco
            self.mpv_rota.set_zoom(13) # Ajusta o zoom
            self.mpv_rota.set_path(result[0], color="#0B67CD", width=5)
            self.mpv_rota.set_path(result[1], color="red", width=4)
            self.mpv_rota.grid(column=0, row=1, columnspan=2)

            # Legenda
            self.lbl_legenda = ttk.Label(self.frm_center, text=' Legenda: ', bootstyle='primary-inverse')
            self.lbl_legenda.grid(column=0, row=2, columnspan=2 , sticky='we', pady=8)


            self.nome_completo = self.nome_completo.split("–")
            self.nome_origem = self.nome_completo[0].strip()
            self.nome_destino = self.nome_completo[1].strip()

            self.lbl_ida_cor = ttk.Label(self.frm_center, bootstyle='info-inverse')
            self.lbl_ida_cor.grid(column=0, row=3, ipadx=8, ipady=0)
            self.lbl_ida_nome = ttk.Label(self.frm_center, text=f"{self.nome_origem} / {self.nome_destino}")
            self.lbl_ida_nome.grid(column=1, row=3, sticky='w')

            self.lbl_volta_cor = ttk.Label(self.frm_center, bootstyle='danger-inverse')
            self.lbl_volta_cor.grid(column=0, row=4, ipadx=8, ipady=0, pady=5)
            self.lbl_volta_nome = ttk.Label(self.frm_center, text=f"{self.nome_destino} / {self.nome_origem}")
            self.lbl_volta_nome.grid(column=1, row=4, sticky='w')
            
        else:
            messagebox.showerror("Error", "Essa linha não possui rota cadastrada.")
