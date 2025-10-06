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
        if("id" not in linha.keys()):
            result = self.model.insert("Linha(nome, numero)", (nome, numero))
        else:
            result = self.model.update("Linha(nome, numero)", (f"'{nome}'", f"'{numero}'"), linha["id"])
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
        if ("id" not in linha.keys()):
            result = self.model.insert("Rota(trajetoSentido, coordenadas, marcacao, linha_id)", ('I', linha_rota_ida, linha_marcacao_ida, linha_id))
        else:
            self.rotas = self.model.find("Rota", f"linha_id = {linha_id}")
            if(self.rotas):
                rota_ida_id = self.rotas[0][0]
                result = self.model.update("Rota(trajetoSentido, coordenadas, marcacao, linha_id)", ('"I"', f"'{linha_rota_ida}'", f"'{linha_marcacao_ida}'", linha_id), rota_ida_id)
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
        if ("id" not in linha.keys()):
            result = self.model.insert("Rota(trajetoSentido, coordenadas, marcacao, linha_id)",
                                   ('V', linha_rota_volta, linha_marcacao_volta, linha_id))
        else:
            rota_volta_id = self.rotas[1][0]
            result = self.model.update("Rota(trajetoSentido, coordenadas, marcacao, linha_id)",
                                       ('"V"', f"'{linha_rota_volta}'", f"'{linha_marcacao_volta}'", linha_id), rota_volta_id)
        if (result):
            return self.inserir_horarios_util(linha, linha_id)

    def inserir_horarios_util(self, linha, linha_id):
        horarios_não_formatado = linha["horarios_util"]
        horarios_formatado = "#".join(horarios_não_formatado)
        if ("id" not in linha.keys()):
            result = self.model.insert("Cronograma(tipoDia, horarios, linha_id)", ("U", horarios_formatado, linha_id))
        else:
            self.cronogramas = self.model.find("Cronograma", f"linha_id = {linha_id}")
            if(self.cronogramas):
                crono_util_id = self.cronogramas[0][0]
                print(crono_util_id)
                result = self.model.update("Cronograma(tipoDia, horarios, linha_id)", ("'U'", f"'{horarios_formatado}'", linha_id), crono_util_id)
        if(result):
            return self.inserir_horarios_n_util(linha, linha_id)

    def inserir_horarios_n_util(self, linha, linha_id):
        horarios_não_formatado = linha["horarios_n_util"]
        horarios_formatado = "#".join(horarios_não_formatado)
        if ("id" not in linha.keys()):
            result = self.model.insert("Cronograma(tipoDia, horarios, linha_id)",
                                   ("N", horarios_formatado, linha_id))
        else:
            crono_n_util_id = self.cronogramas[1][0]
            print(crono_n_util_id)
            result = self.model.update("Cronograma(tipoDia, horarios, linha_id)", ("'N'", f"'{horarios_formatado}'", linha_id),
                                       crono_n_util_id)
        return result

    def verificar_numero_existente(self, numero, linha_id_a_ignorar=None):
        if linha_id_a_ignorar:
            # busca com o id diferente do atual
            result = self.model.find('Linha', f"numero = '{numero}'", f"id != {linha_id_a_ignorar}")
        else:
            # busca no geral
            result = self.model.find('Linha', f"numero = '{numero}'")
        return bool(result)

    def verificar_nome_existente(self, nome, linha_id_a_ignorar=None):
        padrao_busca = f"{nome}#%"
        if linha_id_a_ignorar:
            # busca com o id diferente do atual
            result = self.model.find('Linha', f"nome LIKE '{padrao_busca}'", f"id != {linha_id_a_ignorar}")
        else:
            # busca no geral
            result = self.model.find('Linha', f"nome LIKE '{padrao_busca}'")
        return bool(result)