from H2Connector import H2Connector as connector
from faker import Faker
from utils import insert, select_profile, create_fake_profile, alter, remove

from datetime import datetime

import random
import re

QUANTIDADE_PERFIS = 10

faker = Faker()

class GerentePerfil():
    connection = connector() 
    
    perfil_fields = ["nome_perfil", "biografia", "senha", "nome_real", "privacidade"]
    mensagem = [ "texto", "data", "nome_criador" ]

    post = [ "foto", 'id_mensagem' ]

    comentario = [ "id_messagem", 'id_post' ]

    perfil_atual = None

    _validation_pattern = re.compile("[a-zA-Z_0-9*]+")

    # fills the perfil table with random data
    def fill(self):
        for _ in range(QUANTIDADE_PERFIS):
            perfil = create_fake_profile()
            self.cadastrar_perfil(perfil)

    def _validar_nome_perfil(self, nome):
        m = self._validation_pattern.match(nome)
        if m and m.group() == nome:
            return True
        return False

    def _extrai_marcados(self, text):
        marcados = []
        tokens = text.split(" ")
        for i in tokens:
            if i.startswith("@"):
                marcados.append(i[1:])
        return marcados
                
    def cadastrar_perfil(self, perfil):
        '''
            create a profile
        '''
        if not self._validar_nome_perfil(perfil[0]):
            raise Exception("Nome invalido")
        insert("perfil",
                    self.perfil_fields,
                    perfil,
                    self.connection)

    def alterar_perfil(self, perfil):
        '''
            updates perfil
        '''
        if not self._validar_nome_perfil(perfil[0]):
            raise Exception("Nome invalido")
        alter("perfil",
                "nome_perfil:'{}'".format(self.perfil_atual[0]),
                self.perfil_fields,
                perfil,
                self.connection)

    def remove_perfil(self, nome):
        '''
            removes perfil
        '''
        if not self._validar_nome_perfil(nome):
            raise Exception("Nome invalido")
        remove('perfil',
                'nome_perfil',
                nome,
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
            id = str(self.get_mensagens()[-1][0])
            insert("post", self.post, [foto, id], self.connection)
        self.connection.cursor(aux)

        # notificar

    def get_mensagens(self):
        def aux(cursor):
            query = "SELECT * FROM mensagem m WHERE m.nome_criador = '{}' ORDER BY m.id".format(self.perfil_atual[0]) 
            cursor.execute(query)
            return cursor.fetchall()
        return self.connection.cursor(aux)

    def get_posts_atual(self):
        '''
            Get the posts from the current profile
        '''
        def aux(cursor):
           query = "SELECT * FROM mensagem m INNER JOIN post p ON m.id = p.id_mensagem  WHERE m.nome_criador = '{}' ORDER BY m.id;".format(self.perfil_atual[0])
           cursor.execute(query)
           ret = cursor.fetchall()
           x = [[i[1], i[4]] for i in ret]
           return x
        return self.connection.cursor(aux)
