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
        post = [f.text(), f.uri()]
        self.gp.postar(post[0], post[1])
        self.gp.comentar("olá", 1)
        print(self.gp.get_comentarios(1))

    def test_comentario(self):
        post = ["#test " + f.text() + " @test", f.uri()]
        self.gp.postar(post[0], post[1])
        self.gp.comentar("olá", 1)
        self.assertTrue(self.gp.verifica_topico("test") != [])

    def test_mandar_direct(self):
        texto = f.text()
        self.gp.mandar_direct(texto, self.perfil[0])
        
        self.gp.set_perfil(self.perfil[0])

        self.assertTrue(self.gp.ver_directs()[0][3] == texto)

    def tearDown(self):
        self.t.drop_database()
