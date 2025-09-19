
from model.usuario_model import UsuarioModel

class Cadastra_control:

    def Cadastrar_usuario(self, nome, cpf, telefone, senha, papel, status):
        user_model = UsuarioModel()
        result = user_model.insert("Usuario(nome, cpf, telefone, senha, papel, status)", (nome, cpf, telefone, senha, papel, status))
        if(result):
            return result
        else:
            return None