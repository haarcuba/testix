class Reader:
    def __init__(self, socket):
        self._sock = socket

    def read(self):
        accumulated = b''
        while True:
            data = self._sock.recv(4096)
            if data == b'':
                self._sock.close()
                return accumulated
            accumulated += data
