class Forwarder:
    def forward_once(self, read_from, write_to):
        data = read_from.recv(4096)
        binary = bytes('{} '.format(len(data)), 'latin-1')
        write_to.send(binary)
        write_to.close()
