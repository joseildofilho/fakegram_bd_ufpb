import unittest

from H2Connector import H2Connector

class TestConnection(unittest.TestCase):

    def setUp(self):
        self.connector = H2Connector()

    def test_connection_start(self):
        '''
            Tests if the database is properlly ok.
        '''
        self.assertTrue(self.connector.is_connected())
    
    def test_connection_stop(self):
        '''
            Tests if the connection was properlly ended.
        '''
        self.connector.disconnect()
        self.assertFalse(self.connector.is_connected())

    def test_connection_stop_twice(self):
        '''
            Tests if the close doenst bug if was already called
        '''

        self.connector.disconnect()
        self.connector.disconnect()

    def tearDown(self):
        self.connector.disconnect()

if __name__ == '__main__':
    unittest.main()
