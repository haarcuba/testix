import socket  # when the test runs, this is actually Fake('socket')


class MyServer:
    def __init__(self):
        self._socket = socket.socket()
        self._socket.listen()

    def serve_request(self):
        other_side, address = self._socket.accept()
        other_side.send(b'hi')
        other_side.close()
