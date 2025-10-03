import requests

class OSRM:

    def gerar_rota(self, pontos):
        coordenadas_url = ";".join([f"{x[0]},{x[1]}" for x in pontos])
        try:
            url = f"http://router.project-osrm.org/route/v1/driving/{coordenadas_url}?overview=full&geometries=geojson"
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()
            coordenadas_lista = data['routes'][0]['geometry']['coordinates']
            coordenadas_tuplas = [(lon, lat) for lat, lon in coordenadas_lista ]
            return coordenadas_tuplas
        except requests.RequestException as e:
            print(e)
