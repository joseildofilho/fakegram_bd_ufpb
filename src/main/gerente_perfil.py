from H2Connector import H2Connector as connector
from faker import Faker
from utils import insert, select_profile, create_fake_profile

from datetime import datetime

import random

QUANTIDADE_PERFIS = 10

faker = Faker()

class GerentePerfil():
    connection = connector() 
    
    perfil_fields = ["nome_perfil", "biografia", "senha", "nome_real", "privacidade"]
    mensagem = [ "texto", "data", "nome_criador" ]

    post = [ "foto", 'id_mensagem' ]

    comentario = [ "id_messagem", 'id_post' ]

    perfil_atual = None

    # fills the perfil table with random data
    def fill(self):
        for _ in range(QUANTIDADE_PERFIS):
            perfil = create_fake_profile()
            self.cadastrar_perfil(perfil)
                
    def cadastrar_perfil(self, perfil):
        '''
            create a profile
        '''
        insert("perfil",
                    self.perfil_fields,
                    perfil,
                    self.connection)

    def seleciona_perfil_aleatorio(self):
        '''
            selects a random profile
        '''
        def aux(cursor):
            cursor.execute("SELECT * FROM perfil ORDER BY RAND() LIMIT 1;") 
            return cursor.fetchall()
        result = self.connection.cursor(aux)        
        return result

    def select_perfil(self, nome):
        return select_profile(nome, self.connection)
    
    def set_perfil(self, nome):
        self.perfil_atual = self.select_perfil(nome)

    def postar(self, texto, foto):
        def aux(cursor):
            insert("mensagem", self.mensagem, [texto, str(datetime.now()), self.perfil_atual[0]], self.connection)
            id = str(self.get_mensagens()[0][0])
            insert("post", self.post, [foto, id], self.connection)
        self.connection.cursor(aux)

    def get_mensagens(self):
        def aux(cursor):
            query = "SELECT * FROM mensagem m WHERE m.nome_criador = '{}'".format(self.perfil_atual[0])
            cursor.execute(query)
            return cursor.fetchall()
        return self.connection.cursor(aux)

    def get_posts_atual(self):
        '''
            Get the posts from the current profile
        '''
        def aux(cursor):
           query = "SELECT * FROM mensagem m INNER JOIN post p ON m.id = p.id_mensagem  WHERE m.nome_criador = '{}' ORDER BY m.data;".format(self.perfil_atual[0])
           cursor.execute(query)
           ret = cursor.fetchall()
           x = [[i[1], i[4]] for i in ret]
           return x
        return self.connection.cursor(aux)
