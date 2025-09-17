import sqlite3
from sqlite3 import Error

class Conexao:
    def get_conexao(self):
        caminho = '../mybusapp/database/mybusDB'
        try:
            conexao = sqlite3.connect(caminho)
            return conexao
        except Error as er:
            print(er)


Conexao.get_conexao()