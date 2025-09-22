
from model.usuario_model import UsuarioModel

class GerenciarUsuariosControl:
    def __init__(self):
        self.model = UsuarioModel()

    def listar_usuarios(self, nome=''):
        result = self.model.getAll()
        return result
    
    
    def deletar_usuario(self, id):
        return self.model.delete(id)

    def promover_usuario(self,id):
        return self.model.promover(id)