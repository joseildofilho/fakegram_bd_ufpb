import jaydebeapi

class H2Connector():
    def __init__(self, 
            class_ = 'org.h2.Driver',
            path = 'jdbc:h2:~/test',
            access = ['sa', ''],
            drive='/mnt/00740a3e-0e71-4596-8c4d-789bec641854/codigos/fakegram_bd_ufpb/h2/bin/h2-1.4.197.jar'):
        '''
            
        '''

        self._class_ = class_
        self._path = path
        self._access = access
        self._drive = drive

        self._conn = jaydebeapi.connect(self._class_, self._path, self._access, self._drive)
 
    def is_connected(self):
        return True if self._conn else False

    def disconnect(self):
        if self._conn:
            self._conn.close()
            self._conn = None    

    def rollback(self):
        if self._conn:
            self._conn.rollback()
        else:
            raise Exception('Not conected')

    def cursor(self, query):
        if not self._conn:
            raise Exception('Not connected')
        try:
            cursor = self._conn.cursor()
            query(cursor)
            cursor.close()
        except Exception:
            self.rollback()
            raise Exception("Query fails")

