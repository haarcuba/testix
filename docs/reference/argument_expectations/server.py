class Server:
    def __init__(self, database):
        self._database = database

    def connect1(self):
        self._database.connect()

    def connect2(self):
        self._database.connect(1, 2, 3, x='y')

    def connect3(self):
        self._database.connect(a='1', b='2', c='3')
