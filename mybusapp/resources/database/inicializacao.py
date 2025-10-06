from resources.database.conexao import Conexao
from sqlite3 import Error

class Inicializacao:

    def __init__(self):
        self.conexao = Conexao()
        sql = """
            CREATE TABLE IF NOT EXISTS Linha (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(255) NOT NULL,
                numero VARCHAR(50) NOT NULL
            );

            CREATE TABLE IF NOT EXISTS Usuario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(255) NOT NULL,
                cpf CHAR(11) NOT NULL UNIQUE,
                telefone VARCHAR(9),
                papel VARCHAR(255) NOT NULL,
                status VARCHAR(255) NOT NULL,
                senha VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL DEFAULT ''
            );

            INSERT OR IGNORE INTO Usuario (nome, cpf, telefone, papel, status, senha, email)
            VALUES ('SUPER ADM', '00000000000', '680000000000', 'super', 'ativo', '00000000', 'adm@email.com');

            CREATE TABLE IF NOT EXISTS UserLinha (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                linha_id INTEGER NOT NULL,
                quantidadeUso INTEGER,
                favorito INTEGER,
                FOREIGN KEY (usuario_id) REFERENCES Usuario(id),
                FOREIGN KEY (linha_id) REFERENCES Linha(id)
            );

            CREATE TABLE IF NOT EXISTS Rota (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trajetoSentido VARCHAR(255),
                coordenadas TEXT,
                marcacao TEXT,
                linha_id INTEGER NOT NULL,
                FOREIGN KEY (linha_id) REFERENCES Linha(id)
            );

            CREATE TABLE IF NOT EXISTS Cronograma (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipoDia VARCHAR(50),
                horarios TEXT,
                linha_id INTEGER NOT NULL,
                FOREIGN KEY (linha_id) REFERENCES Linha(id)
            );

            CREATE TABLE IF NOT EXISTS Onibus (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero VARCHAR(50) NOT NULL,
                placa VARCHAR(50) NOT NULL,
                status BOOLEAN,
                linha_id INTEGER,
                FOREIGN KEY (linha_id) REFERENCES Linha(id)
            );
        """
        try:
            con = self.conexao.get_conexao()
            cursor = self.con.cursor()
            cursor.execute(sql)
            con.commit()
            con.close()
        except Error as er:
            print(er)

