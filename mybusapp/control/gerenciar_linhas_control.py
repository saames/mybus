
from model.model import Model
from control.rota_control import RotaControl
from control.cronograma_control import CronogramaControl
from datetime import datetime

class GerenciarLinhasControl:

    def __init__(self):
        self.model = Model()
        self.rota_control = RotaControl()
        self.crono_control = CronogramaControl()

    def listar_linhas(self, nome=''):
        result = self.model.getAll("Linha")
        return result

    def find_linha(self, linha_id):
        result = self.model.find("Linha", f"id = {linha_id}")
        return result

    def find_linha_completa(self, linha_id):
        linha = {}
        result = self.model.find("Linha", f"id = {linha_id}")
        if(result):
            linha["id"] = result[0][0]
            linha["nome"] = result[0][1]
            linha["numero"] = result[0][2]
            result_rotas = self.rota_control.buscar_rotas_da_linha(linha_id)
            if(result_rotas):
                linha["pontos_iniciais"] = []
                linha["pontos_iniciais"].append(result_rotas[1][0][0])
                ponto_destino_index = len(result_rotas[1][0]) - 1
                linha["pontos_iniciais"].append(result_rotas[1][0][ponto_destino_index])
                linha["rota-ida"] = result_rotas[0][0]
                linha["marcacao-ida"] = result_rotas[1][0]
                linha["rota-volta"] = result_rotas[0][1]
                linha["marcacao-volta"] = result_rotas[1][1]
                result_cronograma = self.crono_control.listar_cronograma(linha_id)
                if(result_cronograma):
                    tempo1 = result_cronograma[0][0][0]
                    tempo2 = result_cronograma[0][0][1]
                    tempo1 = datetime.strptime(tempo1, "%H:%M")
                    tempo2 = datetime.strptime(tempo2, "%H:%M")
                    diferenca_util = tempo2 - tempo1
                    tempo1 = result_cronograma[1][0][0]
                    tempo2 = result_cronograma[1][0][1]
                    tempo1 = datetime.strptime(tempo1, "%H:%M")
                    tempo2 = datetime.strptime(tempo2, "%H:%M")
                    diferenca_n_util = tempo2 - tempo1
                    linha["intervalo_util"] = str(int(diferenca_util.total_seconds() / 60))
                    linha["intervalo_n_util"] = str(int(diferenca_n_util.total_seconds() / 60))
                    return linha



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

