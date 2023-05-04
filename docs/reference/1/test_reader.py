from testix import *

import reader

def test_read_all_from_socket():
    with Scenario() as s:
        s.sock.recv(4096) >> b'data1'
        s.sock.recv(4096) >> b'data2'
        s.sock.recv(4096) >> b'data3'
        NO_MORE_DATA = b''
        s.sock.recv(4096) >> b''
        s.sock.close()

        tested = reader.Reader(Fake('sock'))
        assert tested.read() == b'data1data2data3'
