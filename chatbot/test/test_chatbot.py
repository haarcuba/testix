import pytest
import socket
from testix.frequentlyused import *  # noqa: F403
from testix import patch_module  # noqa: F401
from chatbot import chatbot


class TestChatbot:
    @pytest.fixture(autouse=True)
    def globals_patch(self, patch_module):  # noqa: F811
        patch_module(chatbot, 'responder')

    def construct(self):
        with Scenario() as s:
            s.responder.Responder() >> Fake('responder_')
            self.tested = chatbot.Chatbot(Fake('sock'))

    def test_construction(self):
        self.construct()

    def test_request_response_loop(self):
        self.construct()
        with Scenario() as s:
            for i in range(10):
                s.sock.recv(4096) >> f'request {i}'
                s.responder_.process(f'request {i}') >> f'response {i}'
                s.sock.send(f'response {i}')

            s.sock.recv(4096) >> Throwing(TestixLoopBreaker)
            with pytest.raises(TestixLoopBreaker):
                self.tested.go()

    def test_request_response_loop_survives_a_recv_exception(self):
        self.construct()
        with Scenario() as s:
            for i in range(10):
                s.sock.recv(4096) >> f'request {i}'
                s.responder_.process(f'request {i}') >> f'response {i}'
                s.sock.send(f'response {i}')

            s.sock.recv(4096) >> Throwing(socket.error)

            for i in range(10):
                s.sock.recv(4096) >> f'request {i}'
                s.responder_.process(f'request {i}') >> f'response {i}'
                s.sock.send(f'response {i}')

            s.sock.recv(4096) >> Throwing(TestixLoopBreaker)
            with pytest.raises(TestixLoopBreaker):
                self.tested.go()
