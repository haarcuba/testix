from testix import *
import forwarder

def test_forward_data_lengths():
    tested = forwarder.Forwarder()
    incoming = Fake('incoming_socket')
    outgoing = Fake('outgoing_socket')
    with Scenario() as s:
        # we'll require that the length of the data is sent, along with a ' ' separator
        s.incoming_socket.recv(4096)  >>  b'some data'
        s.outgoing_socket.send(b'9 ')
        s.incoming_socket.recv(4096)  >>  b'other data'
        s.outgoing_socket.send(b'10 ')
        s.incoming_socket.recv(4096)  >>  b'even more data'
        s.outgoing_socket.send(b'14 ')

        tested.forward_once(incoming, outgoing)
        tested.forward_once(incoming, outgoing)
        tested.forward_once(incoming, outgoing)
