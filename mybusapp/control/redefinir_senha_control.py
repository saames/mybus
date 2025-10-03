from model.usuario_model import UsuarioModel

class RedefinirSenhaControl:
    def __init__(self):
        self.user_model = UsuarioModel()

    def buscar_usuario_cpf(self, cpf):
        result = self.user_model.find('Usuario', f"cpf = '{cpf}'")
        return result
    
    def editar_senha(self, usuario, senha):
        result = self.user_model.update("Usuario(nome, cpf, telefone, papel, status, senha, email)",
                                   (f"'{usuario[1]}'", f"'{usuario[2]}'", f"'{usuario[3]}'", f"'{usuario[4]}'", f"'{usuario[5]}'", f"'{senha}'", f"'{usuario[7]}'"), usuario[0])
        return result