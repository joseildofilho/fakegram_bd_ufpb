import unittest
from gerente_perfil import GerentePerfil
from build_database import Tables

class TestQueries(unittest.TestCase):

    def setUp(self):
        self.t = Tables()
        self.t.drop_database()
        self.t.build()
        self.gp = GerentePerfil()
        self.gp.fill()
    
    def test_selecion_perfil_aleatorio(self):
        print("test selection:",self.gp.seleciona_perfil_aleatorio())
    
    def tearDown(self):
        self.t.drop_database()
