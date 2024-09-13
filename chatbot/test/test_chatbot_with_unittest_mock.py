import pytest
import unittest.mock
from unittest.mock import Mock, call
import chatbot.chatbot
import chatbot.responder


class TestChatbot:
    def construct(self, sock, Responder):
        self.tested = chatbot.chatbot.Chatbot(sock)
        Responder.assert_called_once_with()

    @unittest.mock.patch('chatbot.responder.Responder')
    def test_construction(self, Responder):
        sock = Mock()
        self.construct(sock, Responder)

    @unittest.mock.patch('chatbot.responder.Responder')
    def test_request_response_loop(self, Responder):
        sock = Mock()
        responder = Mock()
        Responder.side_effect = [responder]
        self.construct(sock, Responder)

        class EndTestException(Exception):
            pass

        REQUESTS = [f'request {i}' for i in range(10)]
        RESPONSES = [f'response {i}' for i in range(10)]
        responder.process.side_effect = RESPONSES
        sock.recv.side_effect = REQUESTS + [EndTestException]

        with pytest.raises(EndTestException):
            self.tested.go()

        sock.recv.assert_has_calls([call(4096)] * 10)
        responder.process.assert_has_calls([call(request) for request in REQUESTS])
        sock.send.assert_has_calls([call(response) for response in RESPONSES])
