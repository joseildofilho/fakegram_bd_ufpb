import jaydebeapi

class H2Connector(object):

    _instance = None

    def __init__(self, 
            class_ = 'org.h2.Driver',
            path = 'jdbc:h2:~/test',
            access = ['sa', ''],
            drive='h2/bin/h2-1.4.199.jar'):
        self._class_ = class_
        self._path = path
        self._access = access
        self._drive = drive

        self._conn = jaydebeapi.connect(self._class_, self._path, self._access, self._drive)

    def __new__(cls, *args, **kwargs):
        print("getting new instance")
        if not cls._instance:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance
 
    def is_connected(self):
        return True if self._conn else False

    def disconnect(self):
        if self._conn:
            self._conn.close()
            self._conn = None    
            self._instance = None

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
            aux = query(cursor)
            cursor.close()
            return aux
        except Exception:
            self.rollback()
            raise Exception("Query fails")

