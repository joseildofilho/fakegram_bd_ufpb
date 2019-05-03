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
    mensagem = [ "texto", "data", 'topico', "nome_criador" ]

    post = [ "foto", 'id_mensagem' ]

    comentario = [ "id_mensagem", 'id_post' ]

    conversa = ['nome_remetente', 'nome_destinatario', 'msg']

    notificacao = ['nome_notificado', 'data', 'vista', 'tipo', 'nome_notificador', 'id_mensagem']

    topico = ['nome']

    marcado_perfil = ["nome_marcado", 'id_mensagem']

    bloqueia = ['nome_bloqueador', 'nome_bloqueado']

    segue = ['nome_seguidor', 'nome_seguido']

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

    def _seguidores(self, marcados):
        def aux(cursor):
            ret = []
            for marcado in marcados:
                query = "SELECT * FROM segue WHERE nome_seguido = '{}' AND nome_seguidor = '{}'".format(self.perfil_atual[0], marcado)
                cursor.execute(query)
                if cursor.fetchall():
                    ret.append(marcado)
            return ret
        return self.connection.cursor(aux)

    def _publicos(self, marcados):
        def aux(cursor):
            ret = []
            for marcado in marcados:
                query = "SELECT privacidade FROM perfil WHERE nome_perfil = '{}'".format(marcado)
                cursor.execute(query)
                priv = cursor.fetchone() 
                if priv and priv[0]:
                    ret.append(marcado)
            return ret
        return self.connection.cursor(aux)

    def _extrai_marcados(self, text):
        marcados = []
        tokens = text.split(" ")
        for i in tokens:
            if i.startswith("@"):
                marcados.append(i[1:])
        marcados = list(set(self._seguidores(marcados)) | set(self._publicos(marcados)))
        return marcados
    
    def _extrair_topicos(self, text):
        topicos = []
        tokens = text.split(" ")
        for token in tokens:
            if token.startswith("#"):
                topicos.append(token[1:])
        return topicos
                
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
            cursor.execute("SELECT nome_perfil FROM perfil ORDER BY RAND() LIMIT 1;") 
            return cursor.fetchone()
        result = self.connection.cursor(aux)        
        return result

    def logar(self, nome, senha):
        if not self._validar_nome_perfil(nome):
            return False
        def aux(cursor):
            cursor.execute("SELECT * FROM perfil p WHERE p.nome_perfil = '{}' AND p.senha = '{}'".format(nome, senha))
            return cursor.fetchall()
        log = self.connection.cursor(aux)
        if len(log):
            self.set_perfil(nome)
            return True
        else:
            return False


    def select_perfil(self, nome):
        return select_profile(nome, self.connection)
    
    def set_perfil(self, nome):
        self.perfil_atual = self.select_perfil(nome)

    def postar(self, texto, foto):
        insert("mensagem", self.mensagem, [texto, str(datetime.now()), '#',self.perfil_atual[0]], self.connection)
        id = str(self.get_mensagens()[-1][0])
        insert("post", self.post, [foto, id], self.connection)

        self.marcar(texto, id) 

        self.criar_topico(texto, id)

    def comentar(self, texto, id_post):
        insert('mensagem',
                self.mensagem,
                [texto, 
                    str(datetime.now()),
                    '#',
                    self.perfil_atual[0]],
                    self.connection)
        id = str(self.get_mensagens()[-1][0])
        insert('comentario',
                self.comentario,
                [str(id), str(id_post)],
                self.connection)

        self.marcar(texto, id) 

        self.criar_topico(texto, id)

    def get_comentarios(self, id_post):
        def aux(cursor):
            query = "SELECT c.id_mensagem, c.id_post, m.texto FROM comentario c INNER JOIN mensagem m ON c.id_mensagem = m.id WHERE c.id_post = '{}';".format(id_post)
            cursor.execute(query)
            return cursor.fetchall()
        return self.connection.cursor(aux)

    def marcar(self, texto, id):
        marcados = self._extrai_marcados(texto)
        for marcado in marcados:
            insert('marcado_perfil',
                    self.marcado_perfil,
                    [str(marcado),
                        id],
                    self.connection)
            self.notificar('marcado', marcado, id)

    def criar_topico(self, texto, id):
        topicos = self._extrair_topicos(texto)
        if len(topicos) > 0:
            topico = topicos[0]
            r = self.verifica_topico(topico)
            if not r:
                insert('topico',
                        self.topico,
                        [topico],
                        self.connection)
            alter('mensagem',
                    'id:{}'.format(id),
                    self.mensagem,
                    [topico],
                    self.connection
                    )            

    def notificar(self, tipo, id_perfil, id_msg="1"):
        insert('notificacao', 
                    self.notificacao, 
                    [self.perfil_atual[0], 
                        str(datetime.now()), 
                        False, 
                        tipo,
                        id_perfil,
                        id_msg],
                    self.connection)

    def verifica_topico(self, topico):
        def aux(cursor):
            cursor.execute("SELECT * FROM topico WHERE topico.nome = '{}'".format(topico))
            x = cursor.fetchall()
            return x
        return self.connection.cursor(aux)

    def ver_notificacoes(self):
        def aux(cursor):
            query = "SELECT * FROM notificacao WHERE nome_notificado = '{}'".format(self.perfil_atual[0])
            cursor.execute(query)

            ret = cursor.fetchall()

            query = """
                DELETE FROM 
                    notificacao
                WHERE
                    nome_notificado = '{}'
            """.format(self.perfil_atual[0])
            cursor.execute(query)

            return ret
        return self.connection.cursor(aux)

    def get_mensagens(self):
        def aux(cursor):
            query = "SELECT * FROM mensagem m WHERE m.nome_criador = '{}' ORDER BY m.id".format(self.perfil_atual[0]) 
            cursor.execute(query)
            return cursor.fetchall()
        return self.connection.cursor(aux)
    
    def mandar_direct(self, texto, id_perfil):
        insert('conversa',
                self.conversa,
                [self.perfil_atual[0],
                    id_perfil,
                    texto],
                self.connection)
        self.notificar('direct', id_perfil)

    def ver_directs(self):
        def aux(cursor):
            query = "SELECT * FROM conversa c WHERE c.nome_destinatario = '{}' OR c.nome_remetente = '{}'".format(self.perfil_atual[0],self.perfil_atual[0])
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
           x = [[i[1], i[5]] for i in ret]
           return x
        return self.connection.cursor(aux)

    def bloquear(self, id_perfil):
        self.deseguir(id_perfil)
        self.apagar_comentarios_em(id_perfil)
        self.remove_marcacao(id_perfil)
        self.remove_directs(id_perfil)
        insert('bloqueia',
                self.bloqueia,
                [self.perfil_atual[0],
                    id_perfil],
                self.connection)

    def apagar_comentarios_em(self, id_perfil):
        query = """
            DELETE FROM 
                comentario c 
            WHERE
                c.id_post IN (
                    SELECT 
                        p.id_mensagem 
                    FROM 
                        post p
                        INNER JOIN mensagem m_s ON p.id_mensagem = m_s.id
                    WHERE
                        m_s.nome_criador = '{0}'
                ) 
                AND
                c.id_mensagem IN (
                    SELECT
                        m.id
                    FROM
                        mensagem m
                    WHERE
                        m.nome_criador = '{1}'
                );
        """.format(id_perfil, self.perfil_atual[0])
        self.connection.cursor(lambda x: x.execute(query))

    def remove_marcacao(self, id_perfil):
        def aux(cursor):
            cursor.execute("""
                    DELETE FROM 
                        marcado_perfil mp 
                    WHERE 
                        mp.id_mensagem IN (
                            SELECT m.id 
                            FROM
                                mensagem m
                            WHERE 
                                m.nome_criador = '{}'
                        )
                        AND
                        mp.nome_marcado = '{}'
                    """.format(self.perfil_atual[0], id_perfil))
        self.connection.cursor(aux)
    
    def remove_directs(self, id_perfil):
        def aux(cursor):
            cursor.execute("""
                    DELETE FROM
                        conversa c
                    WHERE
                        (c.nome_remetente = '{0}'
                        AND
                        c.nome_destinatario = '{1}')
                        OR
                        (c.nome_remetente = '{1}'
                        AND
                        c.nome_destinatario = '{0}') 
                    """.format(self.perfil_atual[0], id_perfil))
        self.connection.cursor(aux)
 

    def deseguir(self, id_perfil):
        def aux(cursor):
            query = """
                DELETE FROM
                    segue 
                WHERE 
                    (nome_seguidor = '{0}'
                    AND 
                    nome_seguido = '{1}')
                    OR
                    (nome_seguidor = '{1}' 
                    AND 
                    nome_seguido = '{0}')

                    """.format(self.perfil_atual[0], id_perfil)
            cursor.execute(query)
        self.connection.cursor(aux)
    
    def seguir(self, id_perfil):
        privacidade = self.select_perfil(id_perfil)[-1]
        if privacidade:
            insert('segue',
                    self.segue,
                    [self.perfil_atual[0],
                        id_perfil],
                    self.connection)
            self.notificar('seguido', self.perfil_atual[0])
        else: 
            self.notificar('seguido_pedido', self.perfil_atual[0])

    def confimar_pedido_seguir(self, id_perfil):
        insert('segue',
                self.segue,
                [id_perfil,
                    self.perfil_atual[0]],
                self.connection)
        self.notificar('confirmacao', id_perfil)

    def get_seguidores(self):
        def aux(cursor):
            cursor.execute("""
                SELECT *
                FROM
                    segue s
                WHERE
                    s.nome_seguido = '{}'
            """.format(self.perfil_atual[0]))
            return cursor.fetchall()
        return self.connection.cursor(aux)
    
    def get_seguidos(self):
        def aux(cursor):
            cursor.execute("""
                SELECT *
                FROM
                    segue s
                WHERE
                    s.nome_seguidor = '{}'
            """.format(self.perfil_atual[0]))
            return cursor.fetchall()
        return self.connection.cursor(aux)
