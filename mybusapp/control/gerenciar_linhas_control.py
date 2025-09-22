
from model.model import Model

class GerenciarLinhasControl:



    def listar_linhas(self, nome=''):
        self.model = Model()
        result = self.model.getAll("Linha")
        return result