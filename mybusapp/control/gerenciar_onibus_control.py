
from model.onibus_model import Onibus_model

class GerenciarOnibusControl:
    def listar_onibus(self, nome=''):
        self.model = Onibus_model()
        result = self.model.getAll()
        return result
