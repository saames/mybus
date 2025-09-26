
from model.model import Model

class RotaControl:

    def __init__(self):
        self.model = Model()

    def buscar_rotas_da_linha(self, linha_id):
        result_bd = self.model.find("Rota", f"linha_id = {linha_id}")
        result = [[(float(lat), float(lon)) for lat, lon in [coord.split(",") for coord in record[2].split("#")]] for record in result_bd]
        return result