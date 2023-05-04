from testix import *

import reader

def test_read_all_from_socket():
    with Scenario() as s:
        s.sock.recv(IgnoreArgument()) >> b'data1'
        s.sock.recv(IgnoreArgument()) >> b'data2'
        s.sock.recv(IgnoreArgument()) >> b'data3'
        NO_MORE_DATA = b''
        s.sock.recv(IgnoreArgument()) >> b''
        s.sock.close()

        tested = reader.Reader(Fake('sock'))
        assert tested.read() == b'data1data2data3'
