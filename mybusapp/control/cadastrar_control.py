
from model.usuario_model import UsuarioModel

class Cadastra_control:

    def __init__(self):
        self.user_model = UsuarioModel()

    def Cadastrar_usuario(self, nome, cpf, telefone, senha, papel, status):
        result = self.user_model.insert("Usuario(nome, cpf, telefone, senha, papel, status)", (nome, cpf, telefone, senha, papel, status))
        if(result):
            return result
        else:
            return None

    def editar_usuario(self, id, nome, cpf, senha, telefone, papel, status):
        result = self.user_model.update("Usuario(nome, cpf, telefone, papel, status, senha)",
                                   (f"'{nome}'", f"'{cpf}'", f"'{telefone}'", f"'{papel}'", f"'{status}'", f"'{senha}'"), id)
        return result