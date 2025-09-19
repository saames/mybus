from mybusapp.resources.database.conexao import Conexao
from sqlite3 import Error

class Model:

    def __init__(self):
        self.conexao = Conexao()

    def getAll(self, table):
          sql = f"SELECT * FROM {table};"
          try:
              con = self.conexao.get_conexao()
              cursor = con.cursor()
              result = cursor.execute(sql).fetchall()
              con.close()
              return result
          except Error as er:
              print(er)

    def find(self, table, *args):
        sql = f"SELECT * FROM {table} WHERE"
        for i in range(len(args)):

            if i != len(args) - 1:
                sql += f" {args[i]} AND"
            else:
                sql += f" {args[i]};"

        print(sql)
        try:
            con = self.conexao.get_conexao()
            cursor = con.cursor()
            result = cursor.execute(sql).fetchall()
            con.close()
            return result
        except Error as er:
            print(er)

    def insert(self, table, values):
         sql = f"INSERT INTO {table} VALUES {values};"
         try:
             con = self.conexao.get_conexao()
             cursor = con.cursor()
             result = cursor.execute(sql).rowcount
             con.commit()
             con.close()
             return result
         except Error as er:
             print(er)

    def update(self, table, values, id):
        """
        Atualiza um registro em uma tabela no banco de dados.

        Parâmetros:
        - table (str): Nome da tabela e os atributos a serem atualizados, no formato 'tabela(atributo1, atributo2,...)'.
        - values (tuple): Tupla contendo os novos valores a serem atribuídos aos atributos, na mesma ordem dos atributos na tabela.
        - id (int): Identificador da ocorrencia que deseja atualiza.

        Exemplo de uso:
        update("Usuario(nome, cpf)", ("João", 00000000000), 1)
        """

        table = table.split("(")
        table_name = table[0]
        table_atributs = table[1].strip(")").split(",")
        num_atributs = len(table_atributs)
        sql = f"UPDATE {table_name} SET"

        for i in range(num_atributs):
            if(i < num_atributs - 1):
                sql += f" {table_atributs[i]} = {values[i]},"
            else:
                sql += f" {table_atributs[i]} = {values[i]}"
        sql += f" WHERE id = {id};"

        try:
            con = self.conexao.get_conexao()
            cursor = con.cursor()
            result = cursor.execute(sql).rowcount
            con.commit()
            con.close()
            return result
        except Error as er:
            print(er)


    def delete(self, table, id):
        sql = f"DELETE FROM {table} WHERE id = {id}"
        try:
            con = self.conexao.get_conexao()
            cursor = con.cursor()
            result = cursor.execute(sql).rowcount
            con.commit()
            con.close()
            return result
        except Error as er:
            print(er)
