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
        self.gp.cadastrar_perfil(self.perfil_atual) 
        self.gp.set_perfil(self.perfil_atual[0])

        self.perfil = create_fake_profile() 
        self.gp.cadastrar_perfil(self.perfil) 
        self.gp.set_perfil(self.perfil[0])
    
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

    def tearDown(self):
        self.t.drop_database()
