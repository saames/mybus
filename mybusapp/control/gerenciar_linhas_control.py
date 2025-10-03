
from model.model import Model

class GerenciarLinhasControl:

    def __init__(self):
        self.model = Model()

    def listar_linhas(self, nome=''):
        result = self.model.getAll("Linha")
        return result

    def find_linha(self, linha_id):
        result = self.model.find("Linha", f"id = {linha_id}")
        return result