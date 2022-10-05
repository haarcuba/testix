from testix import *

def send_some_data(socket, data):
    pass

def test_sending_data():
    fake_socket = Fake('sock')
    with Scenario() as s:
        s.sock.send(b'the data')

        send_some_data(fake_socket, b'the data')

