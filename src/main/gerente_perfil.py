from .H2Connector import H2Connector as connector
from faker import Faker
from .utils import insert

import random

QUANTIDADE_PERFIS = 1000

faker = Faker()

class GerentePerfil():
    connection = connector() 
    
    perfil_fields = ["nome_perfil", "biografia", "senha", "nome_real", "privacidade"]

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
