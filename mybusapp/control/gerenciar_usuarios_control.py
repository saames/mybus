
from model.usuario_model import UsuarioModel

class GerenciarUsuariosControl:
    def __init__(self):
        self.model = UsuarioModel()

    def listar_usuarios(self, nome=''):
        result = self.model.getAll()
        return result

    def pesquisar_usuario(self, termobusca):
        result = self.model.search(termobusca)
        return result

    def buscar_usuario_id(self, id):
        result = self.model.find('Usuario', f'id = {id}')
        return result

    def deletar_usuario(self, id):
        return self.model.delete(id)

    def promover_usuario(self,id):
        return self.model.promover(id)

    def rebaixar_usuario(self,id):
        return self.model.rebaixar(id)