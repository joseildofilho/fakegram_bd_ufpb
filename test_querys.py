import unittest
from H2Connector import H2Connector

class TestQueries(unittest.TestCase):

    def setUp(self):
        self.conn = H2Connector()
        self.conn.cursor(lambda cursor: 
            cursor.execute("CREATE TABLE pessoa (nome varchar(255),idade int,cpf int,PRIMARY KEY (cpf));")
)
    
    def test_single_insert(self):
        def query(cursor):
            cursor.execute("INSERT INTO pessoa (nome, idade, cpf) VALUES ('joao', 20, 103342)")
            print(cursor.execute("SELECT * FROM pessoa"))
        self.conn.cursor(query)

    def tearDown(self):
        self.conn.cursor(lambda cursor:
                cursor.execute("DROP TABLE pessoa;"))
        self.conn.disconnect()
