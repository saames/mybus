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

    def search(self, termobusca):
        sql = f"""SELECT Onibus.id, Onibus.numero, Onibus.placa, Onibus.status, Linha.nome 
                  FROM Onibus LEFT JOIN Linha ON Onibus.linha_id = Linha.id
                  WHERE CAST(Onibus.id AS TEXT) LIKE '%{termobusca}%'
                     OR Onibus.numero LIKE '%{termobusca}%'
                     OR Onibus.placa LIKE '%{termobusca}%'
                     OR Linha.nome LIKE '%{termobusca}%'
                     OR (LOWER('{termobusca}') = 'ativo' AND Onibus.status = 1)
                     OR (LOWER('{termobusca}') = 'inativo' AND Onibus.status = 0);
        """
        try:
            con = self.conexao.get_conexao()
            cursor = con.cursor()
            result = cursor.execute(sql).fetchall()
            con.close()
            return result
        except Error as er:
            print(er)
            return None

