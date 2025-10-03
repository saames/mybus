
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

    def delete_linha(self, linha_id):
        cronograma = self.model.find("Cronograma", f"linha_id={linha_id}")
        for i in cronograma:
            self.model.delete("Cronograma", i[0])

        rotas = self.model.find("Rota", f"linha_id={linha_id}")
        for i in rotas:
            self.model.delete("Rota", i[0])

        user_linha = self.model.find("UserLinha", f"linha_id={linha_id}")
        for i in user_linha:
            self.model.delete("UserLinha", i[0])

        result = self.model.delete("Linha", linha_id)
        return result

