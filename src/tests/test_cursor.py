import unittest

from H2Connector import H2Connector

class TestCursor(unittest.TestCase):

    def setUp(self):
        self.connector = H2Connector()

    def test_cursor(self):
        def query(cursor):
            cursor.execute('CREATE TABLE tests')
            cursor.execute('CREATE TABLE testss')
            cursor.execute('DROP TABLE tests, testss')
        self.connector.cursor(query)

    def tearDown(self):
        self.connector.rollback()
        self.connector.disconnect()

