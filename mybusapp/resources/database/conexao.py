import sqlite3
from sqlite3 import Error

class Conexao:
    def get_conexao(self):
        caminho = "../resources/database/mybusDB.db"
        try:
            conexao = sqlite3.connect(caminho)
            return conexao
        except Error as er:
            print(er)
