from H2Connector import H2Connector as connector
from faker import Faker
from utils import insert

import random

QUANTIDADE_PERFIS = 100

faker = Faker()

class GerentePerfil():
    connection = connector() 
    
    perfil_fields = ["nome_perfil", "biografia", "senha", "nome_real", "privacidade"]
    mensagem = [ "id", "texto", "data", "nome_criador" ]

    post = [ "foto", 'id_messagem' ]

    comentario = [ "id_messagem", 'id_post' ]

    # fills the perfil table with random data
    def fill(self):
        for _ in range(QUANTIDADE_PERFIS):
            nome_perfil = "'" + faker.name() + "'"
            biografia   = "'" + faker.text() +  "'"
            senha       = "'" + faker.credit_card_number() + "'"
            nome_real   = nome_perfil
            privacidade = str(True if random.random() > 0.5 else False)
            insert("perfil",
                    self.perfil_fields,
                    [ nome_perfil,
                        biografia,
                        senha,
                        nome_real,
                        privacidade ],
                    self.connection)

    def seleciona_perfil_aleatorio(self):
        def aux(cursor):
            cursor.execute("SELECT * FROM perfil ORDER BY RAND() LIMIT 1;") 
            return cursor.fetchall()
        result = self.connection.cursor(aux)        
        return result


    # makes a post
    def postar(self, texto, foto):
        pass 
