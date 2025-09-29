from model.model import Model

class UserLinhaControl:

    def __init__(self):
        self.model = Model()

    def criar_userlinha(self, user_id, linha_id):
        result = self.model.insert("UserLinha(usuario_id, linha_id, quantidadeUso, favorito)", (user_id, linha_id, 0, 0))
        return result

    def buscar_linhas_do_usuario(self, user_id):
        result = self.model.find("UserLinha", f"usuario_id = {user_id}")
        return result

    def registrar_viajem(self, user_id, linha_id):
        find_result = self.model.find("UserLinha", f"usuario_id = {user_id}", f"linha_id = {linha_id}")
        if(find_result):
            quantidade = find_result[0][3] + 1
            result = self.model.update("UserLinha(quantidadeUso)", (quantidade,), find_result[0][0])
            return result
        else:
            result = self.criar_userlinha(user_id, linha_id)
            if(result):
                self.registrar_viajem(user_id, linha_id)

    def favoritar_linha(self, user_id, linha_id):
        find_result = self.model.find("UserLinha", f"usuario_id = {user_id}", f"linha_id = {linha_id}")
        if(find_result):
            favorito = find_result[0][4]
            if int(favorito) == 1:
                result = self.model.update("UserLinha(favorito)", ("0"), find_result[0][0])
            else:
                result = self.model.update("UserLinha(favorito)", ("1"), find_result[0][0])
            return result
        else:
            result = self.criar_userlinha(user_id, linha_id)
            if(result):
                self.favoritar_linha(user_id, linha_id)






