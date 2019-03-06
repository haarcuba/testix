import socket
from . import responder 

class Chatbot:
    def __init__( self, peer ):
        self._peer = peer
        self._responder = responder.Responder()

    def go(self):
        while True:
            try:
                request = self._peer.recv(4096)
                response = self._responder.process(request)
                self._peer.send(response)
            except socket.error:
                pass
