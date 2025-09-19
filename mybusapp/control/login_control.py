from model.usuario_model import UsuarioModel

class LoginControl:

    def autenticar(self, cpf, senha):
        user_model = UsuarioModel()
        result = user_model.find("Usuario", f"cpf = {cpf}", f"senha={senha}")
        if(result):
            return result[0]
        else:
            return None