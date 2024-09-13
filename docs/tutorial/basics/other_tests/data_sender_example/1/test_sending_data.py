from testix import *

import data_sender


def test_sending_data():
    fake_socket = Fake('sock')
    with Scenario() as s:
        s.sock.send(b'the data')

        data_sender.send_some_data(fake_socket, b'the data')
