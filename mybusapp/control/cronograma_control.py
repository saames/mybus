from model.model import Model

class CronogramaControl:

    def __init__(self):
        self.model = Model()

    def listar_cronograma(self, linha_id):
        result = self.model.find("Cronograma", f"linha_id = {linha_id}")
        print(result)
        cronograma = []
        for i in result:
            aux = []
            aux2 = []
            for j in i[2].split("#"):
                aux2.append(j)
                if (len(aux2) == 2):
                    aux2 = tuple(aux2)
                    aux.append(aux2)
                    aux2 = []
            cronograma.append(aux)
        return cronograma
