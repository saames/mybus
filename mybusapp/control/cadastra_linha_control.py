from model.model import Model

class CadastrarLinhaControl():

    def __init__(self):
        self.model = Model()

    def inserir_linha(self, linha):
        nome = linha["nome"]
        linha_origem = linha["pontos_iniciais"][0][0]
        linha_destino = linha["pontos_iniciais"][1][0]

        nome += f"#{linha_origem}-{linha_destino}"
        numero = linha["numero"]
        result = self.model.insert("Linha(nome, numero)", (nome, numero))
        if(result):
            linha_id = self.model.find("Linha", f"nome = '{nome}'", f"numero = '{numero}'")
            return self.inserir_rota_ida(linha, linha_id[0][0])


    def inserir_rota_ida(self, linha, linha_id):
        linha_rota_ida_nao_formatada = linha["rota-ida"]
        linha_rota_ida = ""
        for i in range(len(linha_rota_ida_nao_formatada)):
            if(i < len(linha_rota_ida_nao_formatada)-1):
                linha_rota_ida += f"{linha_rota_ida_nao_formatada[i][0]},{linha_rota_ida_nao_formatada[i][1]}#"
            else:
                linha_rota_ida += f"{linha_rota_ida_nao_formatada[i][0]},{linha_rota_ida_nao_formatada[i][1]}"
        linha_marcacao_ida_não_formatada = linha["marcacao-ida"]
        linha_marcacao_ida = ""
        for i in range(len(linha_marcacao_ida_não_formatada)):
            if(i < len(linha_marcacao_ida_não_formatada)-1):
                linha_marcacao_ida += f"{linha_marcacao_ida_não_formatada[i][1]},{linha_marcacao_ida_não_formatada[i][2]},{linha_marcacao_ida_não_formatada[i][3]}#"
            else:
                linha_marcacao_ida += f"{linha_marcacao_ida_não_formatada[i][1]},{linha_marcacao_ida_não_formatada[i][2]},{linha_marcacao_ida_não_formatada[i][3]}"
        result = self.model.insert("Rota(trajetoSentido, coordenadas, marcacao, linha_id)", ('I', linha_rota_ida, linha_marcacao_ida, linha_id))
        if(result):
            return self.inserir_rota_volta(linha, linha_id)

    def inserir_rota_volta(self, linha, linha_id):
        linha_rota_volta_nao_formatada = linha["rota-volta"]
        linha_rota_volta = ""
        for i in range(len(linha_rota_volta_nao_formatada)):
            if (i < len(linha_rota_volta_nao_formatada) - 1):
                linha_rota_volta += f"{linha_rota_volta_nao_formatada[i][0]},{linha_rota_volta_nao_formatada[i][1]}#"
            else:
                linha_rota_volta += f"{linha_rota_volta_nao_formatada[i][0]},{linha_rota_volta_nao_formatada[i][1]}"
        linha_marcacao_volta_não_formatada = linha["marcacao-volta"]
        linha_marcacao_volta = ""
        for i in range(len(linha_marcacao_volta_não_formatada)):
            if (i < len(linha_marcacao_volta_não_formatada) - 1):
                linha_marcacao_volta += f"{linha_marcacao_volta_não_formatada[i][1]},{linha_marcacao_volta_não_formatada[i][2]},{linha_marcacao_volta_não_formatada[i][3]}#"
            else:
                linha_marcacao_volta += f"{linha_marcacao_volta_não_formatada[i][1]},{linha_marcacao_volta_não_formatada[i][2]},{linha_marcacao_volta_não_formatada[i][3]}"
        result = self.model.insert("Rota(trajetoSentido, coordenadas, marcacao, linha_id)",
                                   ('V', linha_rota_volta, linha_marcacao_volta, linha_id))
        if (result):
            return self.inserir_horarios_util(linha, linha_id)

    def inserir_horarios_util(self, linha, linha_id):
        horarios_não_formatado = linha["horarios_util"]
        horarios_formatado = "#".join(horarios_não_formatado)
        result = self.model.insert("Cronograma(tipoDia, horarios, linha_id)", ("U", horarios_formatado, linha_id))
        if(result):
            return self.inserir_horarios_n_util(linha, linha_id)

    def inserir_horarios_n_util(self, linha, linha_id):
        horarios_não_formatado = linha["horarios_n_util"]
        horarios_formatado = "#".join(horarios_não_formatado)
        result = self.model.insert("Cronograma(tipoDia, horarios, linha_id)",
                                   ("U", horarios_formatado, linha_id))
        return result
