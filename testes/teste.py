import tkinter
import tkintermapview
import requests  # Para fazer a chamada à API de rota

# --- Função Principal ---


# Lista de todas as paradas
paradas = []
def tracar_rota_no_mapa():
    """
    Busca as coordenadas da rota na API do OSRM e as desenha no mapa.
    """
    # Coordenadas de início e fim
    ponto_inicio = (-9.953089737653636, -67.86248304933982)
    ponto_fim = (-9.973780474521801, -67.80993100026353)

    # Junta todos os pontos para a requisição (inicio -> paradas -> fim)
    todos_os_pontos = paradas

    # Formata os pontos para a URL do OSRM (longitude,latitude)
    coordenadas_url = ";".join([f"{lon},{lat}" for lat, lon in todos_os_pontos])

    try:
        # 1. Monta a URL da API do OSRM com todas as paradas
        url = f"http://router.project-osrm.org/route/v1/driving/{coordenadas_url}?overview=full&geometries=geojson"
        print(url)
        # 2. Faz a requisição para a API
        response = requests.get(url)
        response.raise_for_status()  # Lança um erro se a requisição falhar

        # 3. Extrai os dados da rota do JSON
        data = response.json()
        rota_coords_raw = data['routes'][0]['geometry']['coordinates']
        nome_rotas = [x["name"] for x in data["waypoints"]]
        print(nome_rotas)

        # 4. Converte as coordenadas para o formato que o TkinterMapView espera
        # OSRM devolve [longitude, latitude], mas a biblioteca espera (latitude, longitude)
        pontos_da_rota = [(lat, lon) for lon, lat in rota_coords_raw]

        if pontos_da_rota:
            print(f"Rota encontrada com {len(pontos_da_rota)} pontos.")
            # 5. Desenha a rota no mapa usando a função .set_path()
            map_widget.set_path(pontos_da_rota, color="blue", width=5)
            
            for i in range(len(nome_rotas)):
                if(nome_rotas[i] == ""):
                    nome_rotas[i] = f"Parada"
                map_widget.set_marker(paradas[i][0], paradas[i][1], f"{i+1}.{nome_rotas[i]}")

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

# Rótulo para exibir as coordenadas
label_coords = tkinter.Label(app, text="Clique no mapa para ver as coordenadas")
label_coords.pack()

# Botão para iniciar a ação
botao_tracar = tkinter.Button(app, text="Traçar Rota", command=tracar_rota_no_mapa)
botao_tracar.pack(pady=5)

# Widget do mapa
map_widget = tkintermapview.TkinterMapView(app, width=800, height=600, corner_radius=0)
map_widget.pack()

# --- Função para obter coordenadas do clique ---
def obter_coordenadas_clique(coordenadas):
    """
    Função chamada ao clicar no mapa. Atualiza o rótulo com as coordenadas.
    """
    lat, lon = coordenadas
    label_coords.config(text=f"Coordenadas: (Latitude: {lat:.7f}, Longitude: {lon:.7f})")
    print(f"Coordenadas do clique: ({lat}, {lon})")
    map_widget.set_marker(lat, lon)
    paradas.append((lat, lon))

# Adiciona o comando de clique esquerdo ao mapa
map_widget.add_left_click_map_command(obter_coordenadas_clique)


# Define uma posição inicial para o mapa
map_widget.set_position(-9.953089737653636, -67.86248304933982)
map_widget.set_zoom(10)

app.mainloop()