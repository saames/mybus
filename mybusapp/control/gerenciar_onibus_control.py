
from model.onibus_model import Onibus_model

class GerenciarOnibusControl:
    def __init__(self):
        self.model = Onibus_model()

    def listar_onibus(self, nome=''):
        result = self.model.getAll()
        return result

    def buscar_onibus(self, id):
        result = self.model.find("Onibus", f"id = {id}")
        return result

    def pesquisar_onibus(self, termobusca):
        result = self.model.search(termobusca)
        return result

    def inserir_onibus(self, numero, placa, status, linha_id = None):

        if linha_id != None:
            result = self.model.insert("Onibus(numero, placa, status, linha_id)", (numero, placa, status, linha_id))
        else:
            result = self.model.insert("Onibus(numero, placa, status)", (numero, placa, status))

        if (result):
            return result
        else:
            return None

    def editar_onibus(self, id, numero, placa, status, linha_id = None):

        if linha_id != None:
            result = self.model.update("Onibus(numero, placa, status, linha_id)", (f"'{numero}'", f"'{placa}'", status, linha_id), id)
        else:
            result = self.model.update("Onibus(numero, placa, status, linha_id)", (f"'{numero}'", f"'{placa}'", status, "NULL"), id)

        if(result):
            return result
        else:
            return None

    def excluir_onibus(self, id):
        result = self.model.delete("Onibus", id)
        if(result):
            return  result
        else:
            return  None