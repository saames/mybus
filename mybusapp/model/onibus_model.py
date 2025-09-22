from model.model import Model
from sqlite3 import Error

class Onibus_model(Model):

    def __int__(self):
        Model()

    def getAll(self):
        sql = f"SELECT Onibus.id, Onibus.numero, Onibus.placa, Onibus.status, Linha.nome FROM Onibus LEFT JOIN Linha ON Onibus.linha_id = Linha.id"
        try:
            con = self.conexao.get_conexao()
            cursor = con.cursor()
            result = cursor.execute(sql).fetchall()
            con.close()
            return result
        except Error as er:
            print(er)
            return None

