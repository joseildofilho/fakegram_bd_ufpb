import unittest
from gerente_perfil import GerentePerfil
from build_database import Tables
from utils import create_fake_profile
from faker import Faker

f = Faker()

class TestQueries(unittest.TestCase):

    def setUp(self):
        self.t = Tables()
        self.t.drop_database()
        self.t.build()
        self.gp = GerentePerfil()
        self.gp.fill()

        self.perfil_atual = create_fake_profile() 
        self.perfil_atual[4] = True
        self.gp.cadastrar_perfil(self.perfil_atual) 
        self.gp.set_perfil(self.perfil_atual[0])

        self.perfil = create_fake_profile() 
        self.perfil[4] = True
        self.gp.cadastrar_perfil(self.perfil) 
    
    def test_post_basico(self):
        post = [f.text(), f.uri()]
        self.gp.postar(post[0],post[1])
        r = self.gp.get_posts_atual()[0]
        self.assertTrue(post == r)

    def test_dois_posts(self):
        post = [f.text(), f.uri()]
        post2 = [f.text(), f.uri()]

        self.gp.postar(post[0],post[1])
        self.gp.postar(post2[0],post2[1])

        r_post = self.gp.get_posts_atual()[0]
        r_post2 = self.gp.get_posts_atual()[1]

        self.assertTrue(post == r_post)
        self.assertTrue(post2 == r_post2)

    def test_post_com_marcacao(self):
        post = [f.text() + " @" + self.perfil[0], f.uri()]
        self.gp.postar(post[0],post[1])
        r = self.gp.get_posts_atual()[0]
        self.assertTrue(post == r)
        self.gp.set_perfil(self.perfil_atual[0])
        self.assertEqual(self.gp.ver_notificacoes()[0][4], 'marcado')

    def test_post_com_topico(self):
        post = [f.text() + " #tests", f.uri()]
        self.gp.postar(post[0],post[1])
        self.assertTrue(self.gp.verifica_topico("tests") != [])

    def test_comentario(self):
        def aux(cursor):
            cursor.execute("SELECT * FROM comentario")
            return cursor.fetchall()
        post = [f.text(), f.uri()]
        self.gp.postar(post[0], post[1])
        self.gp.comentar("olá", 1)

        self.assertEqual(len(self.gp.connection.cursor(aux)), 1)


    def test_comentario_e_post(self):
        post = ["#test " + f.text() + " @test", f.uri()]
        self.gp.postar(post[0], post[1])
        self.gp.comentar("olá", 1)
        self.assertTrue(self.gp.verifica_topico("test") != [])

    def test_mandar_direct(self):
        texto = f.text()
        self.gp.mandar_direct(texto, self.perfil[0])
        
        self.gp.set_perfil(self.perfil[0])

        self.assertTrue(self.gp.ver_directs()[0][3] == texto)

    def test_remove_comentarios(self):
        def aux(cursor):
            cursor.execute("SELECT * FROM comentario")
            return cursor.fetchall()
        post = [f.text(), ""]
        self.gp.postar(post[0], post[1])

        self.gp.set_perfil(self.perfil[0])

        self.gp.comentar("É isso mesmo", 1) 
        self.gp.comentar("NÉ", 1)

        self.gp.apagar_comentarios_em(self.perfil_atual[0])
        self.assertEqual(len(self.gp.connection.cursor(aux)), 0)

    def test_remove_marcacoes(self):
        def aux(cursor):
            cursor.execute("""
                    SELECT * 
                    FROM 
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
                    """.format(self.perfil_atual[0], self.perfil[0]))
            return cursor.fetchall()
        self.gp.postar("@" + self.perfil[0], "")
        self.gp.remove_marcacao(self.perfil[0])
        self.assertEqual(len(self.gp.connection.cursor(aux)), 0)
    
    def test_apagar_directs(self):
        def aux(cursor):
            cursor.execute("""
                    SELECT *
                    FROM
                        conversa c
                    WHERE
                        (c.nome_remetente = '{0}'
                        AND
                        c.nome_destinatario = '{1}')
                        OR
                        (c.nome_remetente = '{1}'
                        AND
                        c.nome_destinatario = '{0}') 
                    """.format(self.perfil_atual[0], self.perfil[0]))
            return cursor.fetchall()

        self.gp.mandar_direct(f.text(), self.perfil[0])
        self.gp.mandar_direct(f.text(), self.perfil[0])
        self.gp.mandar_direct(f.text(), self.perfil[0])
        self.gp.mandar_direct(f.text(), self.perfil[0])

        self.gp.set_perfil(self.perfil[0])
 
        self.gp.mandar_direct(f.text(), self.perfil_atual[0])
        self.gp.mandar_direct(f.text(), self.perfil_atual[0])
        self.gp.mandar_direct(f.text(), self.perfil_atual[0])
        self.gp.mandar_direct(f.text(), self.perfil_atual[0])

        self.gp.set_perfil(self.perfil_atual[0])

        self.assertEqual(len(self.gp.connection.cursor(aux)), 8)

        self.gp.remove_directs(self.perfil[0])

        self.assertEqual(len(self.gp.connection.cursor(aux)), 0)

    def test_seguir_publico(self):
        def aux(cursor):
            cursor.execute("""
                        SELECT s.nome_seguidor, s.nome_seguido
                        FROM 
                            segue s
                    """)
            return cursor.fetchall()

        self.gp.seguir(self.perfil[0])

        s = self.gp.connection.cursor(aux)[0]

        self.assertEqual(s[0], self.perfil_atual[0])
        self.assertEqual(s[1], self.perfil[0])

    def tearDown(self):
        self.t.drop_database()
