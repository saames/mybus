from model.model import Model
from sqlite3 import Error

class UsuarioModel(Model):

    def delete(self, table, id):
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

