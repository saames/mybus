import sqlite3
from sqlite3 import Error
from pathlib import Path



class Conexao:
    def get_conexao(self):
        BASE_DIR = Path(__file__).resolve().parent
        caminho = BASE_DIR / "mybusDB.db"
        caminho = caminho.resolve()
        try:
            conexao = sqlite3.connect(caminho)
            return conexao
        except Error as er:
            print(er)

conexao = Conexao()
conexao.get_conexao()