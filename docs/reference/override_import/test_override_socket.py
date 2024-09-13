from testix import *
import pytest
import my_server


@pytest.fixture(autouse=True)  # if autouse is not used here, you will have to specify override_imports as an argument to test_my_server() below
def override_imports(patch_module):
    patch_module(my_server, 'socket')  # replace socket with Fake('socket')


def test_my_server():
    with Scenario() as s:
        s.socket.socket() >> Fake('server_sock')
        s.server_sock.listen()

        s.server_sock.accept() >> (Fake('connection'), 'some address info')
        s.connection.send(b'hi')
        s.connection.close()

        tested = my_server.MyServer()
        tested.serve_request()
