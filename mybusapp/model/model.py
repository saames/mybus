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

ml = Model()