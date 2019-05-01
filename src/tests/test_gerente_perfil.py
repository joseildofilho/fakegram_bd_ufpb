import unittest
from gerente_perfil import GerentePerfil
from build_database import Tables
from utils import create_fake_profile

class TestQueries(unittest.TestCase):

    def setUp(self):
        self.t = Tables()
        self.t.drop_database()
        self.t.build()
        self.gp = GerentePerfil()
        self.gp.fill()

        self.perfil = create_fake_profile() 
        self.gp.cadastrar_perfil(self.perfil) 
    
    def test_selecion_perfil(self):
        x = self.gp.select_perfil(self.perfil[0])[0]
        self.assertTrue(x == self.perfil[0])

    def test_set_perfil(self):
        self.gp.set_perfil(self.perfil[0])
        for db, local in zip(self.gp.perfil_atual, self.perfil):
            self.assertEqual(db, local)

    def test_alter_perfil(self):
        self.gp.set_perfil(self.perfil[0])

        self.perfil[0] = "Flavio_Serrano"

        self.gp.alterar_perfil(self.perfil)

        self.assertTrue(self.gp.select_perfil(self.perfil[0])[0] == self.perfil[0])

    def test_validar_nome_perfil(self):
        self.assertTrue(self.gp._validar_nome_perfil("Joseildo"))
        self.assertTrue(self.gp._validar_nome_perfil("Joseildo_"))
        self.assertTrue(self.gp._validar_nome_perfil("Joseildo1"))
        self.assertTrue(self.gp._validar_nome_perfil("123Joseildo"))
        self.assertTrue(self.gp._validar_nome_perfil("123_Joseildo"))
        self.assertTrue(self.gp._validar_nome_perfil("Joseildo_123"))

        self.assertFalse(self.gp._validar_nome_perfil("Joseildo "))
        self.assertFalse(self.gp._validar_nome_perfil(" Joseildo "))
        self.assertFalse(self.gp._validar_nome_perfil("Joseildo Mariano"))
        self.assertFalse(self.gp._validar_nome_perfil("Joseildo _"))

    def test_remover_usuario(self):
        self.gp.remove_perfil(self.perfil[0])

        self.assertTrue(self.gp.select_perfil(self.perfil[0]) == None)

    def tearDown(self):
        self.t.drop_database()
