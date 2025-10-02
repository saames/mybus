from model.model import Model
from sqlite3 import Error

class UsuarioModel(Model):

    def __int__(self):
        Model()

    def delete(self, id):
        sql = f"UPDATE Usuario SET status = 'I' where id = {id};"
        try:
            con = self.conexao.get_conexao()
            cursor = con.cursor()
            result = cursor.execute(sql).rowcount
            con.commit()
            con.close()
            return result
        except Error as er:
            print(er)
    
    def promover(self, id):
        sql = f"UPDATE Usuario SET papel = 'adm' where id = {id};"
        try:
            con = self.conexao.get_conexao()
            cursor = con.cursor()
            result = cursor.execute(sql).rowcount
            con.commit()
            con.close()
            return result
        except Error as er:
            print(er)

    def getAll(self):
        sql = f"SELECT Usuario.id, Usuario.nome, Usuario.email, Usuario.telefone, Usuario.papel, Usuario.status FROM Usuario"
        try:
            con = self.conexao.get_conexao()
            cursor = con.cursor()
            result = cursor.execute(sql).fetchall()
            con.close()
            return result
        except Error as er:
            print(er)
            return None

    def search(self, termobusca):
        sql = f"""SELECT 
                    Usuario.id, 
                    Usuario.nome, 
                    Usuario.telefone, 
                    Usuario.papel, 
                    Usuario.status 
                    FROM Usuario
                    WHERE Usuario.id = '{termobusca}'
                       OR Usuario.nome LIKE '%{termobusca}%'
                       OR Usuario.telefone LIKE '%{termobusca}%'
                       OR Usuario.papel = '{termobusca}'
                       OR Usuario.status = (
                            CASE 
                                WHEN UPPER('{termobusca}') = 'ATIVO' THEN 'A'
                                WHEN UPPER('{termobusca}') = 'INATIVO' THEN 'I'
                                ELSE '{termobusca}'
                            END
                       );"""
        try:
            con = self.conexao.get_conexao()
            cursor = con.cursor()
            result = cursor.execute(sql).fetchall()
            con.close()
            return result
        except Error as er:
            print(er)
            return None