import tkinter
import tkintermapview
import requests  # Para fazer a chamada à API de rota

# --- Função Principal ---

def tracar_rota_no_mapa():
    """
    Busca as coordenadas da rota na API do OSRM e as desenha no mapa.
    """
    # Coordenadas de início e fim
    ponto_inicio = (-9.953089737653636, -67.86248304933982)
    ponto_fim = (-9.973780474521801, -67.80993100026353)

    # Lista de todas as paradas
    paradas = [
        (-9.93134046616895, -67.81839677433912),
        (-9.948967954095927, -67.8319821729281),
        (-9.96816579961511, -67.85057813803296),
        (-9.952527438225166, -67.84780256052507),
        (-9.972672384338503, -67.8047532169818)
    ]

    # Junta todos os pontos para a requisição (inicio -> paradas -> fim)
    todos_os_pontos = [ponto_inicio] + paradas + [ponto_fim]

    # Formata os pontos para a URL do OSRM (longitude,latitude)
    coordenadas_url = ";".join([f"{lon},{lat}" for lat, lon in todos_os_pontos])

    try:
        # 1. Monta a URL da API do OSRM com todas as paradas
        url = f"http://router.project-osrm.org/route/v1/driving/{coordenadas_url}?overview=full&geometries=geojson"

        # 2. Faz a requisição para a API
        response = requests.get(url)
        response.raise_for_status()  # Lança um erro se a requisição falhar

        # 3. Extrai os dados da rota do JSON
        data = response.json()
        rota_coords_raw = data['routes'][0]['geometry']['coordinates']

        # 4. Converte as coordenadas para o formato que o TkinterMapView espera
        # OSRM devolve [longitude, latitude], mas a biblioteca espera (latitude, longitude)
        pontos_da_rota = [(lat, lon) for lon, lat in rota_coords_raw]

        if pontos_da_rota:
            print(f"Rota encontrada com {len(pontos_da_rota)} pontos.")
            # 5. Desenha a rota no mapa usando a função .set_path()
            map_widget.set_path(pontos_da_rota, color="blue", width=5)

            # Centraliza o mapa e adiciona marcadores
            map_widget.set_position(ponto_inicio[0], ponto_inicio[1], marker=True, text="UFAC")
            map_widget.set_marker(ponto_fim[0], ponto_fim[1], text="Biblioteca centro")
            
            # Adiciona um marcador para cada parada
            for i, (lat_parada, lon_parada) in enumerate(paradas):
                map_widget.set_marker(lat_parada, lon_parada, text=f"Parada {i+1}")

            map_widget.set_zoom(12) # Ajusta o zoom para ver a rota toda
        else:
            print("Não foi possível encontrar a rota.")

    except requests.RequestException as e:
        print(f"Erro de conexão com a API: {e}")
    except (KeyError, IndexError):
        print("Erro ao processar a resposta da API. Rota não encontrada.")


# --- Interface Gráfica ---

# Janela principal
app = tkinter.Tk()
app.title("Rota com OSRM e Tkinter")
app.geometry("800x650")

# Botão para iniciar a ação
botao_tracar = tkinter.Button(app, text="Traçar Rota", command=tracar_rota_no_mapa)
botao_tracar.pack(pady=10)

# Widget do mapa
map_widget = tkintermapview.TkinterMapView(app, width=800, height=600, corner_radius=0)
map_widget.pack()

# Define uma posição inicial para o mapa
map_widget.set_position(-9.953089737653636, -67.86248304933982)
map_widget.set_zoom(10)

app.mainloop()