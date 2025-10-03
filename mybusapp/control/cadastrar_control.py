
from model.usuario_model import UsuarioModel

class Cadastra_control:

    def __init__(self):
        self.user_model = UsuarioModel()

    def Cadastrar_usuario(self, nome, cpf, telefone, senha, papel, status, email):
        result = self.user_model.insert("Usuario(nome, cpf, telefone, senha, papel, status, email)", (nome, cpf, telefone, senha, papel, status, email))
        if(result):
            return result
        else:
            return None
        
    def editar_usuario(self, id, nome, cpf, senha, telefone, papel, status, email):
        result = self.user_model.update("Usuario(nome, cpf, telefone, papel, status, senha, email)",
                                   (f"'{nome}'", f"'{cpf}'", f"'{telefone}'", f"'{papel}'", f"'{status}'", f"'{senha}'", f"'{email}'"), id)
        return result
    
    def verificar_cpf_existente(self, cpf):
        result = self.user_model.find('Usuario', f"cpf = '{cpf}'")
        return bool(result)

    def verificar_email_existente(self, email, user_id_a_ignorar=None):
        if user_id_a_ignorar:
            # busca com o id diferente do atual
            result = self.user_model.find('Usuario', f"email = '{email}'", f"id != {user_id_a_ignorar}")
        else:
            # busca no geral
            result = self.user_model.find('Usuario', f"email = '{email}'")
        return bool(result)

    def verificar_telefone_existente(self, telefone, user_id_a_ignorar=None):
        if user_id_a_ignorar:
            result = self.user_model.find('Usuario', f"telefone = '{telefone}'", f"id != {user_id_a_ignorar}")
        else:
            result = self.user_model.find('Usuario', f"telefone = '{telefone}'")
        return bool(result)